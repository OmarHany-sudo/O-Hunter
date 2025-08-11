import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from modules.access_control import AccessControlScanner
from modules.injection import InjectionScanner
from modules.xss import XSSScanner
from modules.crypto_failures import CryptoFailuresScanner
from modules.security_misconfiguration import SecurityMisconfigurationScanner
from modules.vulnerable_components import VulnerableComponentsScanner
from modules.authentication_failures import AuthenticationFailuresScanner
from modules.software_data_integrity import SoftwareDataIntegrityScanner
from modules.logging_monitoring import LoggingMonitoringScanner
from modules.ssrf import SSRFScanner


class Scanner:
    def __init__(self):
        self.findings = []
        self.access_control_scanner = AccessControlScanner()
        self.injection_scanner = InjectionScanner()
        self.xss_scanner = XSSScanner()
        self.crypto_failures_scanner = CryptoFailuresScanner()
        self.security_misconfiguration_scanner = SecurityMisconfigurationScanner()
        self.vulnerable_components_scanner = VulnerableComponentsScanner()
        self.authentication_failures_scanner = AuthenticationFailuresScanner()
        self.software_data_integrity_scanner = SoftwareDataIntegrityScanner()
        self.logging_monitoring_scanner = LoggingMonitoringScanner()
        self.ssrf_scanner = SSRFScanner()

    def scan_headers(self, target_url):
        print(f"Scanning headers for: {target_url}")
        try:
            response = requests.get(target_url, timeout=10)
            headers = response.headers
            # Basic check for missing security headers
            if 'X-Content-Type-Options' not in headers:
                self.findings.append({
                    'vulnerability': 'Missing X-Content-Type-Options header',
                    'severity': 'Low',
                    'evidence': f'Header not found in {target_url}',
                    'remediation': 'Ensure X-Content-Type-Options: nosniff is set to prevent MIME-sniffing vulnerabilities.'
                })
            if 'Strict-Transport-Security' not in headers:
                self.findings.append({
                    'vulnerability': 'Missing Strict-Transport-Security header',
                    'severity': 'Medium',
                    'evidence': f'Header not found in {target_url}',
                    'remediation': 'Implement HSTS to force secure (HTTPS) connections.'
                })
            if 'Content-Security-Policy' not in headers:
                self.findings.append({
                    'vulnerability': 'Missing Content-Security-Policy header',
                    'severity': 'Medium',
                    'evidence': f'Header not found in {target_url}',
                    'remediation': 'Implement a strong Content Security Policy to mitigate XSS and data injection attacks.'
                })
            print("Header scan complete.")
        except requests.exceptions.RequestException as e:
            print(f"Error scanning {target_url}: {e}")

    def run_all_scans(self, target_url, idor_params=None, sqli_params=None, xss_params=None, auth_params=None, sdi_params=None, lm_params=None, ssrf_params=None):
        self.scan_headers(target_url)

        if idor_params:
            self.access_control_scanner.check_idor(
                target_url, idor_params["vulnerable_endpoint"],
                idor_params["valid_id"], idor_params["attacker_id"]
            )
            self.findings.extend(self.access_control_scanner.get_findings())

        if sqli_params:
            self.injection_scanner.check_sqli(
                target_url, sqli_params["param_name"]
            )
            self.findings.extend(self.injection_scanner.get_findings())

        if xss_params:
            self.xss_scanner.check_reflected_xss(
                target_url, xss_params["param_name"]
            )
            self.findings.extend(self.xss_scanner.get_findings())

        self.crypto_failures_scanner.check_tls_config(target_url)
        self.findings.extend(self.crypto_failures_scanner.get_findings())

        self.security_misconfiguration_scanner.check_default_pages(target_url)
        self.security_misconfiguration_scanner.check_verbose_errors(target_url)
        self.findings.extend(self.security_misconfiguration_scanner.get_findings())

        self.vulnerable_components_scanner.check_outdated_components(target_url)
        self.findings.extend(self.vulnerable_components_scanner.get_findings())

        if auth_params:
            self.authentication_failures_scanner.check_weak_credentials(
                auth_params["login_url"], auth_params["username_field"],
                auth_params["password_field"], auth_params["common_credentials"]
            )
            self.findings.extend(self.authentication_failures_scanner.get_findings())

        if sdi_params:
            self.software_data_integrity_scanner.check_unsigned_artifacts(
                target_url, sdi_params["artifact_path"]
            )
            self.findings.extend(self.software_data_integrity_scanner.get_findings())

        if lm_params:
            self.logging_monitoring_scanner.check_logging_presence(
                target_url, lm_params["sensitive_action_path"]
            )
            self.findings.extend(self.logging_monitoring_scanner.get_findings())

        if ssrf_params:
            self.ssrf_scanner.check_ssrf(
                target_url, ssrf_params["param_name"],
                ssrf_params.get("collaborator_url")
            )
            self.findings.extend(self.ssrf_scanner.get_findings())

    def get_findings(self):
        return self.findings


