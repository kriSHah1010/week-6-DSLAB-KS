import requests
import pandas as pd
from typing import List, Dict, Union

class Genius:
    BASE_URL = "https://api.genius.com"

    # --- Exercise 1: Initialization ---
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    # --- Helper Method ---
    def _api_request(self, path: str, params: Dict[str, str] = None) -> Union[Dict, None]:
        url = f"{self.BASE_URL}{path}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Error for URL: {url}")
            print(f"Error: {e}")
            return None

    # --- Exercise 2: Get a single artist's details ---
    def get_artist(self, search_term: str) -> Union[Dict, None]:
        print(f"--- Searching for Artist: '{search_term}' ---")
        
        # 1. Search for the artist to get the ID
        search_params = {"q": search_term}
        search_data = self._api_request(
            path="/search", 
            params=search_params
        )

        if not search_data or not search_data['response']['hits']:
            print(f"Artist '{search_term}' not found.")
            return None

        try:
            # 2. Extract the Artist ID from the first hit
            first_hit = search_data['response']['hits'][0]
            artist_id = first_hit['result']['primary_artist']['id']
            print(f"Found Artist ID: {artist_id} (Artist: {first_hit['result']['primary_artist']['name']})")

            # 3. Use the Artist ID to pull full artist information
            artist_path = f"/artists/{artist_id}"
            artist_data = self._api_request(path=artist_path)
            
            # 4. Return the resulting JSON object
            if artist_data:
                return artist_data

        except (KeyError, IndexError) as e:
            print(f"Error parsing search JSON for '{search_term}': {e}")
            return None
            
        return None

    # --- Exercise 3: Get details for multiple artists ---
    def get_artists(self, search_terms: List[str]) -> pd.DataFrame:
        results_list = []
        
        for term in search_terms:
            artist_data = self.get_artist(term)
            
            row = {
                'search_term': term,
                'artist_name': None,
                'artist_id': None,
                'followers_count': None
            }
            
            if artist_data and 'artist' in artist_data['response']:
                artist = artist_data['response']['artist']
                
                row['artist_name'] = artist.get('name', 'N/A')
                row['artist_id'] = artist.get('id', 0)
                row['followers_count'] = artist.get('followers_count', 0)
                
            results_list.append(row)
            print("-" * 20) 

        # Convert the list of dictionaries into a DataFrame
        df = pd.DataFrame(results_list)
        return df
