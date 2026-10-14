cmake_minimum_required(VERSION 3.15)
project(PokemonSpinner)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(cpr CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

add_executable(getpokes main.cpp)
target_link_libraries(getpokes PRIVATE cpr::cpr nlohmann_json::nlohmann_json)