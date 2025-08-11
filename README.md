# O-Hunter: Web Vulnerability Scanner

```
  ____ _   _ _   _ ____   _____
 / ___| | | | \ | |  _ \ / ____|
| |   | | | |  \| | |_) | (___   ___ _ __ __ _ _ __ ___   ___
| |   | | | | . ` |  _ < \___ \ / __| '__/ _` | '_ ` _ \ / _ \
| |___| |_| | |\  | |_) |____) | (__| | | (_| | | | | | |  __/
 \_____\___/|_| \_|____/|_____/ \___|_|  \__,_|_| |_| |_|\___|

Developed by Eng. Omar Hany
```

O-Hunter is a comprehensive web vulnerability scanner that automatically tests for OWASP Top 10 web risks, produces prioritized findings, includes exploitation PoCs (safe/non-destructive by default), and provides clear remediation steps.

## Features

- **OWASP Top 10 Coverage**: Complete coverage of all OWASP Top 10 (2021) categories
- **Multi-Modal Scanning**: Passive, active non-invasive, and optional advanced exploit modules
- **Modular Architecture**: Easy to add new tests and plugins
- **Multiple Output Formats**: JSON, HTML reports, and interactive web UI dashboard
- **Safety First**: Built-in safe-mode with consent workflow for active scanning
- **Professional UI**: Modern React-based dashboard with real-time scanning

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd O-Hunter

# Build and run with Docker Compose
docker-compose up --build

# Access the web interface at http://localhost:5000
```

### Manual Installation

```bash
# Clone the repository
git clone <repository-url>
cd O-Hunter

# Create virtual environment
cd core
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Build the frontend
cd ../gui/ohunter-ui
npm install
npm run build

# Start the application
cd ../../
PYTHONPATH=/path/to/O-Hunter python core/app.py
```

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a target URL in the scan input field
3. Click "Start Scan" to begin vulnerability assessment
4. Review findings and download reports

### Command Line Interface

```bash
# Basic passive scan
python cli.py --target https://example.com --mode passive

# Active scan with JSON report
python cli.py --target https://example.com --mode active --output report.json

# Full scan with HTML report
python cli.py --target https://example.com --mode full --output report.html --format html

# Advanced exploitation (requires confirmation)
python cli.py --target https://example.com --mode full --exploit
```

### CLI Options

- `--target, -t`: Target URL to scan (required)
- `--mode, -m`: Scan mode (passive, active, full) - default: passive
- `--output, -o`: Output file path
- `--format, -f`: Output format (json, html) - default: json
- `--plugin, -p`: Specific plugins to run (comma-separated)
- `--exploit`: Enable advanced exploitation (requires confirmation)

## Architecture

### Core Components

1. **Core Engine** (`core/`): Scanner orchestration, scheduling, plugin loader
2. **Modules** (`modules/`): Individual vulnerability scanners for each OWASP category
3. **GUI** (`gui/`): React-based web interface
4. **CLI** (`cli.py`): Command-line interface for automated scans

### Vulnerability Modules

- **Access Control**: IDOR, privilege escalation, forced browsing
- **Injection**: SQL injection, command injection, NoSQL injection
- **XSS**: Reflected, stored, and DOM-based cross-site scripting
- **Cryptographic Failures**: TLS configuration, weak ciphers
- **Security Misconfiguration**: Missing headers, default files, verbose errors
- **Vulnerable Components**: Outdated software detection
- **Authentication Failures**: Weak credentials, session management
- **Software/Data Integrity**: Unsigned artifacts, CI/CD misconfigurations
- **Logging & Monitoring**: Missing security logs and alerts
- **SSRF**: Server-side request forgery detection

## Safety & Legal Considerations

⚠️ **IMPORTANT**: O-Hunter includes built-in safety mechanisms:

- **Consent Workflow**: Explicit authorization required before active scanning
- **Safe Mode**: Default passive + non-destructive active checks
- **Rate Limiting**: Built-in throttling to avoid DoS
- **Confirmation Gates**: Typed confirmation required for destructive checks

### Legal Usage

- Only scan systems you own or have explicit permission to test
- Respect rate limits and avoid disrupting target services
- Follow responsible disclosure practices for any vulnerabilities found
- Comply with local laws and regulations regarding security testing

## Development

### Adding New Plugins

1. Create a new scanner class in the `modules/` directory
2. Implement the required methods following the existing pattern
3. Add the scanner to the main `Scanner` class in `core/scanner.py`
4. Write tests for your new module

### Project Structure

```
O-Hunter/
├── core/                   # Core engine and backend
│   ├── app.py             # Flask web application
│   ├── scanner.py         # Main scanner orchestrator
│   ├── report_generator.py # Report generation
│   └── venv/              # Python virtual environment
├── modules/               # Vulnerability scanner modules
│   ├── access_control.py
│   ├── injection.py
│   ├── xss.py
│   └── ...
├── gui/                   # React frontend
│   └── ohunter-ui/
├── tests/                 # Unit and integration tests
├── docs/                  # Documentation
├── cli.py                 # Command-line interface
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
└── requirements.txt       # Python dependencies
```

### Running Tests

```bash
# Run unit tests
PYTHONPATH=/path/to/O-Hunter python tests/test_scanner.py

# Test CLI functionality
python cli.py --target https://httpbin.org --mode passive
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OWASP Foundation for the Top 10 vulnerability categories
- Security research community for vulnerability detection techniques
- Open source security tools that inspired this project

## Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact: Eng. Omar Hany

---

**Disclaimer**: This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before scanning any systems.

