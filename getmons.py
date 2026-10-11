import json
from typing import Dict, List
from urllib.request import Request, urlopen

'''
    Get the API URL of ALL Pokemon (even the different forms)
    Organize them into different lists (spinners)
    Make a way to choose different spinners (maybe a C# GUI)
'''
POKE_API = "https://pokeapi.co/api/v2/"
pokefile = "pokemon_data.json"


def get_all_mons() -> List[Dict[str, int | str]]:
    all_forms_url = POKE_API + "pokemon?limit=1025&offset=0"
    request = Request(all_forms_url, headers={"User-Agent": "PokemonSpinner/1.0"})

    with urlopen(request) as response:
        payload = json.loads(response.read().decode("utf-8"))  # Bruh I'm never using Agent mode again

    mon_results = payload["results"]
    pokemon_info = [
        {
            "id": int(mon["url"].rstrip("/").split("/")[-1]),
            "name": mon["name"].capitalize(),
        }
        for mon in mon_results
    ]
    return pokemon_info