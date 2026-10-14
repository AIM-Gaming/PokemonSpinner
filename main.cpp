#include <cpr/cpr.h>
#include <iostream>
#include <vector>
#include <nlohmann/json.hpp>

using namespace std;
using namespace cpr;
using json = nlohmann::json;

    int main() {     
        string POKE_API = "https://pokeapi.co/api/v2/";
        auto all_mons = getAllMons(POKE_API);
        return 0;
    }

    string capitalizeStr(string str) {
        if (!str.empty()) {
            str[0] = toupper(str[0]);
            for (size_t i = 1; i < str.length(); ++i) {
                str[i] = tolower(str[i]);
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
            for (auto& mon : payload["results"]) {
                auto tr = Get(
                    Url{mon["url"]},
                    Header{{"User=Agent", "PokemonSpinner/1.0"}}
                );
                if (tr.status_code == 200){
                    json poke = json::parse(tr.text);
                    vector<string> types;
                    string type1 = poke["types"][0]["type"]["name"];
                    types.push_back(type1);

                    if (poke["types"].size() > 1) {
                        string type2 = poke["types"][1]["type"]["name"];
                        types.push_back(type2);
                    }

                    cout << "Types added: [";
                    for (size_t i = 0; i < types.size(); ++i) {
                        cout << types[i] << (i + 1 < types.size() ? ", " : "");
                    }
                    cout << "]" << endl;

                    // Extract ID from URL
                    string cleanUrl = mon["url"];
                    if(!cleanUrl.empty() && cleanUrl.back() == '/') {
                        cleanUrl.pop_back();
                    }
                    size_t lastSlash = cleanUrl.find_last_of('/');
                    int pokeID = stoi(cleanUrl.substr(lastSlash + 1));

                    string pokeName = capitalizeStr(mon["name"]);
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