# O-Hunter Developer Guide

## Overview

This guide provides detailed information for developers who want to contribute to O-Hunter or extend its functionality by adding new vulnerability scanners.

## Architecture Deep Dive

### Core Engine (`core/scanner.py`)

The core engine orchestrates all vulnerability scans and manages the overall scanning process. It follows a modular architecture where each vulnerability type is implemented as a separate scanner class.

```python
class Scanner:
    def __init__(self):
        self.findings = []
        # Initialize all scanner modules
        self.access_control_scanner = AccessControlScanner()
        self.injection_scanner = InjectionScanner()
        # ... other scanners
```

### Scanner Module Interface

Each vulnerability scanner should implement the following interface:

```python
class VulnerabilityScanner:
    def __init__(self):
        self.findings = []
    
    def scan_method(self, target_url, **kwargs):
        # Implement vulnerability detection logic
        pass
    
    def get_findings(self):
        return self.findings
```

### Finding Format

All findings should follow this standardized format:

```python
finding = {
    'vulnerability': 'Descriptive name of the vulnerability',
    'severity': 'Critical|High|Medium|Low',
    'evidence': 'Specific evidence of the vulnerability',
    'remediation': 'Clear steps to fix the vulnerability'
}
```

## Adding New Vulnerability Scanners

### Step 1: Create Scanner Module

Create a new file in the `modules/` directory:

```python
# modules/new_vulnerability.py
import requests

class NewVulnerabilityScanner:
    def __init__(self):
        self.findings = []
    
    def check_vulnerability(self, target_url):
        # Implement your vulnerability detection logic
        try:
            response = requests.get(target_url, timeout=10)
            # Analyze response for vulnerability indicators
            if self.is_vulnerable(response):
                self.findings.append({
                    'vulnerability': 'New Vulnerability Type',
                    'severity': 'Medium',
                    'evidence': f'Vulnerability detected at {target_url}',
                    'remediation': 'Steps to remediate this vulnerability'
                })
        except requests.exceptions.RequestException as e:
            print(f"Error checking vulnerability: {e}")
    
    def is_vulnerable(self, response):
        # Implement vulnerability detection logic
        return False
    
    def get_findings(self):
        return self.findings
```

### Step 2: Integrate with Core Scanner

Add your scanner to the main `Scanner` class:

```python
# core/scanner.py
from modules.new_vulnerability import NewVulnerabilityScanner

class Scanner:
    def __init__(self):
        # ... existing scanners
        self.new_vulnerability_scanner = NewVulnerabilityScanner()
    
    def run_all_scans(self, target_url, **kwargs):
        # ... existing scans
        
        # Add your scanner
        if kwargs.get('new_vuln_params'):
            self.new_vulnerability_scanner.check_vulnerability(target_url)
            self.findings.extend(self.new_vulnerability_scanner.get_findings())
```

### Step 3: Add Tests

Create tests for your new scanner:

```python
# tests/test_new_vulnerability.py
import unittest
from modules.new_vulnerability import NewVulnerabilityScanner

class TestNewVulnerabilityScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = NewVulnerabilityScanner()
    
    def test_scanner_initialization(self):
        self.assertIsInstance(self.scanner, NewVulnerabilityScanner)
        self.assertEqual(len(self.scanner.findings), 0)
    
    def test_vulnerability_detection(self):
        # Test your vulnerability detection logic
        pass
```

## Best Practices

### Security Considerations

1. **Safe by Default**: All scanners should be non-destructive by default
2. **Rate Limiting**: Implement delays between requests to avoid DoS
3. **Error Handling**: Gracefully handle network errors and timeouts
4. **Input Validation**: Validate all user inputs and target URLs

### Code Quality

1. **Documentation**: Document all methods and complex logic
2. **Error Messages**: Provide clear, actionable error messages
3. **Logging**: Use appropriate logging levels for debugging
4. **Testing**: Write comprehensive tests for all functionality

### Performance

1. **Timeouts**: Set reasonable timeouts for all network requests
2. **Parallel Processing**: Consider using threading for independent checks
3. **Caching**: Cache results when appropriate to avoid duplicate requests
4. **Resource Management**: Properly close connections and clean up resources

## API Integration

### Adding External Tool Integration

To integrate external security tools (like nmap, sqlmap, etc.):

```python
import subprocess
import json

class ExternalToolScanner:
    def run_external_tool(self, target_url):
        try:
            # Example: Running nmap
            result = subprocess.run([
                'nmap', '-sV', '--script=vuln', target_url
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return self.parse_tool_output(result.stdout)
        except subprocess.TimeoutExpired:
            print("External tool timed out")
        except FileNotFoundError:
            print("External tool not found")
    
    def parse_tool_output(self, output):
        # Parse tool output and convert to findings format
        pass
```

## Frontend Integration

### Adding New UI Components

To add new components to the React frontend:

1. Create component in `gui/ohunter-ui/src/components/`
2. Import and use in the main App component
3. Update the API endpoints if needed

### API Endpoints

Add new API endpoints in `core/app.py`:

```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    data = request.get_json()
    # Process request
    return jsonify({'result': 'success'})
```

## Configuration Management

### Environment Variables

Use environment variables for configuration:

```python
import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SCAN_TIMEOUT = int(os.getenv('SCAN_TIMEOUT', '300'))
    MAX_THREADS = int(os.getenv('MAX_THREADS', '10'))
```

### Configuration Files

For complex configurations, use JSON or YAML files:

```python
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)
```

## Deployment Considerations

### Docker Optimization

- Use multi-stage builds to reduce image size
- Run as non-root user for security
- Set appropriate resource limits

### Production Deployment

- Use a production WSGI server (gunicorn, uWSGI)
- Implement proper logging and monitoring
- Set up SSL/TLS certificates
- Configure reverse proxy (nginx, Apache)

## Troubleshooting

### Common Issues

1. **Module Import Errors**: Ensure PYTHONPATH is set correctly
2. **Network Timeouts**: Adjust timeout values for slow targets
3. **Permission Errors**: Check file permissions and user privileges
4. **Memory Issues**: Monitor memory usage for large scans

### Debugging

Enable debug mode for detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing Guidelines

1. Follow PEP 8 style guidelines
2. Write comprehensive tests
3. Update documentation
4. Use meaningful commit messages
5. Test on multiple Python versions

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.org/dev/security/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/)

---

For questions or clarifications, please open an issue or contact the development team.

