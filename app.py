from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from detectors.permissions import check_permissions
from detectors.package_similarity import check_package_similarity
from detectors.playstore_scraper import get_playstore_info, extract_package_from_url
from detectors.malware_scanner import scan_for_malware
from utils.helpers import extract_package_name_from_apk
from utils.db import (
    init_db,
    save_analysis,
    get_app,
    get_recent_analyses,
    get_developer_stats,
)

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# Store uploaded files temporarily
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024  # 300MB max file size

# Make sure database tables exist
init_db()


@app.route('/')
def home():
    return jsonify({"status": "BroIsThisFake API is running!"})


@app.route('/analyze_apk', methods=['POST'])
def analyze_apk():
    """
    Analyze an uploaded APK file
    Returns detection results for fake banking apps (loan, cashback, support, UPI, etc.)
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Extract package name (simplified - in real app would use aapt or similar)
        package_name = extract_package_name_from_apk(filepath)
        
        # Run all detection checks
        results = run_detection_checks(package_name, filepath, None)

        # Enrich with DB info and takedown email template
        results = post_process_results(results)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/analyze_package', methods=['POST'])
def analyze_package():
    """
    Analyze an app by package name only
    Useful when the user only knows the package name
    """
    try:
        data = request.get_json() or {}
        
        package_name = (data.get('package_name') or '').strip()
        playstore_url = (data.get('playstore_url') or '').strip()
        
        if not package_name and playstore_url:
            inferred_package = extract_package_from_url(playstore_url)
            if not inferred_package:
                return jsonify({"error": "Unable to extract package name from the Play Store link"}), 400
            package_name = inferred_package
        
        if not package_name:
            return jsonify({"error": "Package name or a valid Play Store link is required"}), 400
        
        # Run detection checks (without APK file)
        results = run_detection_checks(package_name, None, playstore_url or None)

        # Enrich with DB info and takedown email template
        results = post_process_results(results)

        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_detection_checks(package_name, apk_path=None, playstore_url=None):
    """
    Run all detection algorithms on the app
    Returns combined results from all detectors
    """
    results = {
        "package_name": package_name,
        "risk_score": 0,
        "is_fake": False,
        "checks": {}
    }

    # Check 1: Suspicious permissions
    perm_results = check_permissions(package_name, apk_path)
    results["checks"]["permissions"] = perm_results
    results["risk_score"] += perm_results.get("risk_score", 0)
    
    # Check 2: Package name similarity (checking for fake clones)
    similarity_results = check_package_similarity(package_name)
    results["checks"]["package_similarity"] = similarity_results
    results["risk_score"] += similarity_results.get("risk_score", 0)
    
    # Check 3: Play Store metadata
    playstore_results = get_playstore_info(package_name, playstore_url)
    results["checks"]["playstore"] = playstore_results
    results["risk_score"] += playstore_results.get("risk_score", 0)
    
    # Check 4: Malware scanning
    malware_results = scan_for_malware(package_name, apk_path)
    results["checks"]["malware"] = malware_results
    results["risk_score"] += malware_results.get("risk_score", 0)
    
    # Classify app type based on name and behaviour
    results["app_type"] = classify_app_type(package_name, results["checks"])

    # STRICT SAFETY CHECK: App is ONLY safe if ALL criteria pass
    # Must pass ALL of these:
    # 1. Risk score < 20 (very low risk)
    # 2. Exists on Play Store
    # 3. Rating >= 4.0
    # 4. Review count >= 1000
    # 5. Reviews are verified/real
    # 6. No malware detected
    # 7. No suspicious permissions
    # 8. No fake patterns matched
    
    playstore = playstore_results
    permissions = perm_results
    similarity = similarity_results
    
    is_safe = (
        results["risk_score"] < 20 and
        playstore.get("exists_on_playstore", False) and
        playstore.get("rating", 0) >= 4.0 and
        playstore.get("review_count", 0) >= 1000 and
        playstore.get("reviews_verified", False) and
        not malware_results.get("malware_detected", False) and
        len(permissions.get("suspicious_permissions", [])) == 0 and
        not similarity.get("matches_fake_pattern", False)
    )
    
    # Determine if app is fake (threshold: 30+ risk score for stricter detection)
    results["is_fake"] = results["risk_score"] >= 30 or not is_safe
    results["is_safe"] = is_safe

    # Add risk level description
    if results["risk_score"] >= 70:
        results["risk_level"] = "CRITICAL"
    elif results["risk_score"] >= 50:
        results["risk_level"] = "HIGH"
    elif results["risk_score"] >= 30:
        results["risk_level"] = "MEDIUM"
    elif results["risk_score"] >= 10:
        results["risk_level"] = "LOW"
    else:
        results["risk_level"] = "SAFE"

    return results


def classify_app_type(package_name, checks):
    """
    Very simple classifier that tags the kind of risky banking app we are seeing.
    This is based mostly on keywords from the package name.

    Types we care about (as per project brief):
      - Fake loan / finance apps
      - Fake cashback apps
      - Apps collecting banking info
      - Fake help / support banking apps
      - Fake banking MOD apps
    """
    if not package_name:
        return "Unknown / Other"

    name = package_name.lower()
    tags = []

    # Fake loan / finance apps
    if any(word in name for word in ["loan", "cash", "credit", "emi"]):
        tags.append("Fake Loan / Finance App")

    # Fake cashback apps
    if any(word in name for word in ["cashback", "reward", "offers", "coupon"]):
        tags.append("Fake Cashback / Rewards App")

    # Apps collecting banking info or pretending to be banking tools
    if any(
        word in name
        for word in ["upi", "bank", "ifsc", "neft", "rtgs", "card", "pin", "wallet"]
    ):
        tags.append("Collects Banking / Payment Information")

    # Fake banking help or support
    if any(word in name for word in ["support", "help", "customer", "care", "helpline"]):
        tags.append("Fake Banking Help / Support App")

    # MOD / hacked banking apps
    if any(word in name for word in ["mod", "hack", "premium", "pro"]):
        tags.append("Fake Banking MOD / Hacked App")

    if not tags:
        return "Suspicious Banking App"

    # Join all tags into a single readable string
    return ", ".join(tags)


def build_takedown_email(results):
    """
    Build a simple email template that the user can send to report the app.
    The frontend will show this and also open Gmail with these details.
    """
    package_name = results.get("package_name", "Unknown package")
    checks = results.get("checks", {})
    playstore = checks.get("playstore", {}) or {}
    permissions = checks.get("permissions", {}) or {}
    similarity = checks.get("package_similarity", {}) or {}

    developer = (
        playstore.get("developer")
        if playstore.get("developer_verified", True)
        else None
    )
    developer_display = developer or "Unknown / Unverified developer"
    risk_score = results.get("risk_score", 0)
    risk_level = results.get("risk_level", "LOW")
    app_type = results.get("app_type", "Suspicious banking app")

    evidence_lines = []

    # Permission-based evidence
    susp_perms = permissions.get("suspicious_permissions") or []
    if susp_perms:
        evidence_lines.append(
            f"- Suspicious permissions: {', '.join(susp_perms)}"
        )

    # Similarity-based evidence
    if similarity.get("matches_fake_pattern"):
        evidence_lines.append(
            "- Package name matches known fake / clone patterns"
        )
    if similarity.get("similar_apps"):
        sim_names = [s["package"] for s in similarity["similar_apps"]]
        evidence_lines.append(
            f"- Looks similar to known financial apps: {', '.join(sim_names)}"
        )

    # Play Store evidence
    if not playstore.get("exists_on_playstore", True):
        evidence_lines.append("- App not found on Google Play Store")
    else:
        rating = playstore.get("rating")
        review_count = playstore.get("review_count")
        if rating is not None:
            evidence_lines.append(f"- Play Store rating: {rating} stars")
        if review_count is not None:
            evidence_lines.append(f"- Number of reviews: {review_count}")
        if "suspicious" in (playstore.get("message") or "").lower():
            evidence_lines.append(f"- {playstore['message']}")

    # Fallback if no evidence lines were built
    if not evidence_lines:
        evidence_lines.append("- Automated checks indicate high risk behaviour.")

    subject = f"Takedown request for suspicious app: {package_name}"

    body_lines = [
        "To,",
        "Google Play Support Team,",
        "",
        f"Subject: Takedown request for suspicious app {package_name}",
        "",
        "Dear Google Play Team,",
        "",
        f"I would like to report the app '{package_name}' (developer: {developer_display}) "
        f"which appears to be a high-risk {app_type.lower()}.",
        "",
        f"Our internal analysis tool assigned this app an overall risk score of "
        f"{risk_score}/100 ({risk_level} risk).",
        "",
        "Key evidence from the automated analysis:",
        *evidence_lines,
        "",
        "This app appears to fall into one or more of the following risky banking categories:",
        "- Fake loan / instant credit apps",
        "- Fake cashback or rewards apps",
        "- Apps attempting to collect banking / UPI credentials",
        "- Fake customer care or banking support apps",
        "- Modified (MOD) versions of banking or payment apps",
        "",
        "Please review this app at the earliest and take appropriate action "
        "to protect users from potential fraud.",
        "",
        "Regards,",
        "A concerned user",
    ]

    return {
        "subject": subject,
        "body": "\n".join(body_lines),
    }


def post_process_results(results):
    """
    After core detection is done we:
      - Check if this app was already flagged earlier
      - Store the analysis in the database
      - Compute developer history
      - Build a detection feed
      - Generate a takedown email template
    """
    package_name = results.get("package_name")
    checks = results.get("checks", {}) or {}
    playstore = checks.get("playstore", {}) or {}
    developer_verified = playstore.get("developer_verified", True)
    developer = playstore.get("developer") if developer_verified else None
    app_type = results.get("app_type", "Suspicious Banking App")

    # Look up previous record if any
    previous = get_app(package_name) if package_name else None
    already_flagged = bool(previous and previous.get("flagged_malicious"))

    results["already_flagged"] = already_flagged
    if previous:
        results["previous_analysis"] = {
            "risk_score": previous.get("risk_score"),
            "risk_level": previous.get("risk_level"),
            "first_flagged_at": previous.get("created_at"),
        }

    # Save or update this analysis in the database
    save_analysis(
        package_name=package_name,
        developer=developer,
        app_type=app_type,
        risk_score=results.get("risk_score", 0),
        risk_level=results.get("risk_level", "LOW"),
        is_fake=results.get("is_fake", False),
        checks=checks,
    )

    # Developer stats and disclaimer
    if developer:
        dev_stats = get_developer_stats(developer)
    else:
        dev_stats = {"total_apps": 0, "malicious_apps": 0}
    results["developer_stats"] = dev_stats
    results["developer_warning"] = bool(
        developer and dev_stats.get("malicious_apps", 0) >= 3
    )
    if results["developer_warning"]:
        results["developer_disclaimer"] = (
            "Warning: This developer already has multiple high-risk or "
            "malicious apps flagged in previous analyses. Treat any apps "
            "from this developer with extreme caution."
        )

    # Detection feed (simple rolling history)
    recent = get_recent_analyses(limit=10)
    results["detection_feed"] = recent

    # Auto-generated takedown email
    results["takedown_email"] = build_takedown_email(results)

    return results


if __name__ == '__main__':
    # Run on localhost, port 5000
    app.run(debug=True, port=5000)

