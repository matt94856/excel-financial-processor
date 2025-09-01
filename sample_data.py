#!/usr/bin/env python3
"""
Script to generate sample Excel files for testing
"""
import pandas as pd
from pathlib import Path

def create_sample_estimate():
    """Create a sample estimate Excel file"""
    data = {
        'Description': [
            'Labor - Project Setup',
            'Materials - Hardware Components',
            'Software License',
            'Testing and Quality Assurance',
            'Project Management',
            'Documentation',
            'Training',
            'Support (3 months)'
        ],
        'Quantity': [40, 1, 1, 20, 15, 8, 4, 1],
        'Unit Price': [75.00, 2500.00, 500.00, 100.00, 125.00, 80.00, 150.00, 2000.00],
        'Total': [3000.00, 2500.00, 500.00, 2000.00, 1875.00, 640.00, 600.00, 2000.00]
    }
    
    df = pd.DataFrame(data)
    
    # Add subtotals
    subtotal_row = pd.DataFrame({
        'Description': ['Subtotal'],
        'Quantity': [''],
        'Unit Price': [''],
        'Total': [df['Total'].sum()]
    })
    
    # Add tax
    tax_row = pd.DataFrame({
        'Description': ['Tax (8.5%)'],
        'Quantity': [''],
        'Unit Price': [''],
        'Total': [df['Total'].sum() * 0.085]
    })
    
    # Add grand total
    grand_total = df['Total'].sum() * 1.085
    total_row = pd.DataFrame({
        'Description': ['TOTAL'],
        'Quantity': [''],
        'Unit Price': [''],
        'Total': [grand_total]
    })
    
    # Combine all data
    final_df = pd.concat([df, subtotal_row, tax_row, total_row], ignore_index=True)
    
    # Save to Excel
    output_path = Path("sample_estimate.xlsx")
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        final_df.to_excel(writer, sheet_name='Estimate', index=False)
    
    print(f"✅ Created sample estimate: {output_path}")
    return output_path

def create_sample_financial():
    """Create a sample financial statement Excel file"""
    # Income Statement
    income_data = {
        'Item': [
            'Revenue',
            'Cost of Goods Sold',
            'Gross Profit',
            'Operating Expenses',
            'Salaries',
            'Rent',
            'Utilities',
            'Marketing',
            'Total Operating Expenses',
            'Operating Income',
            'Interest Expense',
            'Income Before Tax',
            'Tax Expense',
            'Net Income'
        ],
        'Amount': [
            500000,
            -200000,
            300000,
            '',
            -120000,
            -24000,
            -12000,
            -30000,
            -186000,
            114000,
            -5000,
            109000,
            -21800,
            87200
        ]
    }
    
    # Balance Sheet
    balance_data = {
        'Item': [
            'ASSETS',
            'Current Assets',
            'Cash',
            'Accounts Receivable',
            'Inventory',
            'Total Current Assets',
            'Fixed Assets',
            'Equipment',
            'Total Assets',
            '',
            'LIABILITIES',
            'Current Liabilities',
            'Accounts Payable',
            'Short-term Debt',
            'Total Current Liabilities',
            'Long-term Debt',
            'Total Liabilities',
            '',
            'EQUITY',
            'Owner Equity',
            'Retained Earnings',
            'Total Equity',
            'Total Liabilities & Equity'
        ],
        'Amount': [
            '',
            0,
            50000,
            75000,
            30000,
            155000,
            0,
            100000,
            255000,
            '',
            '',
            0,
            25000,
            15000,
            40000,
            50000,
            90000,
            '',
            '',
            100000,
            65000,
            165000,
            255000
        ]
    }
    
    # Save to Excel
    output_path = Path("sample_financial.xlsx")
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        pd.DataFrame(income_data).to_excel(writer, sheet_name='Income Statement', index=False)
        pd.DataFrame(balance_data).to_excel(writer, sheet_name='Balance Sheet', index=False)
    
    print(f"✅ Created sample financial statement: {output_path}")
    return output_path

def create_mixed_sample():
    """Create a sample with mixed content"""
    # Project data
    project_data = {
        'Project': [
            'Website Development',
            'Mobile App',
            'Database Design',
            'API Integration',
            'Testing',
            'Deployment'
        ],
        'Hours': [120, 200, 80, 60, 40, 20],
        'Rate': [100, 120, 90, 110, 80, 100],
        'Total': [12000, 24000, 7200, 6600, 3200, 2000]
    }
    
    # Budget data
    budget_data = {
        'Category': [
            'Development',
            'Design',
            'Testing',
            'Infrastructure',
            'Marketing',
            'Miscellaneous'
        ],
        'Budget': [50000, 15000, 10000, 8000, 12000, 5000],
        'Actual': [48000, 16000, 9500, 7500, 11000, 4500],
        'Variance': [-2000, 1000, -500, -500, -1000, -500]
    }
    
    # Save to Excel
    output_path = Path("sample_mixed.xlsx")
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        pd.DataFrame(project_data).to_excel(writer, sheet_name='Projects', index=False)
        pd.DataFrame(budget_data).to_excel(writer, sheet_name='Budget', index=False)
    
    print(f"✅ Created sample mixed content: {output_path}")
    return output_path

def main():
    print("📊 Creating sample Excel files for testing...")
    print("-" * 50)
    
    # Create sample files
    estimate_file = create_sample_estimate()
    financial_file = create_sample_financial()
    mixed_file = create_mixed_sample()
    
    print("-" * 50)
    print("✅ Sample files created successfully!")
    print(f"📁 Files created:")
    print(f"   • {estimate_file}")
    print(f"   • {financial_file}")
    print(f"   • {mixed_file}")
    print("\n💡 You can now test the application with these sample files.")

if __name__ == "__main__":
    main()
