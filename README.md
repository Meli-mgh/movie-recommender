# Movie Recommender CLI

A simple Python command-line tool that recommends movies based on genre using the OMDb API.

## Features
- User inputs a movie they like
- Detects the primary genre
- Recommends a random movie from the same genre
- Easily extendable (add IMDb rating filter, plot similarity, etc.)

## Requirements
- Python 3.x
- requests (`pip install requests`)

## Setup
1. Get an OMDb API key: http://www.omdbapi.com/apikey.aspx
2. Set your environment variable:

### for Windows
setx OMDB_KEY "your_real_key"

### for Mac/Linux
export OMDB_KEY="your_real_key"

3. Run the script:
python movie_recommender.py


## Usage
Enter a movie you like: The Matrix
Detected genre: Action
You might also like: Die Hard - 1988