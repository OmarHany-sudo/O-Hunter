
import requests

class CryptoFailuresScanner:
    def __init__(self):
        self.findings = []

    def check_tls_config(self, target_url):
        print(f"Checking TLS configuration for: {target_url}")
        try:
            # This is a simplified check. A real scanner would use tools like testssl.sh or sslyze.
            # We'll just check if HTTPS is used.
            if not target_url.startswith("https://"):
                self.findings.append({
                    'vulnerability': 'Insecure TLS/SSL Configuration (HTTP used instead of HTTPS)',
                    'severity': 'High',
                    'evidence': f'Target URL {target_url} is using HTTP. All communication should be over HTTPS.',
                    'remediation': 'Enforce HTTPS for all traffic. Obtain and configure a valid SSL/TLS certificate.'
                })
            else:
                print("HTTPS is used. Further TLS checks would require specialized tools.")

        except requests.exceptions.RequestException as e:
            print(f"Error checking TLS config for {target_url}: {e}")

    def get_findings(self):
        return self.findings


