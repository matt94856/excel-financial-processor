import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ExcelProcessor:
    def __init__(self):
        self.estimate_keywords = [
            'estimate', 'quote', 'proposal', 'cost', 'price', 'amount',
            'labor', 'materials', 'equipment', 'subtotal', 'total'
        ]
        self.financial_keywords = [
            'revenue', 'income', 'expense', 'profit', 'loss', 'balance',
            'assets', 'liabilities', 'equity', 'cash flow', 'statement'
        ]
    
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process Excel file and return structured data"""
        try:
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=None)
            
            processed_data = {
                'file_name': file_path.name,
                'sheets': {},
                'estimates': [],
                'financial_statements': [],
                'summary': {}
            }
            
            for sheet_name, sheet_df in df.items():
                logger.info(f"Processing sheet: {sheet_name}")
                
                # Clean the dataframe
                cleaned_df = self._clean_dataframe(sheet_df)
                
                # Detect content type
                content_type = self._detect_content_type(cleaned_df)
                
                # Process based on content type
                if content_type == 'estimate':
                    estimate_data = self._process_estimate(cleaned_df, sheet_name)
                    processed_data['estimates'].append(estimate_data)
                elif content_type == 'financial':
                    financial_data = self._process_financial_statement(cleaned_df, sheet_name)
                    processed_data['financial_statements'].append(financial_data)
                else:
                    # Mixed or unknown content
                    mixed_data = self._process_mixed_content(cleaned_df, sheet_name)
                    processed_data['sheets'][sheet_name] = mixed_data
            
            # Generate summary
            processed_data['summary'] = self._generate_summary(processed_data)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare dataframe for processing"""
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Fill NaN values with empty strings
        df = df.fillna('')
        
        # Convert all data to string for consistent processing
        df = df.astype(str)
        
        return df
    
    def _detect_content_type(self, df: pd.DataFrame) -> str:
        """Detect if content is estimate, financial statement, or mixed"""
        # Get all text content
        all_text = ' '.join(df.values.flatten()).lower()
        
        estimate_score = sum(1 for keyword in self.estimate_keywords if keyword in all_text)
        financial_score = sum(1 for keyword in self.financial_keywords if keyword in all_text)
        
        if estimate_score > financial_score and estimate_score > 2:
            return 'estimate'
        elif financial_score > estimate_score and financial_score > 2:
            return 'financial'
        else:
            return 'mixed'
    
    def _process_estimate(self, df: pd.DataFrame, sheet_name: str) -> Dict[str, Any]:
        """Process estimate data"""
        estimate_data = {
            'sheet_name': sheet_name,
            'title': f"Estimate - {sheet_name}",
            'items': [],
            'subtotals': [],
            'total': 0,
            'headers': []
        }
        
        # Find headers (usually first row with meaningful content)
        headers = self._find_headers(df)
        estimate_data['headers'] = headers
        
        # Process data rows
        for idx, row in df.iterrows():
            if idx == 0:  # Skip header row
                continue
            
            # Check if row contains numeric data
            numeric_values = self._extract_numeric_values(row)
            if numeric_values:
                item = {
                    'description': self._get_description(row),
                    'quantity': self._get_quantity(row),
                    'unit_price': self._get_unit_price(row),
                    'total': self._get_total(row),
                    'row_data': row.tolist()
                }
                estimate_data['items'].append(item)
        
        # Calculate totals
        estimate_data['total'] = sum(item['total'] for item in estimate_data['items'])
        
        return estimate_data
    
    def _process_financial_statement(self, df: pd.DataFrame, sheet_name: str) -> Dict[str, Any]:
        """Process financial statement data"""
        financial_data = {
            'sheet_name': sheet_name,
            'title': f"Financial Statement - {sheet_name}",
            'sections': [],
            'headers': []
        }
        
        # Find headers
        headers = self._find_headers(df)
        financial_data['headers'] = headers
        
        # Group rows into sections
        current_section = None
        for idx, row in df.iterrows():
            if idx == 0:  # Skip header row
                continue
            
            # Check if this is a section header
            if self._is_section_header(row):
                if current_section:
                    financial_data['sections'].append(current_section)
                current_section = {
                    'name': self._get_section_name(row),
                    'items': []
                }
            else:
                # Add item to current section
                numeric_values = self._extract_numeric_values(row)
                if numeric_values and current_section:
                    item = {
                        'description': self._get_description(row),
                        'amount': self._get_amount(row),
                        'row_data': row.tolist()
                    }
                    current_section['items'].append(item)
        
        # Add last section
        if current_section:
            financial_data['sections'].append(current_section)
        
        return financial_data
    
    def _process_mixed_content(self, df: pd.DataFrame, sheet_name: str) -> Dict[str, Any]:
        """Process mixed or unknown content"""
        return {
            'sheet_name': sheet_name,
            'title': f"Data - {sheet_name}",
            'data': df.to_dict('records'),
            'headers': df.columns.tolist()
        }
    
    def _find_headers(self, df: pd.DataFrame) -> List[str]:
        """Find column headers"""
        # Try first row
        first_row = df.iloc[0].tolist()
        if any(str(cell).strip() for cell in first_row):
            return [str(cell).strip() for cell in first_row]
        
        # Use column names as fallback
        return df.columns.tolist()
    
    def _extract_numeric_values(self, row: pd.Series) -> List[float]:
        """Extract numeric values from a row"""
        numeric_values = []
        for cell in row:
            if isinstance(cell, (int, float)) and not pd.isna(cell):
                numeric_values.append(float(cell))
            elif isinstance(cell, str):
                # Try to extract numbers from strings
                numbers = re.findall(r'-?\d+\.?\d*', cell)
                numeric_values.extend([float(n) for n in numbers])
        return numeric_values
    
    def _get_description(self, row: pd.Series) -> str:
        """Extract description from row (usually first non-numeric column)"""
        for cell in row:
            if isinstance(cell, str) and cell.strip() and not re.match(r'^-?\d+\.?\d*$', cell.strip()):
                return cell.strip()
        return "Item"
    
    def _get_quantity(self, row: pd.Series) -> float:
        """Extract quantity from row"""
        numeric_values = self._extract_numeric_values(row)
        return numeric_values[0] if numeric_values else 1.0
    
    def _get_unit_price(self, row: pd.Series) -> float:
        """Extract unit price from row"""
        numeric_values = self._extract_numeric_values(row)
        return numeric_values[1] if len(numeric_values) > 1 else 0.0
    
    def _get_total(self, row: pd.Series) -> float:
        """Extract total from row"""
        numeric_values = self._extract_numeric_values(row)
        if len(numeric_values) >= 3:
            return numeric_values[2]
        elif len(numeric_values) == 2:
            return numeric_values[0] * numeric_values[1]
        else:
            return numeric_values[0] if numeric_values else 0.0
    
    def _get_amount(self, row: pd.Series) -> float:
        """Extract amount from row"""
        numeric_values = self._extract_numeric_values(row)
        return numeric_values[-1] if numeric_values else 0.0
    
    def _is_section_header(self, row: pd.Series) -> bool:
        """Check if row is a section header"""
        # Look for patterns that indicate section headers
        text_content = ' '.join(str(cell) for cell in row).lower()
        return any(keyword in text_content for keyword in ['total', 'subtotal', 'summary', 'section'])
    
    def _get_section_name(self, row: pd.Series) -> str:
        """Extract section name from row"""
        for cell in row:
            if isinstance(cell, str) and cell.strip():
                return cell.strip()
        return "Section"
    
    def _generate_summary(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics"""
        summary = {
            'total_estimates': len(processed_data['estimates']),
            'total_financial_statements': len(processed_data['financial_statements']),
            'total_sheets': len(processed_data['sheets']),
            'grand_total': 0
        }
        
        # Calculate grand total from estimates
        for estimate in processed_data['estimates']:
            summary['grand_total'] += estimate['total']
        
        return summary
