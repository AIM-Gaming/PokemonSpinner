import subprocess
from pathlib import Path
from app import SpinnerApp

LOAD_JSON = False

if __name__ == "__main__":
    if LOAD_JSON:
        output_path = Path(__file__).with_name("pokemon_data.json")

        print("Running C++ backend to fetch Pokemon data")

        result = subprocess.run(
            ["build/Debug/getpokes.exe"],
            capture_output=True,
            text=True
        )
        print("Finished loading pokemon_data.json")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errors: ", result.stderr)
        print(f"Data saved to {output_path}")

    app = SpinnerApp()
    app.run()
    