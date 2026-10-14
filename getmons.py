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
    all_mons = POKE_API + "pokemon?limit=1025&offset=0"
    mon_request = Request(all_mons, headers={"User-Agent": "PokemonSpinner/1.0"})

    with urlopen(mon_request) as response:
        payload = json.loads(response.read().decode("utf-8"))  # Bruh I'm never using Agent mode again

    mon_results = payload["results"]
    for mon in mon_results:
        type_request = Request(mon["url"], headers={"User-Agent": "PokemonSpinner/1.0"})
        with urlopen(type_request) as resp:
            poke = json.loads(resp.read().decode("utf-8"))
        types = []
        type1 = poke["types"][0]["type"]["name"]
        types.append(type1)
        if len(poke["types"]) > 1:
            type2 = poke["types"][1]["type"]["name"]
            types.append(type2)
        print(f"Types added: {types}")
        pokemon_info = {
            "id": int(mon["url"].rstrip("/").split("/")[-1]),
            "name": mon["name"].capitalize(),
            "types": types
        }
        print(f"Pokemon added: {pokemon_info["name"]}")
    return pokemon_info