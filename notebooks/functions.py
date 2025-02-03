# Importing necessary packages
import os
import json
import requests
import pandas as pd
import numpy as np
import subprocess
import time

from serpapi import GoogleSearch

from dotenv import load_dotenv

from tqdm.notebook import tqdm
tqdm.pandas()

# NB01 - Data Collection
# FIDE Data
# Test function to see if the rating scraper works


# Google Trends Data
# Pulls key from .env 
SERPAPI_KEY = os.getenv("serpapi_key")

# Fetches Google Trends data since 2004 for a given keyword and country code and saves it to a JSON file.
def fetch_google_trends(country_code, keyword, destination, SERPAPI_KEY):    
    # destination is used to craft the file name and where the file is saved

    # Keeps the file names uniform - changing artist_name from here on
    keyword_filename = keyword

    # Replace underscores with spaces in the artist's name
    keyword = keyword_filename.replace("_", " ")
    
    # Parameters for the API call
    params = {
        "engine": "google_trends",
        "q": keyword,
        "data_type": "TIMESERIES",
        "date": "all",  # Specify the time range
        "api_key": SERPAPI_KEY , # Replace with your SerpAPI key
        "geo": country_code , 
    }
    
    # Fetch data using SerpAPI
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Extract 'interest_over_time' section
    interest_over_time = results.get("interest_over_time", {})
    
    # Define the output file path
    output_path = f"../data/{destination}/{keyword}_{country_code}_{destination}.json"

    # Save the data as a JSON file
    with open(output_path, "w") as file:
        json.dump(interest_over_time, file, indent=4)
    
    return print(f"Google Trends data successfully saved to {output_path}")

# Function to extract required paramters from Gtrends of players
def gtrends_players(name,country):
    file_path = f'../data/GTrends_Player/{name}_{country}_GTrends_Player.json'
    combined_data=[]
    with open(file_path, 'r', encoding='utf-8') as filepath:   
        data = json.load(filepath)
    for time_data in data['timeline_data']:
        date= time_data.get("date")
        for values in time_data['values']:
            combined_data.append({
                "name":name,
                "country":country,
                "date":date,
                "search_rate":values["extracted_value"]
            })
    return combined_data

# Function to extract required parameters from Gtrends of Countries
def gtrends_country(country):
    file_path = f'../data/GTrends_Country/Chess_{country}_GTrends.json'
    combined_data=[]
    with open(file_path, 'r', encoding='utf-8') as filepath:   
        data = json.load(filepath)
    for time_data in data['timeline_data']:
        date= time_data.get("date")
        for values in time_data['values']:
            combined_data.append({
                "country":country,
                "date":date,
                "search_rate":values["extracted_value"]
            })
    return combined_data

# Chess.com Data
# Function to fetch player stats from Chess.com API
def fetch_chess_com_stats(username):
    url = f"https://api.chess.com/pub/player/{username}/stats"
    
    headers = {
    "User-Agent": "Python script for educational use"
}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        print(f"Access denied for {username}. API may require authentication.")
    else:
        print(f"Failed to fetch data for {username}. Status Code: {response.status_code}")
    
    return None

# Function to fetch all players' stats and store in a DataFrame
def fetch_all_players_stats(players):
    player_stats = []

    for player in players:
        username = player['chess_com_username'] 
        print(f"Fetching data for {player['name']} ({username})...")

        stats = fetch_chess_com_stats(username)

        if stats:
            player_info = {
                'name': player['name'],
                'fide_number': player['fide_number'],
                'chess_com_username': username,
                'country': player['country'],
                'current_classic': stats.get('chess_daily', {}).get('last', {}).get('rating', None),
                'current_blitz': stats.get('chess_blitz', {}).get('last', {}).get('rating', None),
                'current_rapid': stats.get('chess_rapid', {}).get('last', {}).get('rating', None),
            }
            player_stats.append(player_info)
        else:
            print(f"Skipping {username}, no data found.")

        time.sleep(1)

    return pd.DataFrame(player_stats)
