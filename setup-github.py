#!/usr/bin/env python3
"""
Script to help set up GitHub repository for Excel Financial Processor
"""
import os
import subprocess
import sys
from pathlib import Path

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def initialize_git_repo():
    """Initialize git repository"""
    try:
        # Check if already a git repo
        if Path(".git").exists():
            print("✅ Git repository already initialized")
            return True
        
        # Initialize git
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing git: {e}")
        return False

def add_files_to_git():
    """Add all files to git"""
    try:
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Files added to git")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error adding files: {e}")
        return False

def create_initial_commit():
    """Create initial commit"""
    try:
        subprocess.run([
            "git", "commit", "-m", 
            "Initial commit - Excel Financial Processor"
        ], check=True)
        print("✅ Initial commit created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating commit: {e}")
        return False

def main():
    print("🚀 GitHub Setup for Excel Financial Processor")
    print("=" * 50)
    
    # Check git installation
    if not check_git_installed():
        print("❌ Git is not installed. Please install git first:")
        print("   https://git-scm.com/downloads")
        sys.exit(1)
    
    print("✅ Git is installed")
    
    # Initialize git repository
    if not initialize_git_repo():
        sys.exit(1)
    
    # Add files
    if not add_files_to_git():
        sys.exit(1)
    
    # Create commit
    if not create_initial_commit():
        sys.exit(1)
    
    print("\n🎉 Git repository setup complete!")
    print("=" * 50)
    print("📋 Next steps:")
    print("1. Create a new repository on GitHub:")
    print("   https://github.com/new")
    print("2. Copy the repository URL")
    print("3. Run these commands:")
    print("   git remote add origin <YOUR_REPO_URL>")
    print("   git push -u origin main")
    print("\n📚 For detailed instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main()
