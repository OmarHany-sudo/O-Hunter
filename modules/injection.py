
import requests

class InjectionScanner:
    def __init__(self):
        self.findings = []
        self.sqli_payloads = ["' OR 1=1 --", "' OR 'a'='a", "admin'--", "1 UNION SELECT NULL,NULL,NULL--"]

    def check_sqli(self, target_url, param_name):
        print(f"Checking SQL Injection for {target_url} with parameter {param_name}")
        for payload in self.sqli_payloads:
            test_url = f"{target_url}?{param_name}={payload}"
            try:
                response = requests.get(test_url, timeout=10)
                # Simple check for common SQL error messages or unexpected content
                if "syntax error" in response.text.lower() or \
                   "mysql_fetch_array" in response.text.lower() or \
                   "unclosed quotation mark" in response.text.lower():
                    self.findings.append({
                        'vulnerability': 'Potential SQL Injection',
                        'severity': 'High',
                        'evidence': f'Payload \'{payload}\' caused error/unusual response at {test_url}',
                        'remediation': 'Use parameterized queries or prepared statements. Implement input validation and least privilege database accounts.'
                    })
                    return # Found one, no need to test further payloads for this URL/param
            except requests.exceptions.RequestException as e:
                print(f"Error checking SQLi for {test_url}: {e}")
        print("SQL Injection check complete (no obvious vulnerabilities found).")

    def get_findings(self):
        return self.findings


