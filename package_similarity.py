"""
Package name similarity checker
Detects apps that might be clones or fakes of popular loan apps
"""

# Known legitimate loan app package names (examples)
LEGITIMATE_LOAN_APPS = [
    'com.paytm.money',
    'com.phonepe.app',
    'com.cred.club',
    'com.groww.invest',
    'com.razorpay.app',
    'com.mobikwik.new',
    'com.freecharge.android'
]

# Common fake/clone patterns
FAKE_PATTERNS = [
    'com.loan',
    'com.quickloan',
    'com.instantloan',
    'com.easyloan',
    'com.cashloan',
    'com.moneyloan'
]


def check_package_similarity(package_name):
    """
    Check if package name is suspiciously similar to known apps
    or matches common fake app patterns
    
    Args:
        package_name: The package name to check
    
    Returns:
        Dictionary with similarity analysis results
    """
    result = {
        "risk_score": 0,
        "similar_apps": [],
        "matches_fake_pattern": False,
        "message": ""
    }
    
    package_lower = package_name.lower()
    
    # Check against known legitimate apps
    similar = []
    for legit_app in LEGITIMATE_LOAN_APPS:
        similarity = calculate_similarity(package_lower, legit_app)
        if similarity > 0.7:  # 70% similar
            similar.append({
                "package": legit_app,
                "similarity": round(similarity * 100, 1)
            })
            result["risk_score"] += 20
    
    result["similar_apps"] = similar
    
    # Check for fake patterns
    for pattern in FAKE_PATTERNS:
        if pattern in package_lower:
            result["matches_fake_pattern"] = True
            result["risk_score"] += 25
            result["message"] = "Package name matches known fake app pattern"
            break
    
    # Check for suspicious characteristics
    if package_lower.count('.') < 2:  # Too short/not properly namespaced
        result["risk_score"] += 10
        if not result["message"]:
            result["message"] = "Package name structure looks suspicious"
    
    # Check for typosquatting (common misspellings)
    if any(typo in package_lower for typo in ['paytmm', 'phonepay', 'credd']):
        result["risk_score"] += 30
        result["message"] = "Possible typosquatting detected"
    
    if not result["message"]:
        if similar:
            result["message"] = f"Similar to {len(similar)} known app(s)"
        else:
            result["message"] = "Package name looks normal"
    
    return result


def calculate_similarity(str1, str2):
    """
    Simple similarity calculation using Levenshtein-like approach
    Returns a value between 0 and 1
    """
    # Extract main parts of package names (last 2 segments)
    parts1 = str1.split('.')[-2:]
    parts2 = str2.split('.')[-2:]
    
    # Compare main parts
    main1 = ''.join(parts1)
    main2 = ''.join(parts2)
    
    # Simple character overlap calculation
    if main1 == main2:
        return 1.0
    
    # Count common characters
    common = 0
    min_len = min(len(main1), len(main2))
    
    for i in range(min_len):
        if main1[i] == main2[i]:
            common += 1
    
    # Also check if one contains the other
    if main1 in main2 or main2 in main1:
        return 0.8
    
    return common / max(len(main1), len(main2)) if max(len(main1), len(main2)) > 0 else 0

