// Main JavaScript for BroIsThisFake (fake banking app detector)
// Handles API calls and UI updates

const API_BASE_URL = 'http://localhost:5000';

// Check for package name in URL params (from history page)
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const packageName = urlParams.get('package');
    if (packageName) {
        document.getElementById('packageInput').value = packageName;
        switchTab('package');
    }
});

// Tab switching
function switchTab(tab) {
    // Hide all tabs
    document.getElementById('apk-tab').classList.remove('active');
    document.getElementById('package-tab').classList.remove('active');
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    if (tab === 'apk') {
        document.getElementById('apk-tab').classList.add('active');
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
    } else {
        document.getElementById('package-tab').classList.add('active');
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
    }
    
    // Hide results when switching tabs
    document.getElementById('results').style.display = 'none';
}

// Setup file upload
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('apkFile');
    const fileName = document.getElementById('fileName');
    
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.background = 'rgba(255, 255, 255, 0.25)';
        uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.6)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.background = 'rgba(255, 255, 255, 0.15)';
        uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.4)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.background = 'rgba(255, 255, 255, 0.15)';
        uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.4)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].name.endsWith('.apk')) {
            fileInput.files = files;
            fileName.textContent = `Selected: ${files[0].name}`;
        } else {
            alert('Please upload a valid APK file');
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileName.textContent = `Selected: ${e.target.files[0].name}`;
        }
    });
});

