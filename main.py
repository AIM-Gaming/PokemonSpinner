import json
from pathlib import Path

import getmons

if __name__ == "__main__":
    mons = getmons.get_all_mons()
    output_path = Path(__file__).with_name("pokemon_data.json")

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(mons, file, indent=4)

    print(f"Done! Wrote {len(mons)} Pokémon to {output_path}")