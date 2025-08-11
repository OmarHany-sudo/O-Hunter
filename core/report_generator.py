import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, findings, target_url):
        self.findings = findings
        self.target_url = target_url
        self.timestamp = datetime.now().isoformat()

    def generate_json_report(self, output_file):
        """Generate JSON report"""
        report = {
            'scan_info': {
                'target_url': self.target_url,
                'timestamp': self.timestamp,
                'total_findings': len(self.findings)
            },
            'findings': self.findings
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return output_file

    def generate_html_report(self, output_file):
        """Generate HTML report"""
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>O-Hunter Security Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .finding {{ background-color: white; margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #3498db; }}
        .severity-critical {{ border-left-color: #e74c3c; }}
        .severity-high {{ border-left-color: #e67e22; }}
        .severity-medium {{ border-left-color: #f39c12; }}
        .severity-low {{ border-left-color: #3498db; }}
        .severity {{ padding: 2px 8px; border-radius: 3px; color: white; font-size: 12px; }}
        .severity.critical {{ background-color: #e74c3c; }}
        .severity.high {{ background-color: #e67e22; }}
        .severity.medium {{ background-color: #f39c12; }}
        .severity.low {{ background-color: #3498db; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>O-Hunter Security Report</h1>
        <p>Target: {self.target_url}</p>
        <p>Scan Date: {self.timestamp}</p>
        <p>Total Findings: {len(self.findings)}</p>
        <p>Developed by Eng. Omar Hany</p>
    </div>
    
    <div class="findings">
        {"".join([self._format_finding_html(finding) for finding in self.findings])}
    </div>
</body>
</html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html_template)
        
        return output_file

    def _format_finding_html(self, finding):
        severity_class = finding['severity'].lower()
        return f"""
        <div class="finding severity-{severity_class}">
            <h3>{finding['vulnerability']} <span class="severity {severity_class}">{finding['severity']}</span></h3>
            <p><strong>Evidence:</strong> {finding['evidence']}</p>
            <p><strong>Remediation:</strong> {finding['remediation']}</p>
        </div>
        """

    def generate_summary(self):
        """Generate a summary of findings"""
        severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        
        for finding in self.findings:
            severity = finding['severity']
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        return {
            'target_url': self.target_url,
            'timestamp': self.timestamp,
            'total_findings': len(self.findings),
            'severity_breakdown': severity_counts
        }

