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
def fetch_fide_data(fide_number):
    try:
        result = subprocess.run(
            ["fide-ratings-scraper", "get", "info", str(fide_number)],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return data
    except subprocess.CalledProcessError as e:
        print(f"Command error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON. Check if the command's output is valid JSON.")
        return None

# Full function to fetch historical FIDE data of top 10 players 
def fetch_fide_data_with_history(fide_number):
    try:
        info_result = subprocess.run(
            ["fide-ratings-scraper", "get", "info", str(fide_number)],
            capture_output=True,
            text=True,
            check=True
        )
        player_info = json.loads(info_result.stdout)

        history_result = subprocess.run(
            ["fide-ratings-scraper", "get", "history", str(fide_number)],
            capture_output=True,
            text=True,
            check=True
        )
        history_data = json.loads(history_result.stdout)

        if isinstance(history_data, list):
            records = history_data  
        elif isinstance(history_data, dict) and "history" in history_data:
            records = history_data["history"]  
        else:
            print(f"Unexpected format for historical data: {history_data}")
            return []

        combined_data = []
        for record in records:
            combined_data.append({
                'fide_id': fide_number,
                'name': player_info.get('name', ''),
                'federation': player_info.get('federation', ''),
                'world_rank_active_players': player_info.get('world_rank_active_players', ''),
                'date': record.get('date', ''),
                'standard': record.get('standard', None),
                'rapid': record.get('rapid', None),
                'blitz': record.get('blitz', None)
            })
        return combined_data

    except subprocess.CalledProcessError as e:
        print(f"Command error for FIDE ID {fide_number}: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return []

    except json.JSONDecodeError:
        print(f"Failed to decode JSON for FIDE ID {fide_number}. Check the command's output.")
        return []

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
