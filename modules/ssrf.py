
import requests

class SSRFScanner:
    def __init__(self):
        self.findings = []

    def check_ssrf(self, target_url, param_name, collaborator_url="http://example.com/collaborator"):
        print(f"Checking SSRF for {target_url} with parameter {param_name} and Collaborator URL {collaborator_url}")
        # This is a simplified check. A real SSRF test would involve a controlled external server (Collaborator)
        # to detect out-of-band interactions.
        # For demonstration, we will try to make the target request a local IP or a known external IP.

        internal_ip_payload = "127.0.0.1"
        external_ip_payload = "http://www.google.com"

        payloads = [internal_ip_payload, external_ip_payload, collaborator_url]

        for payload in payloads:
            test_url = f"{target_url}?{param_name}={payload}"
            try:
                response = requests.get(test_url, timeout=5)
                # In a real scenario, we would check the Collaborator server for interaction.
                # Here, we'll look for signs of internal network access or unexpected redirects.
                if response.status_code == 200 and ("root:x" in response.text or "google" in response.text.lower()):
                    self.findings.append({
                        'vulnerability': 'Server-Side Request Forgery (SSRF)',
                        'severity': 'Critical',
                        'evidence': f'Payload \'{payload}\' caused unexpected response or internal resource access at {test_url}',
                        'remediation': 'Validate and whitelist URLs and domains accessed by the server. Enforce network egress filtering to prevent access to internal resources or unauthorized external endpoints.'
                    })
                    return # Found one, no need to test further payloads
            except requests.exceptions.RequestException as e:
                print(f"Error checking SSRF for {test_url}: {e}")
        print("SSRF check complete (no obvious vulnerabilities found).")

    def get_findings(self):
        return self.findings


