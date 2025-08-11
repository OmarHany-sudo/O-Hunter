
from scanner import Scanner

ASCII_LOGO = """
  ____ _   _ _   _ ____   _____
 / ___| | | | \ | |  _ \ / ____|
| |   | | | |  \| | |_) | (___   ___ _ __ __ _ _ __ ___   ___
| |   | | | | . ` |  _ < \___ \ / __| \'_/ _` | \'_ ` _ \ / _ \
| |___| |_| | |\  | |_) |____) | (__| | | (_| | | | | | |  __/
 \_____\___/|_| \_|____/|_____/ \___|_|  \__,_|_| |_| |_|\___|

Developed by Eng. Omar Hany
"""

def main():
    print(ASCII_LOGO)
    print("O-Hunter: Web Vulnerability Scanner")
    print("Starting core engine...")

    scanner = Scanner()
    # Example usage: Scan a target URL for headers
    target_url = "https://www.google.com"
    scanner.scan_headers(target_url)

    findings = scanner.get_findings()
    if findings:
        print("\nScan Findings:")
        for finding in findings:
            print(f"  Vulnerability: {finding["vulnerability"]}")
            print(f"  Severity: {finding["severity"]}")
            print(f"  Evidence: {finding["evidence"]}")
            print(f"  Remediation: {finding["remediation"]}\n")
    else:
        print("\nNo findings from header scan.")

if __name__ == "__main__":
    main()


