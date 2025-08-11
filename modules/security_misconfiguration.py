
import requests

class SecurityMisconfigurationScanner:
    def __init__(self):
        self.findings = []

    def check_default_pages(self, target_url):
        print(f"Checking for default pages/files on: {target_url}")
        common_default_paths = [
            "/admin", "/backup", "/test", "/phpinfo.php", "/.git/config"
        ]
        for path in common_default_paths:
            test_url = f"{target_url}{path}"
            try:
                response = requests.get(test_url, timeout=5)
                if response.status_code == 200:
                    self.findings.append({
                        'vulnerability': 'Default/Sensitive File or Directory Found',
                        'severity': 'Medium',
                        'evidence': f'Found accessible path: {test_url} (Status: {response.status_code})',
                        'remediation': 'Remove or restrict access to default, unused, or sensitive files and directories. Ensure proper server configuration.'
                    })
            except requests.exceptions.RequestException as e:
                print(f"Error checking {test_url}: {e}")

    def check_verbose_errors(self, target_url):
        print(f"Checking for verbose error messages on: {target_url}")
        # This is a simplified check. A real check would involve triggering errors.
        # For now, we'll just look for common error indicators in a generic response.
        try:
            response = requests.get(target_url + "/nonexistent_page_to_trigger_error", timeout=5)
            if "stack trace" in response.text.lower() or \
               "error in query" in response.text.lower() or \
               "exception" in response.text.lower():
                self.findings.append({
                    'vulnerability': 'Verbose Error Messages',
                    'severity': 'Low',
                    'evidence': f'Verbose error message detected at {target_url}/nonexistent_page_to_trigger_error',
                    'remediation': 'Configure the application to display generic error messages to users and log detailed errors securely on the server-side.'
                })
        except requests.exceptions.RequestException as e:
            print(f"Error checking verbose errors for {target_url}: {e}")

    def get_findings(self):
        return self.findings


