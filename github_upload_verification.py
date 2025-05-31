#!/usr/bin/env python3
"""
GitHub Upload Verification Script
Verifies that the repository is ready for GitHub upload
"""

import os
import subprocess
from pathlib import Path

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """Check Git repository status"""
    print("🔍 Checking Git Repository Status...")
    
    # Check if we're in a git repository
    success, output, error = run_command("git status")
    if not success:
        print("❌ Not a Git repository or Git not available")
        return False
    
    # Check if there are any uncommitted changes
    if "nothing to commit" in output:
        print("✅ All changes committed")
    else:
        print("⚠️ Uncommitted changes detected:")
        print(output)
        return False
    
    # Check number of commits
    success, output, error = run_command("git rev-list --count HEAD")
    if success and output:
        print(f"✅ Repository has {output} commit(s)")
    
    return True

def check_files():
    """Check important files are present"""
    print("\n📁 Checking Important Files...")
    
    required_files = [
        "README.md",
        ".gitignore", 
        "package.json",
        "backend/requirements.txt",
        "frontend/package.json",
        "backend/.env.example",
        "frontend/.env.example"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_sensitive_files():
    """Check that sensitive files are properly ignored"""
    print("\n🔒 Checking Sensitive Files...")
    
    sensitive_patterns = [
        "*.env",
        "*.db", 
        "__pycache__",
        "node_modules"
    ]
    
    # Check if .gitignore exists and contains sensitive patterns
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
            
        for pattern in sensitive_patterns:
            if pattern.replace("*", "") in gitignore_content:
                print(f"✅ {pattern} patterns ignored")
            else:
                print(f"⚠️ {pattern} patterns not found in .gitignore")
    
    # Check if actual sensitive files are tracked
    success, output, error = run_command("git ls-files")
    if success:
        tracked_files = output.split('\n') if output else []
        sensitive_found = []
        
        for file in tracked_files:
            if (file.endswith('.env') or 
                file.endswith('.db') or 
                'node_modules' in file or
                '__pycache__' in file):
                sensitive_found.append(file)
        
        if sensitive_found:
            print("⚠️ Sensitive files found in Git:")
            for file in sensitive_found:
                print(f"   - {file}")
            return False
        else:
            print("✅ No sensitive files tracked")
    
    return True

def check_documentation():
    """Check documentation files"""
    print("\n📚 Checking Documentation...")
    
    doc_files = [
        "docs/DOKUMENTASI.md",
        "docs/PANDUAN_CEPAT.md", 
        "docs/FINAL_STATUS_REPORT.md",
        "docs/CHANGELOG.md"
    ]
    
    for doc in doc_files:
        if os.path.exists(doc):
            print(f"✅ {doc}")
        else:
            print(f"❌ {doc}")
    
    return True

def get_repository_stats():
    """Get repository statistics"""
    print("\n📊 Repository Statistics...")
    
    # Count files
    success, output, error = run_command("git ls-files | wc -l")
    if success and output:
        print(f"📁 Total files: {output.strip()}")
    
    # Get languages
    extensions = {}
    success, output, error = run_command("git ls-files")
    if success and output:
        for file in output.split('\n'):
            if '.' in file:
                ext = file.split('.')[-1].lower()
                extensions[ext] = extensions.get(ext, 0) + 1
    
    print("📝 File types:")
    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   .{ext}: {count} files")

def main():
    """Main verification function"""
    print("🚀 GitHub Upload Verification")
    print("=" * 40)
    
    checks = [
        ("Git Status", check_git_status),
        ("Required Files", check_files), 
        ("Sensitive Files", check_sensitive_files),
        ("Documentation", check_documentation)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
            all_passed = False
    
    get_repository_stats()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 READY FOR GITHUB UPLOAD!")
        print("✅ All checks passed")
        print("\nNext steps:")
        print("1. Create repository on github.com")
        print("2. Add remote: git remote add origin <URL>") 
        print("3. Push: git push -u origin main")
    else:
        print("⚠️ ISSUES FOUND")
        print("Please fix the issues above before uploading")
    
    return all_passed

if __name__ == "__main__":
    main()
