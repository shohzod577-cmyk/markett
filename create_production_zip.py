import os
import zipfile
from pathlib import Path

print("Creating PRODUCTION deployment package...")
print("=" * 60)

exclude_dirs = {
    'venv', '__pycache__', '.git', '.idea', 'staticfiles', 
    'backup', 'market_mvp', 'node_modules', '.pytest_cache',
    '.vscode', 'htmlcov', '.coverage'
}

exclude_files = {
    '.env', 'db.sqlite3', '.DS_Store', 'markett-deploy.zip',
    'markett-minimal-test.zip', '.gitignore', 'remove_comments.py',
    'create_minimal_zip.py', 'create_deploy_zip.py'
}

def should_exclude(path):
    parts = Path(path).parts
    return any(excluded in parts for excluded in exclude_dirs)

included_files = []
with zipfile.ZipFile('markett-production.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file in exclude_files:
                continue
                
            file_path = os.path.join(root, file)
            
            if should_exclude(file_path):
                continue
            
            arcname = file_path[2:] if file_path.startswith('.\\') or file_path.startswith('./') else file_path
            
            zipf.write(file_path, arcname)
            included_files.append(arcname)

print(f"\n✅ SUCCESS! Created: markett-production.zip")
print(f"📦 Size: {os.path.getsize('markett-production.zip') / (1024*1024):.2f} MB")
print(f"📄 Files: {len(included_files)}")
print("\nThis is PRODUCTION deployment with:")
print("  ✅ All apps (cart, products, orders, etc.)")
print("  ✅ Templates and static files")
print("  ✅ Configuration files")
print("  ✅ Requirements.txt")
print("\nReady to deploy to AWS Elastic Beanstalk!")
