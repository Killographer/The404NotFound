"""
Play Store metadata checker
Looks up apps in the supplied Pixel Pitch dataset or falls back to a simulation.
"""

from urllib.parse import urlparse, parse_qs, unquote
import re


RAW_DATASET = [
    # ---- REAL APPS ----
    {"package": "in.sbi.lotus", "app_name": "YONO SBI", "developer": "State Bank of India", "rating": 4.0, "reviews": 10_000_000, "downloads": "100M+", "status": "REAL"},
    {"package": "com.hdfcbank.mobilebanking", "app_name": "HDFC Bank MobileBanking", "developer": "HDFC Bank Ltd", "rating": 4.1, "reviews": 5_200_000, "downloads": "50M+", "status": "REAL"},
    {"package": "com.icici.bank.imobile", "app_name": "ICICI iMobile Pay", "developer": "ICICI Bank Ltd", "rating": 4.2, "reviews": 4_800_000, "downloads": "50M+", "status": "REAL"},
    {"package": "com.kmb.banking", "app_name": "Kotak 811 & Mobile Banking", "developer": "Kotak Mahindra Bank", "rating": 4.1, "reviews": 1_200_000, "downloads": "10M+", "status": "REAL"},
    {"package": "com.axis.mobile", "app_name": "Axis Bank Mobile App", "developer": "Axis Bank Ltd", "rating": 4.0, "reviews": 1_400_000, "downloads": "10M+", "status": "REAL"},
    {"package": "com.bob.mobile", "app_name": "Bank of Baroda M-Connect+", "developer": "Bank of Baroda", "rating": 3.8, "reviews": 900_000, "downloads": "10M+", "status": "REAL"},
    {"package": "com.idfcfirstbank.mobile", "app_name": "IDFC FIRST MobileBanking", "developer": "IDFC FIRST Bank", "rating": 4.3, "reviews": 500_000, "downloads": "10M+", "status": "REAL"},
    {"package": "net.one97.paytm", "app_name": "Paytm", "developer": "Paytm Mobile Solutions", "rating": 4.5, "reviews": 17_000_000, "downloads": "500M+", "status": "REAL"},
    {"package": "com.phonepe.app", "app_name": "PhonePe", "developer": "PhonePe Pvt Ltd", "rating": 4.5, "reviews": 40_000_000, "downloads": "500M+", "status": "REAL"},
    {"package": "com.google.android.apps.nbu.paisa.user", "app_name": "Google Pay (GPay)", "developer": "Google LLC", "rating": 4.3, "reviews": 12_000_000, "downloads": "500M+", "status": "REAL"},
    {"package": "in.org.npci.upiapp", "app_name": "BHIM UPI", "developer": "NPCI", "rating": 4.3, "reviews": 900_000, "downloads": "50M+", "status": "REAL"},
    {"package": "com.indusind.mobile", "app_name": "IndusMobile", "developer": "IndusInd Bank", "rating": 4.2, "reviews": 300_000, "downloads": "5M+", "status": "REAL"},
    {"package": "com.yesbank.mobile", "app_name": "Yes Bank Mobile", "developer": "Yes Bank Ltd", "rating": 4.0, "reviews": 400_000, "downloads": "5M+", "status": "REAL"},
    {"package": "com.pnb.mobile", "app_name": "Punjab National Bank ONE", "developer": "PNB", "rating": 3.7, "reviews": 600_000, "downloads": "10M+", "status": "REAL"},
    {"package": "com.unionbank.vyom", "app_name": "Union Bank Vyom", "developer": "Union Bank of India", "rating": 4.0, "reviews": 350_000, "downloads": "10M+", "status": "REAL"},
    {"package": "com.fed.mobile", "app_name": "Federal Bank FedMobile", "developer": "Federal Bank", "rating": 4.4, "reviews": 350_000, "downloads": "5M+", "status": "REAL"},
    {"package": "com.canara.mobile", "app_name": "Canara ai1", "developer": "Canara Bank", "rating": 3.8, "reviews": 420_000, "downloads": "10M+", "status": "REAL"},
    {"package": "com.boi.mobile", "app_name": "Bank of India BOI Mobile", "developer": "Bank of India", "rating": 3.8, "reviews": 300_000, "downloads": "5M+", "status": "REAL"},
    {"package": "com.idbi.bank.mobile", "app_name": "IDBI Go Mobile+", "developer": "IDBI Bank", "rating": 3.6, "reviews": 200_000, "downloads": "5M+", "status": "REAL"},
    {"package": "com.au.bank", "app_name": "AU 0101", "developer": "AU Small Finance Bank", "rating": 4.4, "reviews": 250_000, "downloads": "5M+", "status": "REAL"},
    {"package": "com.myairtel.app", "app_name": "Airtel Thanks", "developer": "Airtel", "rating": 4.3, "reviews": 8_000_000, "downloads": "100M+", "status": "REAL"},
    {"package": "com.jio.money", "app_name": "JioMoney", "developer": "Jio Platforms", "rating": 4.2, "reviews": 1_100_000, "downloads": "50M+", "status": "REAL"},
    {"package": "com.mobikwik_new", "app_name": "MobiKwik", "developer": "MobiKwik", "rating": 4.1, "reviews": 2_000_000, "downloads": "50M+", "status": "REAL"},
    {"package": "in.amazon.mshop.android.shopping", "app_name": "Amazon Pay", "developer": "Amazon", "rating": 4.4, "reviews": 20_000_000, "downloads": "500M+", "status": "REAL"},
    {"package": "sbi.card.mobile", "app_name": "SBI Card App", "developer": "SBI Card", "rating": 4.3, "reviews": 300_000, "downloads": "10M+", "status": "REAL"},
    # ---- FAKE / SIMULATED APPS ----
    {"package": "com.sbi.yono.rewardsplus", "app_name": "YONO SBI Rewards+", "developer": "SBI Digital Rewards Ltd", "rating": 4.6, "reviews": 3200, "downloads": "10K+", "status": "FAKE"},
    {"package": "com.icici.quickpay.secureupdate", "app_name": "ICICI QuickPay Update", "developer": "ICICI Finance Update Corp", "rating": 3.1, "reviews": 800, "downloads": "5K+", "status": "FAKE"},
    {"package": "com.hdfc.loginpro", "app_name": "HDFC Secure Login Pro", "developer": "HDFC Secure Systems", "rating": 2.9, "reviews": 1200, "downloads": "2K+", "status": "FAKE"},
    {"package": "com.axis.cashback.promo", "app_name": "Axis Bank Bonus Cashback", "developer": "AxisPromo Pvt Ltd", "rating": 4.0, "reviews": 2500, "downloads": "8K+", "status": "FAKE"},
    {"package": "com.pnb.kyc.verify2025", "app_name": "PNB KYC Update 2025", "developer": "PNB Services Update Centre", "rating": 3.0, "reviews": 700, "downloads": "4K+", "status": "FAKE"},
    {"package": "com.sbi.yono.fastkyc", "app_name": "SBI YONO FastKYC", "developer": "SBI KYC Express", "rating": 3.5, "reviews": 1100, "downloads": "7K+", "status": "FAKE"},
    {"package": "com.paytm.cashback.rewardcenter", "app_name": "Paytm Cashback Center", "developer": "Paytm Promo Hub", "rating": 4.2, "reviews": 4400, "downloads": "15K+", "status": "FAKE"},
    {"package": "com.phonepe.securewallet", "app_name": "PhonePe Secure Wallet", "developer": "PhoneSecure Tech Ltd", "rating": 2.7, "reviews": 500, "downloads": "3K+", "status": "FAKE"},
    {"package": "com.federal.quickloan.instant", "app_name": "Federal QuickLoan", "developer": "FedLoan Services", "rating": 3.3, "reviews": 1600, "downloads": "9K+", "status": "FAKE"},
    {"package": "com.bharatloan.instantpro", "app_name": "BharatLoan Instant Pro", "developer": "Bharat Instant Loans", "rating": 3.8, "reviews": 2100, "downloads": "20K+", "status": "FAKE"},
    {"package": "com.sbi.refund.checker", "app_name": "SBI Instant Refund Checker", "developer": "SBI Refund Team", "rating": 3.6, "reviews": 1200, "downloads": "6K+", "status": "FAKE"},
    {"package": "com.axis.811.promo", "app_name": "Axis 811 Promo Edition", "developer": "Axis Promo Apps", "rating": 4.0, "reviews": 2300, "downloads": "10K+", "status": "FAKE"},
    {"package": "com.boi.mobile.litequick", "app_name": "BOI Mobile Lite Quick", "developer": "BOI Services Lite", "rating": 3.1, "reviews": 400, "downloads": "2K+", "status": "FAKE"},
    {"package": "com.idfc.rewardwallet", "app_name": "IDFC Reward Wallet", "developer": "IDFC Digital Rewards", "rating": 4.1, "reviews": 1900, "downloads": "12K+", "status": "FAKE"},
    {"package": "com.upi.booster.pro", "app_name": "UPI Booster Pro", "developer": "UPI Upgrade Inc", "rating": 3.9, "reviews": 2800, "downloads": "18K+", "status": "FAKE"},
    {"package": "com.gpay.cashback.max2025", "app_name": "Google Pay Cashback Max", "developer": "GPay Prize Center", "rating": 3.4, "reviews": 3200, "downloads": "11K+", "status": "FAKE"},
    {"package": "com.sbi.loan.fasttrack", "app_name": "SBI Loan FastTrack", "developer": "SBI Loan Express", "rating": 3.0, "reviews": 500, "downloads": "3K+", "status": "FAKE"},
    {"package": "com.indusbank.promovault", "app_name": "IndusBank Promo Vault", "developer": "IndusPromo Ltd", "rating": 3.8, "reviews": 1450, "downloads": "6K+", "status": "FAKE"},
    {"package": "com.au.pay.bonusapp", "app_name": "AU Pay Bonus", "developer": "AU Offers", "rating": 4.2, "reviews": 2800, "downloads": "13K+", "status": "FAKE"},
    {"package": "com.securepay.kyc.update", "app_name": "SecurePay KYC Update", "developer": "SecurePay Global", "rating": 3.5, "reviews": 1100, "downloads": "8K+", "status": "FAKE"},
    {"package": "com.phonepe.gold.rewards", "app_name": "PhonePe Gold Rewards", "developer": "PhonePe Gold Ltd", "rating": 4.1, "reviews": 2500, "downloads": "12K+", "status": "FAKE"},
    {"package": "com.loantap.lite.app", "app_name": "LoanTap Lite", "developer": "LoanTap QuickFunds", "rating": 3.6, "reviews": 1700, "downloads": "9K+", "status": "FAKE"},
    {"package": "com.axis.upi.verify", "app_name": "Axis UPI Verify", "developer": "Axis Verification Hub", "rating": 2.9, "reviews": 650, "downloads": "3K+", "status": "FAKE"},
    {"package": "com.icici.bonus.center", "app_name": "ICICI Bonus Center", "developer": "ICICI Bonus Pvt Ltd", "rating": 3.7, "reviews": 1900, "downloads": "10K+", "status": "FAKE"},
    {"package": "com.sbi.wallet.pro", "app_name": "SBI Wallet Pro", "developer": "SBI Wallet Services", "rating": 3.4, "reviews": 1200, "downloads": "5K+", "status": "FAKE"}
]

