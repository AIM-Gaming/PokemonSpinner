import json
import subprocess
from pathlib import Path

import getmons

if __name__ == "__main__":
    output_path = Path(__file__).with_name("pokemon_data.json")

    # with output_path.open("w", encoding="utf-8") as file:
    #     json.dump(mons, file, indent=4)

    # print(f"Done! Wrote {len(mons)} Pokémon to {output_path}")