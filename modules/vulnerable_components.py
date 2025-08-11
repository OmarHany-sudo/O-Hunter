
import requests

class VulnerableComponentsScanner:
    def __init__(self):
        self.findings = []

    def check_outdated_components(self, target_url):
        print(f"Checking for outdated components on: {target_url}")
        # This is a placeholder. Real-world component scanning requires
        # integration with vulnerability databases (e.g., Snyk, OWASP Dependency-Check)
        # or analyzing package.json/pom.xml files.
        # For demonstration, we'll simulate a check for a known outdated server header.
        try:
            response = requests.get(target_url, timeout=10)
            server_header = response.headers.get("Server", "").lower()

            if "apache/2.2" in server_header or "nginx/1.0" in server_header:
                self.findings.append({
                    'vulnerability': 'Outdated Web Server Component',
                    'severity': 'High',
                    'evidence': f'Server header indicates outdated component: {server_header} at {target_url}',
                    'remediation': 'Upgrade web server to the latest stable version to mitigate known vulnerabilities.'
                })
            else:
                print("No obviously outdated server components detected (simplified check).")

        except requests.exceptions.RequestException as e:
            print(f"Error checking outdated components for {target_url}: {e}")

    def get_findings(self):
        return self.findings