DATASET = {entry["package"].lower(): entry for entry in RAW_DATASET}


def get_playstore_info(package_name, playstore_url=None):
    """
    Get Play Store information for a package
    Checks if app exists, reviews, ratings, etc.
    
    Args:
        package_name: Package name to check
        playstore_url: Optional Play Store listing URL supplied by user
    
    Returns:
        Dictionary with Play Store analysis results
    """
    result = {
        "risk_score": 0,
        "exists_on_playstore": False,
        "rating": None,
        "review_count": 0,
        "developer": "",
        "developer_verified": True,
        "message": "",
        "provided_url": playstore_url,
        "url_package_name": None,
        "official_package_name": package_name,
        "package_match": None,
        "developer_from_url": None,
        "developer_match": None,
        "domain_verified": None
    }
    
    pkg_key = (package_name or "").lower()
    dataset_entry = DATASET.get(pkg_key)
    
    if dataset_entry:
        playstore_data = {
            "exists": True,
            "rating": dataset_entry["rating"],
            "review_count": dataset_entry["reviews"],
            "developer": dataset_entry["developer"],
            "reviews_verified": dataset_entry["status"] == "REAL" and dataset_entry["reviews"] >= 1000,
            "review_extracts": [],
            "screenshots_available": dataset_entry["status"] == "REAL",
            "official_package": pkg_key,
            "app_name": dataset_entry["app_name"],
            "downloads": dataset_entry["downloads"],
            "status": dataset_entry["status"],
        }
    else:
        playstore_data = simulate_playstore_lookup(package_name)
    
    official_developer = playstore_data.get("developer")
    result["exists_on_playstore"] = playstore_data.get("exists", True)
    result["rating"] = playstore_data.get("rating")
    result["review_count"] = playstore_data.get("review_count", 0)
    result["developer"] = official_developer
    result["developer_verified"] = bool(official_developer)
    result["official_package_name"] = playstore_data.get("official_package", package_name)
    result["reviews_verified"] = playstore_data.get("reviews_verified", False)
    result["review_extracts"] = playstore_data.get("review_extracts", [])
    result["screenshots_available"] = playstore_data.get("screenshots_available", False)
    result["app_name"] = playstore_data.get("app_name", package_name)
    result["downloads"] = playstore_data.get("downloads", "N/A")
    result["dataset_status"] = playstore_data.get("status")
    
    # If user supplied a Play Store link, verify all details
    if playstore_url:
        url_data = scrape_playstore_page(playstore_url, package_name, playstore_data.get("developer"))
        result["url_package_name"] = url_data.get("package_from_url")
        result["domain_verified"] = url_data.get("domain_verified")
        result["developer_from_url"] = url_data.get("developer_name")
        
        if url_data.get("package_from_url"):
            result["package_match"] = url_data["package_from_url"] == package_name
            if not result["package_match"]:
                result["risk_score"] += 35
                msg = "Play Store link package does not match provided package name"
                result["message"] = append_message(result["message"], msg)
        else:
            result["package_match"] = False
            result["risk_score"] += 25
            msg = "Could not extract package name from provided Play Store link"
            result["message"] = append_message(result["message"], msg)
        
        developer_match = None
        if url_data.get("developer_name") and playstore_data.get("developer"):
            official_dev = (playstore_data["developer"] or "").strip().lower()
            url_dev = url_data["developer_name"].strip().lower()
            developer_match = official_dev == url_dev and bool(official_dev)
            if not developer_match:
                result["risk_score"] += 35
                msg = "Developer name on provided link does not match official Play Store developer"
                result["message"] = append_message(result["message"], msg)
        else:
            developer_match = None
        result["developer_match"] = developer_match
        if developer_match is False or not url_data.get("developer_name"):
            result["developer_verified"] = False
        elif developer_match is True:
            result["developer_verified"] = True
        
        if url_data.get("domain_verified") is False:
            result["risk_score"] += 20
            msg = "Play Store link domain is not the official Google Play domain"
            result["message"] = append_message(result["message"], msg)
    else:
        result["developer_match"] = None
    
    if not result["developer_verified"]:
        result["developer"] = None
    
    dataset_status = playstore_data.get("status")
    if dataset_status == "FAKE":
        result["risk_score"] += 60
        result["message"] = append_message(result["message"], "Dataset labels this app as FAKE")
    
    # Risk scoring based on Play Store data
    if not result["exists_on_playstore"]:
        result["risk_score"] += 30
        result["message"] = "App not found on Google Play Store"
    elif playstore_data.get("rating") is not None:
        if playstore_data["rating"] < 3.0:
            result["risk_score"] += 20
            result["message"] = "Very low rating on Play Store"
        elif playstore_data["rating"] < 4.0:
            result["risk_score"] += 10
            result["message"] = "Below average rating"
        else:
            result["message"] = "App has good ratings"
        
        if playstore_data["review_count"] < 1000:
            result["risk_score"] += 20
            if result["message"]:
                result["message"] += " and insufficient reviews"
            else:
                result["message"] = "Insufficient reviews (need 1000+ for safety verification)"
        
        if not playstore_data.get("reviews_verified", False):
            result["risk_score"] += 25
            if result["message"]:
                result["message"] += " - reviews may be fake"
            else:
                result["message"] = "Reviews appear to be fake or unverified"
    else:
        result["message"] = "Play Store data unavailable"
    
    # Check developer name for suspicious patterns
    if playstore_data.get("developer"):
        dev_lower = playstore_data["developer"].lower()
        if any(susp in dev_lower for susp in ['unknown', 'test', 'developer', 'app', 'promo', 'services', 'hub']):
            result["risk_score"] += 15
            if result["message"]:
                result["message"] += " (suspicious developer name)"
    
    return result


