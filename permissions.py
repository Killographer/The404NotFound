"""
Permission-based detection for fake loan apps
Checks for suspicious or excessive permissions
"""

# Common suspicious permissions that fake loan apps often request
SUSPICIOUS_PERMISSIONS = [
    'android.permission.READ_SMS',
    'android.permission.SEND_SMS',
    'android.permission.READ_CONTACTS',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.CAMERA',
    'android.permission.RECORD_AUDIO',
    'android.permission.READ_PHONE_STATE',
    'android.permission.CALL_PHONE',
    'android.permission.READ_CALL_LOG',
    'android.permission.WRITE_EXTERNAL_STORAGE'
]

# Permissions that legitimate loan apps might need
NORMAL_PERMISSIONS = [
    'android.permission.INTERNET',
    'android.permission.ACCESS_NETWORK_STATE',
    'android.permission.READ_PHONE_STATE'  # For device ID (sometimes needed)
]


def check_permissions(package_name, apk_path=None):
    """
    Analyze permissions requested by the app
    Returns risk score and suspicious permissions found
    
    Args:
        package_name: Package name of the app
        apk_path: Optional path to APK file (for future real implementation)
    
    Returns:
        Dictionary with permission analysis results
    """
    # For this demo, we'll simulate permission checking
    # In a real implementation, you'd extract permissions from APK using aapt or similar
    
    result = {
        "risk_score": 0,
        "suspicious_permissions": [],
        "total_permissions": 0,
        "message": ""
    }
    
    # Simulate permission extraction based on package name patterns
    # This is a simplified version - real implementation would parse AndroidManifest.xml
    
    detected_permissions = simulate_permission_extraction(package_name)
    result["total_permissions"] = len(detected_permissions)
    
    # Check for suspicious permissions
    suspicious_found = []
    for perm in detected_permissions:
        if perm in SUSPICIOUS_PERMISSIONS:
            suspicious_found.append(perm)
            result["risk_score"] += 10  # Each suspicious permission adds 10 points
    
    result["suspicious_permissions"] = suspicious_found
    
    # If too many permissions, add risk
    if len(detected_permissions) > 15:
        result["risk_score"] += 15
        result["message"] = "App requests excessive permissions"
    elif len(suspicious_found) > 0:
        result["message"] = f"Found {len(suspicious_found)} suspicious permission(s)"
    else:
        result["message"] = "Permissions look normal"
    
    return result


def simulate_permission_extraction(package_name):
    """
    Simulate extracting permissions from an app
    In real implementation, this would parse AndroidManifest.xml
    
    This function uses heuristics based on package name to simulate results
    """
    permissions = ['android.permission.INTERNET', 'android.permission.ACCESS_NETWORK_STATE']
    
    # Add some logic based on package name patterns
    package_lower = package_name.lower()
    
    # Fake apps often have certain patterns - add suspicious perms
    if any(word in package_lower for word in ['loan', 'cash', 'money', 'credit']):
        # Simulate suspicious behavior - fake loan apps often request these
        if 'fake' in package_lower or 'clone' in package_lower:
            permissions.extend([
                'android.permission.READ_SMS',
                'android.permission.SEND_SMS',
                'android.permission.READ_CONTACTS',
                'android.permission.ACCESS_FINE_LOCATION',
                'android.permission.CAMERA'
            ])
        # Even legitimate-sounding ones might request too much
        elif len(package_name) < 15:  # Short package names sometimes suspicious
            permissions.extend([
                'android.permission.READ_SMS',
                'android.permission.READ_CONTACTS'
            ])
    
    # Add some random normal permissions to make it realistic
    permissions.append('android.permission.WAKE_LOCK')
    permissions.append('android.permission.VIBRATE')
    
    return permissions

