# SWSEARCH

A simple cli-tool to show which StarWars characters are associated with a search term.

This tool uses `https://swapi.dev/api` as a data source. An can take a single search term.
The tool will search for all partial mathces of the search term across all api endpoints.
The tool will print all search results, alongside a list of People assoicated with each resource found. 

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


# High Volume Production Environment

I went for Python with this tool, but given time and resources
in a high volume production environment I would opt for a more performant language for a implementation - I would naturally go towards
Java for this.
In this tool I make a many single calls to the api and reasoned the time taken to fetch all resources and reason about the data
was in general a slower process than the fewer calls I would make in most of the "almost complete" searches.
I would probably use mongo for a data storage and look into using solr search for opimising search performance.

