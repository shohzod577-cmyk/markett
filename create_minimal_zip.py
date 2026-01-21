#!/usr/bin/env python3
"""Ultra minimal deployment ZIP - for testing only"""
import zipfile
import os
from pathlib import Path

def create_minimal_zip(output_filename='markett-minimal-test.zip'):
    """Create absolute minimum deployment package"""
    
    # Bare minimum files
    include_dirs = [
        'apps',
        'config',
        'core',
        'templates'
    ]
    
    include_files = [
        'manage.py',
        'requirements.txt'
    ]
    
    # Files to exclude
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.git',
        'db.sqlite3',
        'media',
        'backup',
        'staticfiles'
    ]
    
    print(f"Creating MINIMAL test ZIP: {output_filename}")
    print("=" * 60)
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        
        # Add directories
        for dir_name in include_dirs:
            dir_path = Path(dir_name)
            if not dir_path.exists():
                continue
                
            print(f"Adding: {dir_name}/")
            
            for file_path in dir_path.rglob('*'):
                if any(pattern in str(file_path) for pattern in exclude_patterns):
                    continue
                    
                if file_path.is_file():
                    arcname = str(file_path).replace('\\', '/')
                    zipf.write(file_path, arcname=arcname)
                    file_count += 1
        
        # Add files
        for file_name in include_files:
            file_path = Path(file_name)
            if file_path.exists():
                zipf.write(file_path, arcname=file_name.replace('\\', '/'))
                print(f"Added: {file_name}")
                file_count += 1
        
        # Create minimal .ebextensions
        minimal_config = """option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: config.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: config.settings
"""
        zipf.writestr('.ebextensions/01_django.config', minimal_config)
        print("Added: .ebextensions/01_django.config (minimal)")
        file_count += 1
    
    file_size = os.path.getsize(output_filename)
    size_mb = file_size / (1024 * 1024)
    
    print("=" * 60)
    print(f"SUCCESS! Created: {output_filename}")
    print(f"Size: {size_mb:.2f} MB ({file_count} files)")
    print("\nThis is MINIMAL test version - NO migrations, NO collectstatic")
    print("Use this to test if basic deployment works")
    
    return output_filename

if __name__ == '__main__':
    create_minimal_zip()
