
import requests

class AuthenticationFailuresScanner:
    def __init__(self):
        self.findings = []

    def check_weak_credentials(self, login_url, username_field, password_field, common_credentials):
        print(f"Checking for weak credentials on {login_url}")
        for username, password in common_credentials:
            data = {username_field: username, password_field: password}
            try:
                response = requests.post(login_url, data=data, timeout=5)
                # This is a simplified check. A real check would look for successful login indicators.
                if "welcome" in response.text.lower() or "dashboard" in response.text.lower():
                    self.findings.append({
                        'vulnerability': 'Weak/Default Credentials Found',
                        'severity': 'High',
                        'evidence': f'Successful login with username: {username}, password: {password} at {login_url}',
                        'remediation': 'Enforce strong password policies, implement multi-factor authentication, and disable default credentials.'
                    })
                    return # Found one, no need to continue
            except requests.exceptions.RequestException as e:
                print(f"Error checking weak credentials for {login_url}: {e}")

    def get_findings(self):
        return self.findings


