#include <cpr/cpr.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <future>
#include <algorithm>
#include <nlohmann/json.hpp>

using namespace std;
using namespace cpr;
using json = nlohmann::json;

string capitalizeStr(string str);
vector<json> getAllMons(string api);

    int main() {     
        string POKE_API = "https://pokeapi.co/api/v2/";
        auto all_mons = getAllMons(POKE_API);

        // Write data into pokemon_data.json
        ofstream file("pokemon_data.json");
        if (file.is_open()) {
            file << json(all_mons).dump(4);
            file.close();
            cout << "Wrote " << all_mons.size() << " Pokemon to pokemon_data.json" << endl; 
        } else {
            cerr << "Error: Could not open the JSON file for writing." << endl;
        }

        return 0;
    }

    string capitalizeStr(string str) {
        if (!str.empty()) {
            str[0] = toupper(str[0]);
            for (size_t i = 1; i < str.length(); ++i) {  // Check the rest of the string
                if (str[i - 1] == ' ') {
                    str[i] = toupper(str[i]);  // Capitalize if the previous character was a space
                } else {
                    str[i] = tolower(str[i]);  // Otherwise, lowercase it
                }
            }
        }
        return str;
    }

vector<json> getAllMons(string api) {
    string all_mons_url = api + "pokemon?limit=1025&offset=0";
    auto r = Get(Url{all_mons_url}, Header{{"User-Agent", "PokemonSpinner/1.0"}});
    vector<json> all_pokemon_list;

    if (r.status_code == 200) {
        json payload = json::parse(r.text);
        auto results = payload["results"];

        // Use cpr::AsyncResponse to hold the asynchronous requests
        vector<cpr::AsyncResponse> futures;
        futures.reserve(results.size());

        // 1. Launch all asynchronous requests at once
        for (auto& mon : results) {
            futures.push_back(cpr::GetAsync(
                cpr::Url{mon["url"]},
                Header{{"User-Agent", "PokemonSpinner/1.0"}}
            ));
        }

        // 2. Gather responses as they finish
        for (size_t i = 0; i < results.size(); ++i) {
            cpr::Response tr = futures[i].get();
            if (tr.status_code == 200) {
                json poke = json::parse(tr.text);
                vector<string> types;
                string type1 = capitalizeStr(poke["types"][0]["type"]["name"]);
                types.push_back(type1);

                if (poke["types"].size() > 1) {
                    string type2 = capitalizeStr(poke["types"][1]["type"]["name"]);
                    types.push_back(type2);
                }

                cout << "Types added: [";
                for (size_t j = 0; j < types.size(); ++j) {
                    cout << types[j] << (j + 1 < types.size() ? ", " : "");
                }
                cout << "]" << endl;

                // Extract ID from URL
                string cleanUrl = results[i]["url"];
                if (!cleanUrl.empty() && cleanUrl.back() == '/') {
                    cleanUrl.pop_back();
                }
                size_t lastSlash = cleanUrl.find_last_of('/');
                int pokeID = stoi(cleanUrl.substr(lastSlash + 1));

                string pokeName = results[i]["name"];
                for (char &ch : pokeName) {
                    if (pokeName.find(ch)) {
                        if (ch == '-' && !pokeName.find(ch) == pokeName.length() - 2) {
                            ch = ' ';  // Protects mons like Nidoran-F while editing others like Iron Hands
                        }
                    }
                }
                pokeName = capitalizeStr(pokeName);
                cout << "Pokemon added: " << pokeName << endl;

                // Construct JSON object
                json pokemonInfo = {
                    {"id", pokeID},
                    {"name", pokeName},
                    {"types", types}
                };
                all_pokemon_list.push_back(pokemonInfo);
            }
        }
    }
    return all_pokemon_list;
}