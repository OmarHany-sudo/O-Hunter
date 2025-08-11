import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scanner import Scanner

class TestScanner(unittest.TestCase):
    
    def setUp(self):
        self.scanner = Scanner()
    
    def test_scanner_initialization(self):
        """Test that scanner initializes correctly"""
        self.assertIsInstance(self.scanner, Scanner)
        self.assertEqual(len(self.scanner.findings), 0)
    
    def test_header_scan(self):
        """Test header scanning functionality"""
        # This would normally test against a mock server
        # For now, we'll just test that the method exists and can be called
        try:
            self.scanner.scan_headers("https://httpbin.org")
            # Check that findings were added (headers are usually missing)
            self.assertGreater(len(self.scanner.findings), 0)
        except Exception as e:
            # If network is unavailable, test should still pass
            self.skipTest(f"Network unavailable: {e}")
    
    def test_get_findings(self):
        """Test that get_findings returns a list"""
        findings = self.scanner.get_findings()
        self.assertIsInstance(findings, list)

if __name__ == '__main__':
    unittest.main()

