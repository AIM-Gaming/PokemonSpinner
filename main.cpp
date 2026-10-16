#include <cpr/cpr.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <future>
#include <algorithm>
#include <nlohmann/json.hpp>
#include <cctype>
#include <unordered_map>

using namespace std;
using namespace cpr;
using json = nlohmann::json;

string capitalizeStr(string str);
vector<json> getAllMons(string api);

    int main() { 
        try {
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
        } catch (const exception& e) {
            cerr << "Fatal: " << e.what() << endl;
            return 1;
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

    int idFromUrl(string url) {
        if (!url.empty() && url.back() == '/') url.pop_back();
        return stoi(url.substr(url.find_last_of('/') + 1));
    }

    string formatGeneration(const string& raw) {
        size_t dash = raw.rfind('-');
        if (dash == string::npos) return capitalizeStr(raw);

        string word = capitalizeStr(raw.substr(0, dash));  // "Generation"
        string numeral = raw.substr(dash + 1);  // "iv"
        for (char& c : numeral) {
            c = toupper(static_cast<unsigned char>(c));  // "IV"
        }
        return word + " " + numeral;  // "Generation IV"
    }

    string prettyName(const string& raw) {
        static const unordered_map<string, string> special = {
            {"nidoran-f", "Nidoran-F"}, {"nidoran-m", "Nidoran-M"},
            {"ho-oh", "Ho-Oh"},         {"porygon-z", "Porygon-Z"},
            {"jangmo-o", "Jangmo-o"},   {"hakamo-o", "Hakamo-o"}, {"kommo-o", "Kommo-o"},
            {"wo-chien", "Wo-Chien"},   {"chien-pao", "Chien-Pao"},
            {"ting-lu", "Ting-Lu"},     {"chi-yu", "Chi-Yu"},
            {"mr-mime", "Mr. Mime"},    {"mr-rime", "Mr. Rime"}, {"mime-jr", "Mime Jr."},
            {"type-null", "Type: Null"},
            {"farfetchd", "Farfetch'd"}, {"sirfetchd", "Sirfetch'd"}
        };

        auto it = special.find(raw);
        if (it != special.end()) return it->second;  // Return the proper name

        // Default: dashes become spaces and each word is capitalized
        string name = raw;
        bool newWord = true;
        for (char& c : name) {
            if (c == '-') {
                c = ' ';
                newWord = true;
            } else {
                c = newWord ? toupper(static_cast<unsigned char>(c))
                            : tolower(static_cast<unsigned char>(c));
                newWord = false;
            }
        }
        return name;
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
        vector<cpr::AsyncResponse> futureGens;
        futures.reserve(results.size());
        futureGens.reserve(results.size());

        // 1. Launch all asynchronous requests at once
        for (auto& mon : results) {
            futures.push_back(cpr::GetAsync(
                cpr::Url{mon["url"]},
                Header{{"User-Agent", "PokemonSpinner/1.0"}}
            ));
            string url = mon["url"];
            string genUrl = api + "pokemon-species/" + to_string(idFromUrl(url));
            futureGens.push_back(cpr::GetAsync(
                cpr::Url{genUrl},
                Header{{"User-Agent", "PokemonSpinner/1.0"}}
            ));
        }

        // 2. Gather responses as they finish
        for (size_t i = 0; i < results.size(); ++i) {
            cpr::Response tr = futures[i].get();
            cpr::Response gr = futureGens[i].get();
            if (tr.status_code == 200 && gr.status_code == 200) {
                json poke = json::parse(tr.text);
                json mon = json::parse(gr.text);

                vector<string> types;
                string type1 = poke["types"][0]["type"]["name"];
                types.push_back(type1);

                if (poke["types"].size() > 1) {
                    string type2 = poke["types"][1]["type"]["name"];
                    types.push_back(type2);
                }

                cout << "Types added: [";
                for (size_t j = 0; j < types.size(); ++j) {
                    cout << types[j] << (j + 1 < types.size() ? ", " : "");
                }
                cout << "]" << endl;

                string gen = formatGeneration(mon["generation"]["name"]);
                bool is_legend = mon["is_legendary"];
                bool is_myth = mon["is_mythical"];
                bool is_baby = mon["is_baby"];

                // Extract ID from URL
                string cleanUrl = results[i]["url"];
                if (!cleanUrl.empty() && cleanUrl.back() == '/') {
                    cleanUrl.pop_back();
                }
                int pokeID = idFromUrl(results[i]["url"]);

                string pokeName = prettyName(mon["name"]);
                cout << "Pokemon added: " << pokeName << endl;

                // Construct JSON object
                json pokemonInfo = {
                    {"id", pokeID},
                    {"name", pokeName},
                    {"types", types},
                    {"generation", gen},
                    {"legendary", is_legend},
                    {"mythical", is_myth},
                    {"baby", is_baby}, 
                };
                all_pokemon_list.push_back(pokemonInfo);
            }
        }
    }
    return all_pokemon_list;
}