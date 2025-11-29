import os
import json
import urllib.request
import urllib.parse
import urllib.error
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID", "")

@app.route('/')
def index():
    return render_template('index.html', api_configured=bool(GOOGLE_API_KEY))

@app.route('/search', methods=['POST'])
def search():
    if not GOOGLE_API_KEY:
        return jsonify({'error': 'Cle API non configuree'}), 500
    
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Recherche vide'}), 400
        
        search_engine_id = SEARCH_ENGINE_ID or "a1b2c3d4e5f6g7h8i"
        
        params = urllib.parse.urlencode({
            'key': GOOGLE_API_KEY,
            'cx': search_engine_id,
            'q': query,
            'num': 10
        })
        
        url = f"https://www.googleapis.com/customsearch/v1?{params}"
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            
            items = result.get('items', [])
            search_results = []
            
            for item in items:
                search_results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'image': item.get('pagemap', {}).get('cse_thumbnail', [{}])[0].get('src', '')
                })
            
            return jsonify({
                'results': search_results,
                'total': result.get('searchInformation', {}).get('totalResults', 0),
                'time': result.get('searchInformation', {}).get('formattedSearchTime', '')
            })
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            error_json = json.loads(error_body)
            error_message = error_json.get('error', {}).get('message', str(e))
        except:
            error_message = str(e)
        return jsonify({'error': f'Erreur API: {error_message}'}), e.code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-api', methods=['GET'])
def test_api():
    if not GOOGLE_API_KEY:
        return jsonify({'status': 'error', 'message': 'Cle API non configuree'}), 500
    
    try:
        url = f"https://www.googleapis.com/discovery/v1/apis?key={GOOGLE_API_KEY}"
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if 'items' in data:
                return jsonify({
                    'status': 'success',
                    'message': 'Cle API valide!',
                    'apis_count': len(data['items'])
                })
            else:
                return jsonify({'status': 'error', 'message': 'Reponse inattendue'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
