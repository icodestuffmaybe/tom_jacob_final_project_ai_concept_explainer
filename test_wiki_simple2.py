import requests
import urllib.parse

def test_wikipedia_direct():
    print("Testing Wikipedia API directly")
    print("=" * 40)
    
    test_terms = ["embeddings", "Vector_Representation", "photosynthesis", "machine_learning"]
    
    for term in test_terms:
        print(f"\nTesting: '{term}'")
        
        # Test direct Wikipedia API
        encoded_term = urllib.parse.quote(term.replace(' ', '_'))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_term}"
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', 'No title')
                extract = data.get('extract', 'No extract')
                print(f"Found: {title}")
                print(f"Extract: {extract[:100]}...")
            else:
                print(f"Failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_wikipedia_direct()