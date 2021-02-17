# SWSEARCH

A simple cli-tool to show which StarWars characters are associated with a search term.

This tool uses `https://swapi.dev/api` as a data source.
It takes as an input argument a single search term.
The tool will search for all partial matches of the search term across all api endpoints.
The tool will print all search results, alongside a list of People associated with each resource found. 

# Build

The project can be built by running
`make`

This will set up a python venv and install an editable version of the lib.

# How To Run

The python console script can be run with
```
./build/.venv/bin/swsearch --help
```

```
./build/.venv/bin/swsearch "Mill"
```

# Tests

Tests can be run with

`make tests`
