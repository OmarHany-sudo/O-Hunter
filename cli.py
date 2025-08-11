#!/usr/bin/env python3
import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.scanner import Scanner
from core.report_generator import ReportGenerator

ASCII_LOGO = """
  ____ _   _ _   _ ____   _____
 / ___| | | | \ | |  _ \ / ____|
| |   | | | |  \| | |_) | (___   ___ _ __ __ _ _ __ ___   ___
| |   | | | | . ` |  _ < \___ \ / __| '__/ _` | '_ ` _ \ / _ \
| |___| |_| | |\  | |_) |____) | (__| | | (_| | | | | | |  __/
 \_____\___/|_| \_|____/|_____/ \___|_|  \__,_|_| |_| |_|\___|

Developed by Eng. Omar Hany
"""

def main():
    print(ASCII_LOGO)
    
    parser = argparse.ArgumentParser(description='O-Hunter: Web Vulnerability Scanner')
    parser.add_argument('--target', '-t', required=True, help='Target URL to scan')
    parser.add_argument('--mode', '-m', choices=['passive', 'active', 'full'], default='passive',
                        help='Scan mode (default: passive)')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['json', 'html'], default='json',
                        help='Output format (default: json)')
    parser.add_argument('--plugin', '-p', help='Specific plugins to run (comma-separated)')
    parser.add_argument('--exploit', action='store_true', 
                        help='Enable advanced exploitation (requires confirmation)')
    
    args = parser.parse_args()
    
    # Safety check for exploit mode
    if args.exploit:
        print("⚠️  WARNING: Advanced exploitation mode enabled!")
        print("This mode may perform potentially destructive tests.")
        confirmation = input("Type 'YES' to confirm: ")
        if confirmation != 'YES':
            print("Exploitation mode cancelled. Running in safe mode.")
            args.exploit = False
    
    print(f"Starting scan of {args.target} in {args.mode} mode...")
    
    scanner = Scanner()
    
    # Configure scan parameters based on mode
    if args.mode == 'passive':
        scanner.scan_headers(args.target)
    elif args.mode == 'active':
        scanner.run_all_scans(
            args.target,
            sqli_params={'param_name': 'id'},
            xss_params={'param_name': 'search'}
        )
    elif args.mode == 'full':
        scanner.run_all_scans(
            args.target,
            idor_params={'vulnerable_endpoint': 'user', 'valid_id': '1', 'attacker_id': '2'},
            sqli_params={'param_name': 'id'},
            xss_params={'param_name': 'search'},
            auth_params={
                'login_url': f"{args.target}/login",
                'username_field': 'username',
                'password_field': 'password',
                'common_credentials': [('admin', 'admin'), ('admin', 'password')]
            },
            sdi_params={'artifact_path': '/download/app.zip'},
            lm_params={'sensitive_action_path': '/login'},
            ssrf_params={'param_name': 'url'}
        )
    
    findings = scanner.get_findings()
    
    print(f"\nScan complete. Found {len(findings)} potential vulnerabilities.")
    
    # Generate report
    if args.output:
        report_gen = ReportGenerator(findings, args.target)
        
        if args.format == 'json':
            output_file = report_gen.generate_json_report(args.output)
        elif args.format == 'html':
            output_file = report_gen.generate_html_report(args.output)
        
        print(f"Report saved to: {output_file}")
    else:
        # Print findings to console
        for finding in findings:
            print(f"\n[{finding['severity']}] {finding['vulnerability']}")
            print(f"Evidence: {finding['evidence']}")
            print(f"Remediation: {finding['remediation']}")

if __name__ == '__main__':
    main()

