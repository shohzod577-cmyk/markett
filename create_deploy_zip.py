#!/usr/bin/env python3
"""
AWS Elastic Beanstalk uchun to'g'ri ZIP yaratish scripti
Linux-compatible path separators bilan
"""
import zipfile
import os
from pathlib import Path

def create_eb_zip(output_filename='markett-v5-fixed.zip'):
    """Create deployment ZIP with Unix-style path separators"""
    
    # Files and directories to include
    include_dirs = [
        'apps',
        'config',
        'core',
        'locale',
        'static',
        'templates',
        '.ebextensions'
    ]
    
    include_files = [
        'manage.py',
        'requirements.txt',
        '.ebignore'
    ]
    
    # Files to exclude
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.git',
        '.venv',
        'venv',
        'env',
        '.env',
        'db.sqlite3',
        'media',
        'backup',
        'market_mvp',
        'scripts',
        'staticfiles',
        '.DS_Store',
        'Thumbs.db'
    ]
    
    print(f"Creating deployment ZIP: {output_filename}")
    print("=" * 60)
    
    # Create ZIP with Unix-style paths
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        
        # Add directories
        for dir_name in include_dirs:
            dir_path = Path(dir_name)
            if not dir_path.exists():
                print(f"Skipping {dir_name} (not found)")
                continue
                
            print(f"Adding directory: {dir_name}/")
            
            for file_path in dir_path.rglob('*'):
                # Skip excluded patterns
                if any(pattern in str(file_path) for pattern in exclude_patterns):
                    continue
                    
                if file_path.is_file():
                    # Convert Windows path to Unix path (forward slashes)
                    arcname = str(file_path).replace('\\', '/')
                    zipf.write(file_path, arcname=arcname)
                    file_count += 1
        
        # Add individual files
        for file_name in include_files:
            file_path = Path(file_name)
            if file_path.exists():
                # Use forward slashes
                arcname = file_name.replace('\\', '/')
                zipf.write(file_path, arcname=arcname)
                print(f"Added: {file_name}")
                file_count += 1
            else:
                print(f"Skipping {file_name} (not found)")
    
    # Get file size
    file_size = os.path.getsize(output_filename)
    size_mb = file_size / (1024 * 1024)
    
    print("=" * 60)
    print(f"SUCCESS! Created: {output_filename}")
    print(f"Size: {size_mb:.2f} MB ({file_count} files)")
    print(f"Ready for AWS Elastic Beanstalk deployment!")
    print("\nNext steps:")
    print("1. Upload this ZIP via AWS Console")
    print("2. Deploy to Markett-env environment")
    
    return output_filename

if __name__ == '__main__':
    create_eb_zip()