def append_message(existing, new_msg):
    if not existing:
        return new_msg
    if new_msg.lower() in existing.lower():
        return existing
    return f"{existing}. {new_msg}"


def extract_package_from_url(playstore_url, depth=0):
    """Extract package name from a Google Play URL or share link if possible."""
    if not playstore_url or depth > 2:
        return None
    decoded = unquote(playstore_url.strip())
    parsed = urlparse(decoded)
    query_params = parse_qs(parsed.query)
    # Handle links wrapped in Google shorteners (?link=...)
    if 'link' in query_params:
        return extract_package_from_url(query_params['link'][0], depth + 1)
    if "id" in query_params:
        return query_params["id"][0]
    # Fallback: look for details?id= segment (case-insensitive)
    match = re.search(r'details\?[^ ]*id=([A-Za-z0-9_\.]+)', decoded, re.IGNORECASE)
    if match:
        return match.group(1)
    # Handle already clean package names
    if re.fullmatch(r'[A-Za-z0-9_\.]+', decoded):
        return decoded
    return None


def scrape_playstore_page(playstore_url, fallback_package, official_developer):
    """
    Simulate scraping of the supplied Play Store link.
    Ensures that the URL points to the official domain and extracts developer info.
    """
    data = {
        "page_exists": False,
        "domain_verified": None,
        "package_from_url": None,
        "developer_name": None,
    }
    
    if not playstore_url:
        return data
    
    parsed = urlparse(playstore_url)
    host = parsed.netloc.lower()
    package_from_url = extract_package_from_url(playstore_url) or fallback_package
    data["package_from_url"] = package_from_url
    data["page_exists"] = True
    
    if host.endswith("play.google.com"):
        data["domain_verified"] = True
        # Simulate scenario where malicious actors manipulate page (keywords in URL)
        if any(keyword in playstore_url.lower() for keyword in ["spoof", "fake", "clone"]):
            data["developer_name"] = "Suspicious Mirror Developer"
        else:
            data["developer_name"] = official_developer
    else:
        data["domain_verified"] = False
        if any(keyword in host for keyword in ["fake", "clone", "mirror", "apk", "download"]):
            data["developer_name"] = "Unverified / Suspicious Developer"
        else:
            data["developer_name"] = "Unknown Web Listing"
    
    return data


