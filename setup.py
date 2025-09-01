#!/usr/bin/env python3
"""
Setup script for Excel Financial Processor
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def setup_backend():
    """Setup backend dependencies"""
    print("🐍 Setting up Python backend...")
    backend_dir = Path(__file__).parent / "backend"
    
    # Create virtual environment
    if not run_command(f"{sys.executable} -m venv venv", cwd=backend_dir, "Creating virtual environment"):
        return False
    
    # Determine activation script based on OS
    if os.name == 'nt':  # Windows
        activate_script = backend_dir / "venv" / "Scripts" / "activate.bat"
        pip_cmd = str(backend_dir / "venv" / "Scripts" / "pip.exe")
    else:  # Unix/Linux/Mac
        activate_script = backend_dir / "venv" / "bin" / "activate"
        pip_cmd = str(backend_dir / "venv" / "bin" / "pip")
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir, "Installing Python dependencies"):
        return False
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Setup frontend dependencies"""
    print("⚛️ Setting up React frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Install npm dependencies
    if not run_command("npm install", cwd=frontend_dir, "Installing Node.js dependencies"):
        return False
    
    print("✅ Frontend setup complete!")
    return True

def create_sample_files():
    """Create sample Excel files for testing"""
    print("📊 Creating sample Excel files...")
    
    if not run_command(f"{sys.executable} sample_data.py", description="Generating sample data"):
        return False
    
    print("✅ Sample files created!")
    return True

def main():
    print("🚀 Excel Financial Processor Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Check if Node.js is installed
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js and npm are required but not installed")
        print("Please install Node.js from https://nodejs.org/")
        sys.exit(1)
    
    print("✅ Prerequisites check passed")
    print()
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    print()
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        sys.exit(1)
    
    print()
    
    # Create sample files
    if not create_sample_files():
        print("❌ Sample file creation failed")
        sys.exit(1)
    
    print()
    print("🎉 Setup complete!")
    print("=" * 50)
    print("📋 Next steps:")
    print("1. Start the backend: python start_backend.py")
    print("2. Start the frontend: python start_frontend.py")
    print("3. Or start both: python start_both.py")
    print()
    print("🌐 URLs:")
    print("• Frontend: http://localhost:3000")
    print("• Backend: http://localhost:8000")
    print("• API Docs: http://localhost:8000/docs")
    print()
    print("📁 Sample files created for testing:")
    print("• sample_estimate.xlsx")
    print("• sample_financial.xlsx")
    print("• sample_mixed.xlsx")

if __name__ == "__main__":
    main()
