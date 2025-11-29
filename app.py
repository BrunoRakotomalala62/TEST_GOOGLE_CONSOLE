import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = os.urandom(24)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY") or os.environ.get("GOOGLE_API_KEY")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html', maps_api_key=GOOGLE_MAPS_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({'error': 'Cle API Gemini non configuree'}), 500
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/geocode', methods=['POST'])
def geocode():
    try:
        data = request.get_json()
        address = data.get('address', '')
        
        if not address:
            return jsonify({'error': 'Adresse vide'}), 400
        
        if not client:
            return jsonify({'error': 'Cle API non configuree'}), 500
        
        prompt = f"""Tu es un assistant de geocodage. Pour l'adresse suivante, donne-moi les coordonnees GPS (latitude, longitude) au format JSON.
        
Adresse: {address}

Reponds UNIQUEMENT avec un JSON valide dans ce format exact:
{{"latitude": number, "longitude": number, "formatted_address": "string"}}

Si tu ne peux pas trouver les coordonnees, utilise des coordonnees approximatives pour la ville ou le pays mentionne."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        import json
        import re
        
        text = response.text or ""
        json_match = re.search(r'\{[^{}]+\}', text)
        if json_match:
            coords = json.loads(json_match.group())
            return jsonify(coords)
        else:
            return jsonify({'error': 'Impossible de parser les coordonnees'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-location', methods=['POST'])
def analyze_location():
    if not client:
        return jsonify({'error': 'Cle API non configuree'}), 500
    
    try:
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')
        
        prompt = f"""Tu es un guide touristique expert. Pour les coordonnees GPS suivantes:
Latitude: {lat}
Longitude: {lng}

Donne-moi des informations interessantes sur cet endroit:
1. Quel lieu/ville/pays se trouve a ces coordonnees?
2. Quels sont les points d'interet a proximite?
3. Une anecdote historique ou culturelle interessante sur cet endroit.

Reponds de maniere concise et informative en francais."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        return jsonify({'analysis': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
