BroIsThisFake
=============

BroIsThisFake is a banking-app safety lab for Pixel Pitch 2025. It checks Android banking, UPI, cashback, and “support” apps for the usual red flags: sketchy permissions, Play Store mismatches, developer spoofing, and malware-style behavior. The UI includes a dashboard, analyzer, requested-permissions guide, and history view that mirrors the detection feed.

Key capabilities
----------------
- Upload APKs up to **300 MB** or type package names (with optional Play Store link).
- Dataset-backed Play Store lookups so every rating/review/download value matches the judges’ spreadsheet.
- Permission, package-similarity, Play Store, and malware scans run in one pass; the app is only marked SAFE if it passes every rule.
- Evidence kit auto-builds Gmail takedown drafts and highlights developer history.
- Detection feed plus local cache keeps the history page alive even if the backend restarts.
- Dashboard calls out the workflow, strict checklist, and the Team 404 Not Found credit.

Dataset reference (for judges)
-----------------------------
All Play Store signals come straight from the mock dataset below (25 real + 25 fake apps). Fake entries look polished but are flagged as FAKE internally, so the risk score lines up with your labels.

### Real banking / UPI apps

| # | App Name | Developer | Package | Rating | Reviews | Downloads |
|---|----------|-----------|---------|--------|---------|-----------|
|1|YONO SBI|State Bank of India|in.sbi.lotus|4.0|10,000,000|100M+|
|2|HDFC Bank MobileBanking|HDFC Bank Ltd|com.hdfcbank.mobilebanking|4.1|5,200,000|50M+|
|3|ICICI iMobile Pay|ICICI Bank Ltd|com.icici.bank.imobile|4.2|4,800,000|50M+|
|4|Kotak 811 & Mobile Banking|Kotak Mahindra Bank|com.kmb.banking|4.1|1,200,000|10M+|
|5|Axis Bank Mobile App|Axis Bank Ltd|com.axis.mobile|4.0|1,400,000|10M+|
|6|Bank of Baroda M-Connect+|Bank of Baroda|com.bob.mobile|3.8|900,000|10M+|
|7|IDFC FIRST MobileBanking|IDFC FIRST Bank|com.idfcfirstbank.mobile|4.3|500,000|10M+|
|8|Paytm|Paytm Mobile Solutions|net.one97.paytm|4.5|17,000,000|500M+|
|9|PhonePe|PhonePe Pvt Ltd|com.phonepe.app|4.5|40,000,000|500M+|
|10|Google Pay (GPay)|Google LLC|com.google.android.apps.nbu.paisa.user|4.3|12,000,000|500M+|
|11|BHIM UPI|NPCI|in.org.npci.upiapp|4.3|900,000|50M+|
|12|IndusMobile|IndusInd Bank|com.indusind.mobile|4.2|300,000|5M+|
|13|Yes Bank Mobile|Yes Bank Ltd|com.yesbank.mobile|4.0|400,000|5M+|
|14|Punjab National Bank ONE|PNB|com.pnb.mobile|3.7|600,000|10M+|
|15|Union Bank Vyom|Union Bank of India|com.unionbank.vyom|4.0|350,000|10M+|
|16|Federal Bank FedMobile|Federal Bank|com.fed.mobile|4.4|350,000|5M+|
|17|Canara ai1|Canara Bank|com.canara.mobile|3.8|420,000|10M+|
|18|Bank of India BOI Mobile|Bank of India|com.boi.mobile|3.8|300,000|5M+|
|19|IDBI Go Mobile+|IDBI Bank|com.idbi.bank.mobile|3.6|200,000|5M+|
|20|AU 0101|AU Small Finance Bank|com.au.bank|4.4|250,000|5M+|
|21|Airtel Thanks|Airtel|com.myairtel.app|4.3|8,000,000|100M+|
|22|JioMoney|Jio Platforms|com.jio.money|4.2|1,100,000|50M+|
|23|MobiKwik|MobiKwik|com.mobikwik_new|4.1|2,000,000|50M+|
|24|Amazon Pay|Amazon|in.amazon.mShop.android.shopping|4.4|20,000,000|500M+|
|25|SBI Card App|SBI Card|sbi.card.mobile|4.3|300,000|10M+|

### Simulated fake/malicious apps

