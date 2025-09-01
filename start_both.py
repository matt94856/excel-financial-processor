#!/usr/bin/env python3
"""
Startup script to run both backend and frontend simultaneously
"""
import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_backend():
    """Run the backend server"""
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    print("🚀 Starting Backend Server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("👋 Backend server stopped.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Run the frontend server"""
    # Wait a bit for backend to start
    time.sleep(3)
    
    frontend_dir = Path(__file__).parent / "frontend"
    os.chdir(frontend_dir)
    
    print("🚀 Starting Frontend Server...")
    try:
        subprocess.run([
            "npm", "start"
        ], check=True)
    except KeyboardInterrupt:
        print("👋 Frontend server stopped.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend error: {e}")

def main():
    print("🚀 Starting Excel Financial Processor...")
    print("🌐 Backend: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("-" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Start frontend in main thread
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n👋 Application stopped.")

if __name__ == "__main__":
    main()
