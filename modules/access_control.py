
import requests

class AccessControlScanner:
    def __init__(self):
        self.findings = []

    def check_idor(self, base_url, vulnerable_endpoint, valid_id, attacker_id):
        print(f"Checking IDOR for {vulnerable_endpoint} with IDs {valid_id} and {attacker_id}")
        try:
            # Attempt to access valid_id with attacker_id credentials (simulated)
            # In a real scenario, this would involve session management and authentication
            valid_url = f"{base_url}/{vulnerable_endpoint}/{valid_id}"
            attacker_url = f"{base_url}/{vulnerable_endpoint}/{attacker_id}"

            # Simulate accessing valid_id as attacker
            response_valid = requests.get(valid_url, timeout=10)
            response_attacker = requests.get(attacker_url, timeout=10)

            if response_valid.status_code == 200 and response_attacker.status_code == 200 and response_valid.text != response_attacker.text:
                self.findings.append({
                    'vulnerability': 'Insecure Direct Object Reference (IDOR)',
                    'severity': 'High',
                    'evidence': f'Accessed {valid_url} (expected) and {attacker_url} (unexpected) with similar content structure but different data.',
                    'remediation': 'Implement robust server-side access control checks for all direct object references. Use indirect references or enforce ownership checks.'
                })
            else:
                print("IDOR check passed (no direct evidence found).")

        except requests.exceptions.RequestException as e:
            print(f"Error checking IDOR: {e}")

    def get_findings(self):
        return self.findings


