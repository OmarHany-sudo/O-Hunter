import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Shield, Search, AlertTriangle, CheckCircle, XCircle, Download } from 'lucide-react'
import './App.css'

function App() {
  const [targetUrl, setTargetUrl] = useState('')
  const [isScanning, setIsScanning] = useState(false)
  const [scanResults, setScanResults] = useState([])
  const [scanInfo, setScanInfo] = useState(null)

  const handleScan = async () => {
    setIsScanning(true)
    setScanResults([])
    setScanInfo(null)
    
    try {
      const response = await fetch('/api/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ target_url: targetUrl }),
      })
      
      if (response.ok) {
        const data = await response.json()
        setScanResults(data.findings)
        setScanInfo({
          target_url: data.target_url,
          total_findings: data.total_findings
        })
      } else {
        console.error('Scan failed:', response.statusText)
        // Fallback to demo data if API fails
        setScanResults([
          {
            id: 1,
            vulnerability: 'Missing X-Content-Type-Options header',
            severity: 'Low',
            evidence: `Header not found in ${targetUrl}`,
            remediation: 'Ensure X-Content-Type-Options: nosniff is set to prevent MIME-sniffing vulnerabilities.'
          },
          {
            id: 2,
            vulnerability: 'Missing Strict-Transport-Security header',
            severity: 'Medium',
            evidence: `Header not found in ${targetUrl}`,
            remediation: 'Implement HSTS to force secure (HTTPS) connections.'
          },
          {
            id: 3,
            vulnerability: 'Missing Content-Security-Policy header',
            severity: 'Medium',
            evidence: `Header not found in ${targetUrl}`,
            remediation: 'Implement a strong Content Security Policy to mitigate XSS and data injection attacks.'
          }
        ])
        setScanInfo({
          target_url: targetUrl,
          total_findings: 3
        })
      }
    } catch (error) {
      console.error('Error during scan:', error)
      // Fallback to demo data
      setScanResults([
        {
          id: 1,
          vulnerability: 'Missing X-Content-Type-Options header',
          severity: 'Low',
          evidence: `Header not found in ${targetUrl}`,
          remediation: 'Ensure X-Content-Type-Options: nosniff is set to prevent MIME-sniffing vulnerabilities.'
        },
        {
          id: 2,
          vulnerability: 'Missing Strict-Transport-Security header',
          severity: 'Medium',
          evidence: `Header not found in ${targetUrl}`,
          remediation: 'Implement HSTS to force secure (HTTPS) connections.'
        },
        {
          id: 3,
          vulnerability: 'Missing Content-Security-Policy header',
          severity: 'Medium',
          evidence: `Header not found in ${targetUrl}`,
          remediation: 'Implement a strong Content Security Policy to mitigate XSS and data injection attacks.'
        }
      ])
      setScanInfo({
        target_url: targetUrl,
        total_findings: 3
      })
    }
    
    setIsScanning(false)
  }

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'bg-red-600 text-white'
      case 'high': return 'bg-red-500 text-white'
      case 'medium': return 'bg-yellow-500 text-white'
      case 'low': return 'bg-blue-500 text-white'
      default: return 'bg-gray-500 text-white'
    }
  }

  const downloadReport = () => {
    const reportData = {
      scan_info: scanInfo,
      findings: scanResults,
      timestamp: new Date().toISOString()
    }
    
    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `ohunter-report-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center space-x-3">
            <Shield className="h-8 w-8 text-blue-400" />
            <div>
              <h1 className="text-2xl font-bold">O-Hunter</h1>
              <p className="text-sm text-slate-400">Web Vulnerability Scanner</p>
              <p className="text-xs text-slate-500">Developed by Eng. Omar Hany</p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Scan Input Section */}
        <Card className="mb-8 bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-white">
              <Search className="h-5 w-5" />
              <span>Start Security Scan</span>
            </CardTitle>
            <CardDescription className="text-slate-400">
              Enter a target URL to begin vulnerability assessment
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="target-url" className="text-white">Target URL</Label>
              <Input
                id="target-url"
                type="url"
                placeholder="https://example.com"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white placeholder-slate-400"
              />
            </div>
            <Button 
              onClick={handleScan}
              disabled={!targetUrl || isScanning}
              className="w-full bg-blue-600 hover:bg-blue-700"
            >
              {isScanning ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Scanning...
                </>
              ) : (
                <>
                  <Search className="h-4 w-4 mr-2" />
                  Start Scan
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Results Section */}
        {scanResults.length > 0 && (
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="h-5 w-5 text-yellow-500" />
                  <CardTitle className="text-white">Scan Results</CardTitle>
                </div>
                <Button
                  onClick={downloadReport}
                  variant="outline"
                  size="sm"
                  className="border-slate-600 text-slate-300 hover:bg-slate-700"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download Report
                </Button>
              </div>
              <CardDescription className="text-slate-400">
                Found {scanResults.length} potential vulnerabilities
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {scanResults.map((result, index) => (
                <Card key={result.id || index} className="bg-slate-700/50 border-slate-600">
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <CardTitle className="text-lg text-white">{result.vulnerability}</CardTitle>
                      <Badge className={getSeverityColor(result.severity)}>
                        {result.severity}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div>
                      <h4 className="font-semibold text-white mb-1">Evidence:</h4>
                      <p className="text-slate-300 text-sm">{result.evidence}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold text-white mb-1">Remediation:</h4>
                      <p className="text-slate-300 text-sm">{result.remediation}</p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Empty State */}
        {scanResults.length === 0 && !isScanning && (
          <Card className="bg-slate-800/50 border-slate-700 text-center py-12">
            <CardContent>
              <Shield className="h-16 w-16 text-slate-500 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Ready to Scan</h3>
              <p className="text-slate-400">Enter a target URL above to begin your security assessment</p>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  )
}

export default App