def simulate_playstore_lookup(package_name):
    """
    Simulate looking up an app on Play Store
    In real implementation, use Google Play Store API
    
    Returns mock data based on package name patterns
    Includes review extracts and screenshot simulation
    """
    package_lower = package_name.lower()
    
    # Simulate different scenarios
    data = {
        "exists": True,
        "rating": 4.5,
        "review_count": 5000,
        "developer": "Legitimate App Developer",
        "reviews_verified": True,
        "review_extracts": [],
        "screenshots_available": True,
        "official_package": package_name.lower(),
        "app_name": package_name,
        "downloads": "1M+",
        "status": "SIMULATED",
    }
    
    # Fake apps often don't exist or have bad data
    if any(pattern in package_lower for pattern in ['fake', 'clone', 'test', 'demo']):
        data["exists"] = False
        data["rating"] = None
        data["review_count"] = 0
        data["developer"] = "Unknown Developer"
        data["reviews_verified"] = False
        data["review_extracts"] = []
        data["screenshots_available"] = False
    elif any(pattern in package_lower for pattern in ['loan', 'cash', 'money']):
        # Some loan apps might exist but have issues
        if len(package_name) < 15:
            data["rating"] = 2.5
            data["review_count"] = 50
            data["developer"] = "App Developer"
            data["reviews_verified"] = False  # Suspicious reviews
            data["review_extracts"] = [
                "This app is a scam!",
                "Don't download, it's fake",
                "Took my money and ran"
            ]
            data["screenshots_available"] = True
        else:
            # Legitimate-looking ones
            data["rating"] = 4.2
            data["review_count"] = 10000
            data["developer"] = "Trusted Financial Services"
            data["reviews_verified"] = True
            data["review_extracts"] = [
                "Great app, works perfectly",
                "Safe and secure, highly recommend",
                "Legitimate service, no issues"
            ]
            data["screenshots_available"] = True
    else:
        # Default: app exists with decent ratings
        data["rating"] = 4.0
        data["review_count"] = 2000
        data["reviews_verified"] = True
        data["review_extracts"] = [
            "Good app overall",
            "Works as expected",
            "No complaints"
        ]
        data["screenshots_available"] = True
    
    return data

