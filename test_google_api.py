import os
import urllib.request
import urllib.error
import json

def test_google_api_key():
    api_key = os.environ.get('GOOGLE_API_KEY')
    
    if not api_key:
        print("Erreur: La cle API n'est pas configuree.")
        print("Veuillez ajouter votre cle API comme secret avec le nom 'GOOGLE_API_KEY'")
        return False
    
    print("Test de votre cle API Google...")
    print("-" * 40)
    
    test_url = f"https://www.googleapis.com/discovery/v1/apis?key={api_key}"
    
    try:
        req = urllib.request.Request(test_url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if 'items' in data:
                print("Succes! Votre cle API fonctionne correctement.")
                print(f"Nombre d'APIs Google disponibles: {len(data['items'])}")
                print("\nQuelques APIs accessibles:")
                for api in data['items'][:5]:
                    print(f"  - {api.get('title', 'N/A')}")
                return True
            else:
                print("Reponse inattendue de l'API.")
                return False
                
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print("Erreur 400: Cle API invalide ou mal formatee.")
        elif e.code == 403:
            print("Erreur 403: Cle API non autorisee ou quotas depasses.")
            print("Verifiez que les APIs necessaires sont activees dans la Console Google.")
        else:
            print(f"Erreur HTTP {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"Erreur de connexion: {e.reason}")
        return False
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("  TEST DE CLE API GOOGLE")
    print("=" * 50)
    print()
    test_google_api_key()
    print()
    print("=" * 50)