| # | App Name | Developer | Package | Rating | Reviews | Downloads |
|---|----------|-----------|---------|--------|---------|-----------|
|1|YONO SBI Rewards+|SBI Digital Rewards Ltd|com.sbi.yono.rewardsplus|4.6|3,200|10K+|
|2|ICICI QuickPay Update|ICICI Finance Update Corp|com.icici.quickpay.secureupdate|3.1|800|5K+|
|3|HDFC Secure Login Pro|HDFC Secure Systems|com.hdfc.loginpro|2.9|1,200|2K+|
|4|Axis Bank Bonus Cashback|AxisPromo Pvt Ltd|com.axis.cashback.promo|4.0|2,500|8K+|
|5|PNB KYC Update 2025|PNB Services Update Centre|com.pnb.kyc.verify2025|3.0|700|4K+|
|6|SBI YONO FastKYC|SBI KYC Express|com.sbi.yono.fastkyc|3.5|1,100|7K+|
|7|Paytm Cashback Center|Paytm Promo Hub|com.paytm.cashback.rewardcenter|4.2|4,400|15K+|
|8|PhonePe Secure Wallet|PhoneSecure Tech Ltd|com.phonepe.securewallet|2.7|500|3K+|
|9|Federal QuickLoan|FedLoan Services|com.federal.quickloan.instant|3.3|1,600|9K+|
|10|BharatLoan Instant Pro|Bharat Instant Loans|com.bharatloan.instantpro|3.8|2,100|20K+|
|11|SBI Instant Refund Checker|SBI Refund Team|com.sbi.refund.checker|3.6|1,200|6K+|
|12|Axis 811 Promo Edition|Axis Promo Apps|com.axis.811.promo|4.0|2,300|10K+|
|13|BOI Mobile Lite Quick|BOI Services Lite|com.boi.mobile.litequick|3.1|400|2K+|
|14|IDFC Reward Wallet|IDFC Digital Rewards|com.idfc.rewardwallet|4.1|1,900|12K+|
|15|UPI Booster Pro|UPI Upgrade Inc|com.upi.booster.pro|3.9|2,800|18K+|
|16|Google Pay Cashback Max|GPay Prize Center|com.gpay.cashback.max2025|3.4|3,200|11K+|
|17|SBI Loan FastTrack|SBI Loan Express|com.sbi.loan.fasttrack|3.0|500|3K+|
|18|IndusBank Promo Vault|IndusPromo Ltd|com.indusbank.promovault|3.8|1,450|6K+|
|19|AU Pay Bonus|AU Offers|com.au.pay.bonusapp|4.2|2,800|13K+|
|20|SecurePay KYC Update|SecurePay Global|com.securepay.kyc.update|3.5|1,100|8K+|
|21|PhonePe Gold Rewards|PhonePe Gold Ltd|com.phonepe.gold.rewards|4.1|2,500|12K+|
|22|LoanTap Lite|LoanTap QuickFunds|com.loantap.lite.app|3.6|1,700|9K+|
|23|Axis UPI Verify|Axis Verification Hub|com.axis.upi.verify|2.9|650|3K+|
|24|ICICI Bonus Center|ICICI Bonus Pvt Ltd|com.icici.bonus.center|3.7|1,900|10K+|
|25|SBI Wallet Pro|SBI Wallet Services|com.sbi.wallet.pro|3.4|1,200|5K+|

Project structure
-----------------
```
BroIsThisFake/
├── backend/
│   ├── app.py                    # Flask API + scoring + DB + takedown emails
│   ├── detectors/
│   │   ├── permissions.py        # Permission heuristics
│   │   ├── package_similarity.py # Clone + typosquat checks
│   │   ├── playstore_scraper.py  # Dataset-aware Play Store lookup
│   │   └── malware_scanner.py    # Suspicious behavior simulation
│   ├── utils/
│   │   ├── db.py                 # SQLite helpers
│   │   └── helpers.py
│   └── requirements.txt
├── frontend/
│   ├── dashboard.html            # Landing page
│   ├── index.html                # Analyzer
│   ├── history.html              # Detection feed + history
│   ├── permissions.html          # Requested-permissions guide
│   ├── app.js                    # Frontend logic
│   └── styles.css                # Liquid glass theme
├── frontend-react/               # Optional React/Tailwind prototype
├── README.md
├── CUSTOMIZATION_GUIDE.md
└── BACKEND_CUSTOMIZATION_GUIDE.md
```

Running the project
-------------------
**Backend**
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python app.py` (runs on `http://127.0.0.1:5000`)

**Frontend (vanilla)**
1. `cd frontend`
2. `python -m http.server 8000`
3. Open `http://localhost:8000/dashboard.html`

Usage tips
----------
- Analyzer accepts either an APK upload or package name plus optional Play Store link. If you only have the link, paste it; the backend extracts the package and developer.
- History page combines backend results with a local cache so you can demo offline.
- Permissions page lists the dangerous vs safe permission categories for quick reference.
- Evidence kit shows the Gmail message that would go to Play Support with all the gathered proof.

How scoring works
-----------------
1. **Collect inputs** – Package name or APK metadata plus an optional Play Store link.
2. **Match dataset** – Look up the package in the 50-row table above; if it is labeled FAKE we stop trusting any Play Store claims from the app.
3. **Run detectors** – Permissions, package similarity, malware scan, and Play Store verification each add to the risk score.
4. **Apply the safety checklist** – An app is only marked SAFE when it exists on Play Store, has ≥4.0 rating, ≥1000 verified reviews, a trusted developer name, zero suspicious permissions, and zero malware findings.
5. **Store & explain** – Results go into SQLite + local storage, the detection feed, and the Gmail evidence kit so you can explain every decision on stage.

Troubleshooting
---------------
- **Backend busy**: change the port in `backend/app.py` (`app.run(... port=5000)`).
- **Frontend can’t reach backend**: restart Flask, verify it’s still on localhost:5000, refresh the browser.
- **APK upload fails**: confirm `.apk` extension and ≤ 300 MB size; otherwise use package name mode.
- **History empty**: run a scan first; the local cache stores up to 50 entries.

Learning notes
--------------
This repo is meant for first-year students, so the detectors are lightweight. In production you’d plug in real APK parsing (aapt/apktool), Play Store API calls, signed certificate checks, and stronger telemetry. Treat this as a sandbox for demonstrating how multi-layer vetting works.

Next steps
----------
- Hook in real APK parsing and Play Store APIs.
- Export evidence kit as PDF/CSV for investigators.
- Add batch scanning for lists of suspicious packages.
- Finish the React/Tailwind frontend once Node.js is available.

License / note
--------------
Educational use only. Always confirm suspicious apps with official bank advisories. Built by **Team 404 Not Found** for Pixel Pitch 2025.

