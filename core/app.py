import sys
import os

# إضافة جذر المشروع
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# إضافة مجلد modules عشان Python يلاقي الموديولات
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from scanner import Scanner

# تحديد مسار الـ static folder بشكل صحيح
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gui', 'ohunter-ui', 'dist')
app = Flask(__name__, static_folder=static_path, static_url_path='')
CORS(app)

@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        return jsonify({
            "error": "Frontend not available", 
            "message": "Please ensure the frontend is built properly",
            "details": str(e)
        }), 404

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files for React app"""
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        # If file not found, serve index.html for React Router
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/scan', methods=['POST'])
def scan_endpoint():
    """Main scanning endpoint"""
    try:
        data = request.get_json()
        target_url = data.get('target_url')
        
        if not target_url:
            return jsonify({'error': 'Target URL is required'}), 400
        
        scanner = Scanner()
        scanner.run_all_scans(
            target_url,
            sqli_params={'param_name': 'id'},
            xss_params={'param_name': 'search'},
            ssrf_params={'param_name': 'url'}
        )
        
        findings = scanner.get_findings()
        
        return jsonify({
            'target_url': target_url,
            'findings': findings,
            'total_findings': len(findings),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': 'Scanning failed',
            'message': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy', 
        'message': 'O-Hunter API is running',
        'version': '1.0.0',
        'frontend_available': os.path.exists(os.path.join(app.static_folder, 'index.html'))
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by serving React app"""
    return serve_frontend()

if __name__ == '__main__':
    # قراءة البورت من متغير البيئة (Railway يستخدم PORT)
    port = int(os.environ.get("PORT", 8080))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    print(f"Starting O-Hunter on port {port}")
    print(f"Static folder: {app.static_folder}")
    print(f"Frontend available: {os.path.exists(os.path.join(app.static_folder, 'index.html'))}")
    
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
