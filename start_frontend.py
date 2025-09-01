#!/usr/bin/env python3
"""
Startup script for the Excel Financial Processor frontend
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    # Change to frontend directory
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    print("🚀 Starting Excel Financial Processor Frontend...")
    print(f"📁 Working directory: {frontend_dir}")
    print("🌐 Application will be available at: http://localhost:3000")
    print("-" * 50)
    
    try:
        # Start the React development server
        subprocess.run([
            "npm", "start"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting frontend: {e}")
        print("💡 Make sure you have Node.js installed and run 'npm install' first.")
        sys.exit(1)

if __name__ == "__main__":
    main()
