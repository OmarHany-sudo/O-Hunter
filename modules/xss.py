
import requests

class XSSScanner:
    def __init__(self):
        self.findings = []
        self.xss_payloads = [
            "<script>alert(\'XSS\')</script>",
            "<img src=x onerror=alert(\'XSS\')>",
            "<svg/onload=alert(\'XSS\')>"
        ]

    def check_reflected_xss(self, target_url, param_name):
        print(f"Checking Reflected XSS for {target_url} with parameter {param_name}")
        for payload in self.xss_payloads:
            test_url = f"{target_url}?{param_name}={payload}"
            try:
                response = requests.get(test_url, timeout=10)
                if payload in response.text:
                    self.findings.append({
                        'vulnerability': 'Reflected Cross-Site Scripting (XSS)',
                        'severity': 'High',
                        'evidence': f'Payload \'{payload}\' reflected in response at {test_url}',
                        'remediation': 'Implement proper output encoding for all user-supplied input. Use Content Security Policy (CSP).'
                    })
                    return
            except requests.exceptions.RequestException as e:
                print(f"Error checking XSS for {test_url}: {e}")
        print("Reflected XSS check complete (no obvious vulnerabilities found).")

    def get_findings(self):
        return self.findings


