from flask import Flask, jsonify, render_template
import os
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Main web page"""
    return render_template('index.html', 
                         version=os.environ.get('APP_VERSION', '1.0.0'),
                         environment=os.environ.get('FLASK_ENV', 'development'))

@app.route('/api')
def api():
    """API endpoint"""
    return jsonify({
        'message': 'Welcome to Simple DevOps Flask API',
        'version': os.environ.get('APP_VERSION', '1.0.0'),
        'status': 'running'
    })

@app.route('/health')
def health_check():
    """Health check endpoint with web UI"""
    health_data = {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'version': os.environ.get('APP_VERSION', '1.0.0'),
        'environment': os.environ.get('FLASK_ENV', 'development')
    }
    return render_template('health.html', **health_data)

@app.route('/api/health')
def health_api():
    """Health check API endpoint (JSON only)"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': os.environ.get('APP_VERSION', '1.0.0')
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)