"""
Helper utility functions
"""

import os
import zipfile


def extract_package_name_from_apk(apk_path):
    """
    Extract package name from APK file
    In a real implementation, you'd use aapt (Android Asset Packaging Tool)
    or parse AndroidManifest.xml
    
    For this demo, we simulate extraction
    """
    # Real implementation would do:
    # aapt dump badging app.apk | grep package
    
    # For demo, extract from filename or return a default
    filename = os.path.basename(apk_path)
    
    # Try to extract package name from filename if it looks like one
    if '.apk' in filename:
        # Remove .apk extension
        name_part = filename.replace('.apk', '')
        
        # If filename looks like a package name (has dots), use it
        if '.' in name_part and len(name_part) > 5:
            return name_part
    
    # Default: generate a mock package name based on file
    # In real app, you'd parse the APK properly
    return f"com.example.{filename.replace('.apk', '').replace(' ', '').lower()}"


def validate_package_name(package_name):
    """
    Validate if a string looks like a valid Android package name
    """
    if not package_name:
        return False
    
    # Basic validation: should have at least one dot
    if '.' not in package_name:
        return False
    
    # Should not have spaces
    if ' ' in package_name:
        return False
    
    # Should be reasonable length
    if len(package_name) < 5 or len(package_name) > 200:
        return False
    
    return True