// Analyze APK file
async function analyzeAPK() {
    const fileInput = document.getElementById('apkFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select an APK file first');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze_apk`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            alert('Error: ' + (data.error || 'Failed to analyze APK'));
        }
    } catch (error) {
        alert('Error connecting to server. Make sure the backend is running on port 5000.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Analyze package name
async function analyzePackage() {
    const packageInput = document.getElementById('packageInput');
    const playstoreUrlInput = document.getElementById('playstoreUrlInput');
    const packageName = packageInput.value.trim();
    const playstoreUrl = playstoreUrlInput ? playstoreUrlInput.value.trim() : '';
    
    if (!packageName && !playstoreUrl) {
        alert('Please enter a package name or provide a Play Store link');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze_package`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                package_name: packageName,
                playstore_url: playstoreUrl || null
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            alert('Error: ' + (data.error || 'Failed to analyze package'));
        }
    } catch (error) {
        alert('Error connecting to server. Make sure the backend is running on port 5000.');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Display analysis results
function displayResults(data) {
    const resultsSection = document.getElementById('results');
    resultsSection.style.display = 'block';
    
    // Persist latest analysis locally so History page can mirror detection feed instantly
    persistLocalHistory(data);
    
    // Update package info with strict safety check
    document.getElementById('resultPackage').textContent = data.package_name || '-';
    
    // Use is_safe flag if available, otherwise fallback to is_fake
    const isSafe = data.is_safe === true;
    const statusEl = document.getElementById('resultStatus');
    
    if (isSafe) {
        statusEl.textContent = '✅ VERIFIED SAFE - Passed All Security Checks';
        statusEl.style.color = '#00aa00';
    } else if (data.is_fake) {
        statusEl.textContent = '⚠️ UNSAFE - Failed Security Checks';
        statusEl.style.color = '#cc0000';
    } else {
        statusEl.textContent = '⚠️ POTENTIALLY UNSAFE - Did Not Pass All Safety Criteria';
        statusEl.style.color = '#ff8800';
    }
    
    // Update risk badge with enhanced display
    const riskBadge = document.getElementById('riskBadge');
    const riskScore = data.risk_score || 0;
    const riskLevel = data.risk_level || 'LOW';
    
    riskBadge.className = 'risk-badge ' + riskLevel;
    document.getElementById('riskLevel').textContent = riskLevel;
    document.getElementById('riskScore').textContent = `Risk Score: ${riskScore}/100`;
    document.getElementById('riskPercentage').textContent = `${riskScore}%`;
    
    // Update progress bar
    const progressFill = document.getElementById('riskProgressFill');
    progressFill.style.width = `${riskScore}%`;
    
    // Update progress bar color based on risk level
    if (riskScore >= 70) {
        progressFill.style.backgroundColor = '#ff4444';
    } else if (riskScore >= 50) {
        progressFill.style.backgroundColor = '#ff8800';
    } else {
        progressFill.style.backgroundColor = '#44ff44';
    }
    
    // Update score breakdown (including malware)
    const permScore = data.checks?.permissions?.risk_score || 0;
    const similarityScore = data.checks?.package_similarity?.risk_score || 0;
    const playstoreScore = data.checks?.playstore?.risk_score || 0;
    const malwareScore = data.checks?.malware?.risk_score || 0;
    
    document.getElementById('permScore').textContent = `+${permScore}`;
    document.getElementById('similarityScore').textContent = `+${similarityScore}`;
    document.getElementById('playstoreScore').textContent = `+${playstoreScore}`;
    
    // Add malware score if breakdown exists
    const breakdown = document.getElementById('riskBreakdown');
    let malwareBreakdown = breakdown.querySelector('#malwareScore');
    if (!malwareBreakdown && malwareScore > 0) {
        const malwareItem = document.createElement('div');
        malwareItem.className = 'breakdown-item';
        malwareItem.id = 'malwareScoreItem';
        malwareItem.innerHTML = `
            <span>Malware Scan:</span>
            <span id="malwareScore">+${malwareScore}</span>
        `;
        breakdown.appendChild(malwareItem);
    } else if (malwareBreakdown) {
        malwareBreakdown.textContent = `+${malwareScore}`;
    }

    // App type and developer disclaimer
    document.getElementById('appType').textContent = data.app_type || 'Not classified';
    const disclaimerEl = document.getElementById('developerDisclaimer');
    if (data.developer_warning && data.developer_disclaimer) {
        disclaimerEl.textContent = data.developer_disclaimer;
        disclaimerEl.style.display = 'block';
    } else {
        disclaimerEl.style.display = 'none';
    }

    // Evidence kit: takedown email
    if (data.takedown_email) {
        const subject = data.takedown_email.subject || '';
        const body = data.takedown_email.body || '';
        document.getElementById('emailSubject').value = subject;
        document.getElementById('emailBody').value = body;

        const gmailLink = document.getElementById('gmailLink');
        const subjectEnc = encodeURIComponent(subject);
        const bodyEnc = encodeURIComponent(body);
        // Google Play developer support email can be customised if needed
        gmailLink.href = `https://mail.google.com/mail/?view=cm&fs=1&to=play-developer-support@google.com&su=${subjectEnc}&body=${bodyEnc}`;
    }

    // Detection feed
    const feedList = document.getElementById('feedList');
    feedList.innerHTML = '';
    if (data.detection_feed && Array.isArray(data.detection_feed) && data.detection_feed.length > 0) {
        data.detection_feed.forEach(item => {
            const div = document.createElement('div');
            div.className = 'feed-item';

            const header = document.createElement('div');
            header.className = 'feed-item-header';
            const nameSpan = document.createElement('span');
            nameSpan.textContent = item.package_name || '-';
            const chip = document.createElement('span');
            chip.className = `feed-chip ${item.risk_level || 'LOW'}`;
            chip.textContent = item.risk_level || 'LOW';
            header.appendChild(nameSpan);
            header.appendChild(chip);

            const meta = document.createElement('div');
            meta.className = 'feed-item-meta';
            const scoreSpan = document.createElement('span');
            scoreSpan.textContent = `Score: ${item.risk_score || 0}/100`;
            const typeSpan = document.createElement('span');
            typeSpan.textContent = item.app_type || 'Unknown';
            meta.appendChild(scoreSpan);
            meta.appendChild(typeSpan);

            div.appendChild(header);
            div.appendChild(meta);
            feedList.appendChild(div);
        });
    } else {
        const empty = document.createElement('p');
        empty.textContent = 'No previous analyses stored yet.';
        empty.style.fontSize = '0.85em';
        empty.style.color = '#666';
        feedList.appendChild(empty);
    }

    // Already-flagged popup
    if (data.already_flagged) {
        const popup = document.getElementById('flaggedPopup');
        const msg = document.getElementById('flaggedMessage');
        const prev = data.previous_analysis || {};
        const prevScore = prev.risk_score ?? '?';
        const prevLevel = prev.risk_level || 'UNKNOWN';
        const when = prev.first_flagged_at || 'an earlier scan';
        msg.textContent = `This app was already flagged as malicious during ${when} with a risk score of ${prevScore} (${prevLevel}).`;
        popup.style.display = 'flex';
    }
    
    // Update permissions check
    if (data.checks && data.checks.permissions) {
        const perm = data.checks.permissions;
        document.getElementById('permResult').textContent = perm.message || '-';
        const permList = document.getElementById('permList');
        permList.innerHTML = '';
        if (perm.suspicious_permissions && perm.suspicious_permissions.length > 0) {
            perm.suspicious_permissions.forEach(p => {
                const li = document.createElement('li');
                li.textContent = p;
                permList.appendChild(li);
            });
        } else {
            permList.innerHTML = '<li>No suspicious permissions found</li>';
        }
    }
    
    // Update similarity check
    if (data.checks && data.checks.package_similarity) {
        const sim = data.checks.package_similarity;
        document.getElementById('similarityResult').textContent = sim.message || '-';
        const simList = document.getElementById('similarityList');
        simList.innerHTML = '';
        if (sim.similar_apps && sim.similar_apps.length > 0) {
            sim.similar_apps.forEach(app => {
                const li = document.createElement('li');
                li.textContent = `${app.package} (${app.similarity}% similar)`;
                simList.appendChild(li);
            });
        } else {
            simList.innerHTML = '<li>No similar apps found</li>';
        }
    }
    
    // Update malware check
    if (data.checks && data.checks.malware) {
        const malware = data.checks.malware;
        const malwareResult = document.getElementById('malwareResult');
        const malwareList = document.getElementById('malwareList');
        const malwareDetails = document.getElementById('malwareDetails');
        
        if (malwareResult) {
            malwareResult.textContent = malware.message || '-';
        }
        
        if (malwareList) {
            malwareList.innerHTML = '';
            if (malware.threats_found && malware.threats_found.length > 0) {
                malware.threats_found.forEach(threat => {
                    const li = document.createElement('li');
                    li.style.color = '#ff4444';
                    li.textContent = `⚠️ ${threat}`;
                    malwareList.appendChild(li);
                });
            }
            if (malware.security_issues && malware.security_issues.length > 0) {
                malware.security_issues.forEach(issue => {
                    const li = document.createElement('li');
                    li.style.color = '#ff8800';
                    li.textContent = `⚠️ ${issue}`;
                    malwareList.appendChild(li);
                });
            }
            if ((!malware.threats_found || malware.threats_found.length === 0) && 
                (!malware.security_issues || malware.security_issues.length === 0)) {
                malwareList.innerHTML = '<li style="color: #44ff44;">✅ No malware or security issues detected</li>';
            }
        }
        
        if (malwareDetails && malware.scan_details) {
            malwareDetails.innerHTML = '<p><strong>Scan Details:</strong></p>';
            Object.entries(malware.scan_details).forEach(([key, value]) => {
                malwareDetails.innerHTML += `<p>${key.replace('_', ' ').toUpperCase()}: ${value}</p>`;
            });
        }
    }
    
    // Update Play Store check with review extracts and screenshots
    if (data.checks && data.checks.playstore) {
        const ps = data.checks.playstore;
        document.getElementById('playstoreResult').textContent = ps.message || '-';
        const psDetails = document.getElementById('playstoreDetails');
        const reviewExtracts = document.getElementById('reviewExtracts');
        const screenshotsInfo = document.getElementById('screenshotsInfo');
        const packageMatchStatus = document.getElementById('packageMatchStatus');
        const developerMatchStatus = document.getElementById('developerMatchStatus');
        
        psDetails.innerHTML = '';
        
        if (ps.exists_on_playstore) {
            psDetails.innerHTML += `<p><strong>Rating:</strong> ${ps.rating ? ps.rating + '/5.0' : 'N/A'}</p>`;
            psDetails.innerHTML += `<p><strong>Reviews:</strong> ${ps.review_count || 0} ${ps.reviews_verified ? '(Verified)' : '(Unverified)'}</p>`;
            psDetails.innerHTML += `<p><strong>Developer:</strong> ${ps.developer || 'Unknown'}</p>`;
            if (ps.official_package_name) {
                psDetails.innerHTML += `<p><strong>Official Package:</strong> ${ps.official_package_name}</p>`;
            }
            if (ps.url_package_name) {
                psDetails.innerHTML += `<p><strong>URL Package:</strong> ${ps.url_package_name}</p>`;
            }
            psDetails.innerHTML += `<p><strong>Play Store Status:</strong> <span style="color: #44ff44;">✅ Verified</span></p>`;
            
            // Package match flag
            if (packageMatchStatus) {
                if (ps.package_match === false) {
                    packageMatchStatus.textContent = '❌ Mismatch detected';
                    packageMatchStatus.className = 'match-badge bad';
                } else if (ps.package_match === true) {
                    packageMatchStatus.textContent = '✅ Exact match';
                    packageMatchStatus.className = 'match-badge ok';
                } else {
                    packageMatchStatus.textContent = 'Unknown (no link provided)';
                    packageMatchStatus.className = 'match-badge warn';
                }
            }
            
            // Developer match flag
            if (developerMatchStatus) {
                if (ps.developer_match === false) {
                    developerMatchStatus.textContent = `❌ Mismatch (link developer: ${ps.developer_from_url || 'Unknown'})`;
                    developerMatchStatus.className = 'match-badge bad';
                } else if (ps.developer_match === true) {
                    developerMatchStatus.textContent = '✅ Developer matches official listing';
                    developerMatchStatus.className = 'match-badge ok';
                } else {
                    developerMatchStatus.textContent = 'Unknown (no link provided)';
                    developerMatchStatus.className = 'match-badge warn';
                }
            }
            
            // Review extracts
            if (reviewExtracts && ps.review_extracts && ps.review_extracts.length > 0) {
                reviewExtracts.innerHTML = '<h5>Review Extracts:</h5><div class="review-list">';
                ps.review_extracts.forEach(review => {
                    reviewExtracts.innerHTML += `<div class="review-item glass-card">"${review}"</div>`;
                });
                reviewExtracts.innerHTML += '</div>';
            } else if (reviewExtracts) {
                reviewExtracts.innerHTML = '<p style="color: #999; font-size: 0.9em;">No review extracts available</p>';
            }
            
            // Screenshots info
            if (screenshotsInfo) {
                if (ps.screenshots_available) {
                    screenshotsInfo.innerHTML = '<h5>Screenshots:</h5><p style="color: #44ff44;">✅ Screenshots available on Play Store</p>';
                } else {
                    screenshotsInfo.innerHTML = '<h5>Screenshots:</h5><p style="color: #ff8800;">⚠️ Screenshots not available</p>';
                }
            }
        } else {
            psDetails.innerHTML = '<p style="color: #cc0000;">❌ App not found on Play Store</p>';
            if (reviewExtracts) reviewExtracts.innerHTML = '';
            if (screenshotsInfo) screenshotsInfo.innerHTML = '<p style="color: #cc0000;">❌ Screenshots not available (app not on Play Store)</p>';
            if (packageMatchStatus) {
                packageMatchStatus.textContent = '❌ Play Store listing missing';
                packageMatchStatus.className = 'match-badge bad';
            }
            if (developerMatchStatus) {
                developerMatchStatus.textContent = '❌ Unable to verify developer';
                developerMatchStatus.className = 'match-badge bad';
            }
        }
    }
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function persistLocalHistory(entry) {
    if (!entry || !entry.package_name) {
        return;
    }

    const historyKey = 'bro_is_this_fake_history';
    const existing = JSON.parse(localStorage.getItem(historyKey) || '[]');
    
    const sanitized = {
        package_name: entry.package_name,
        developer: entry.checks?.playstore?.developer || null,
        app_type: entry.app_type || 'Unknown',
        risk_score: entry.risk_score || 0,
        risk_level: entry.risk_level || 'LOW',
        is_fake: !!entry.is_fake,
        flagged_malicious: entry.already_flagged ? 1 : (entry.is_fake ? 1 : 0),
        created_at: new Date().toISOString(),
    };

    const updated = [sanitized, ...existing.filter(item => item.package_name !== sanitized.package_name)];
    localStorage.setItem(historyKey, JSON.stringify(updated.slice(0, 50)));
}

// Show loading spinner
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

// Hide loading spinner
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Reset analysis
function resetAnalysis() {
    document.getElementById('results').style.display = 'none';
    document.getElementById('apkFile').value = '';
    document.getElementById('fileName').textContent = '';
    document.getElementById('packageInput').value = '';
    const playstoreUrlInput = document.getElementById('playstoreUrlInput');
    if (playstoreUrlInput) {
        playstoreUrlInput.value = '';
    }
}

// Copy takedown email body to clipboard
function copyTakedownEmail() {
    const body = document.getElementById('emailBody').value;
    if (!body) return;
    navigator.clipboard.writeText(body).then(() => {
        alert('Takedown email copied to clipboard.');
    }).catch(() => {
        alert('Unable to copy email. Please select and copy manually.');
    });
}

// Close already-flagged popup
function closeFlaggedPopup() {
    document.getElementById('flaggedPopup').style.display = 'none';
}

