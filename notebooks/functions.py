# Importing necessary packages
import os
import json
import requests
import pandas as pd
import numpy as np
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import sqlite3

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

# NB04 - Data Visualization
def create_line_graph_popularity(name, country, date, player_search, country_search):
    data = pd.DataFrame({
        'Date': pd.to_datetime(date),
        f"{name}'s search": player_search,
        f"{country}'s search": country_search
    })
    data_melted = data.melt(id_vars=['Date'], var_name='Search Type', value_name='Search Volume')

    correlation = np.corrcoef(player_search, country_search)[0, 1] # Calculate correlation

    fig = px.line(
        data_melted, x='Date', y='Search Volume', color='Search Type',
        title=f"{name}'s Popularity Graph",
        labels={'Search Volume': 'Search Volume', 'Date': 'Date'},
        template="plotly_white" 
    )

    fig.add_annotation(
        x=data['Date'].iloc[len(data) // 3], 
        y=max(player_search) * 0.9,
        text=f"Correlation: {correlation:.2f}",
        showarrow=False,
        font=dict(size=14, color="blue"),
        bgcolor="white"
    )
    if name == "Magnus Carlsen":
        win_dates = ["2013-11-01","2014-11-01","2016-11-01","2018-11-01","2021-12-01"]
        win_label = ["1st WC","2nd WC","3rd WC","4th WC","5th WC"]
        for x in range(len(win_dates)):
            if x == 0:
                height = 100
            else:
                height = 50
            fig.add_annotation(
                    x= str(win_dates[x]),
                    y=height,
                    text=win_label[x],
                    showarrow=True,
                    arrowhead=2,
                    ax=0, ay=-40, 
                    textangle = -45,
                )
            fig.add_annotation(
                x = "2023-01-01",
                y = 40,
                text="Doesn't defend",
                showarrow=True,
                arrowhead=2,
                ax=30, ay=-40,  
            )
        fig.write_html("../docs/plots/magnus_gtrends_plot.html", full_html=False) # saving wanted plot as html file for website usasge
    fig.show()

def player_info_returner(name,country_code):
    conn = sqlite3.connect("../data/chess.db")
    cursor = conn.cursor()


    country = cursor.execute(f"SELECT date, search_rate FROM country_gtrends WHERE country = '{country_code}'").fetchall()
    player = cursor.execute(f"SELECT date, search_rate FROM players_gtrends WHERE name='{name}'").fetchall()

    dates = [date[0] for date in country]
    dates = pd.to_datetime(dates, format="%b %Y")
    country_search=[rate[1] for rate in country]
    player_search=[rate[1] for rate in player[:-1]]

    conn.close()
    return dates,country_search,player_search

# NB05 - Data Visualization Pt. 2

def create_line_graph_popularity(name, date, player_search, fide_rating):
    player_search = (player_search - np.min(player_search)) / (np.max(player_search) - np.min(player_search))
    fide_rating = (fide_rating - np.min(fide_rating)) / (np.max(fide_rating) - np.min(fide_rating))
    
    data = pd.DataFrame({
        'Date': pd.to_datetime(date),
        f"{name}'s search volume (normalized)": player_search,
        f"{name}'s FIDE rating (normalized)": fide_rating
    })

    data_melted = data.melt(id_vars=['Date'], var_name='Metric', value_name='Value')

    fig = px.line(
        data_melted, x='Date', y='Value', color='Metric',
        title=f"{name}'s Popularity vs. FIDE Rating (Normalized)",
        labels={'Value': 'Normalized Value', 'Date': 'Date'},
        template="plotly_white"
    )
    if name == "Yi Wei":
        fig.write_html("../docs/plots/Yi_Wei_Pop_to_Fide_plot.html", full_html=False)
    fig.show()

def player_info_returner(name):
    conn = sqlite3.connect("../data/chess.db")
    cursor = conn.cursor()

    player = cursor.execute(
        f"SELECT date, search_rate FROM players_gtrends WHERE name='{name}'"
    ).fetchall()

    fide = cursor.execute(
        f"SELECT date, standard FROM fide WHERE name='{name}'"
    ).fetchall()

    conn.close()
    

    df_search = pd.DataFrame(player, columns=['Date', 'Search Volume'])
    df_fide = pd.DataFrame(fide, columns=['Date', 'FIDE Rating'])
    
    df_search['Date'] = pd.to_datetime(df_search['Date'], format='%b %Y')
    df_fide['Date'] = pd.to_datetime(df_fide['Date'], format='%b %Y')
    
    df = pd.merge(df_search, df_fide, on='Date', how='outer').sort_values(by='Date')
    
    return df['Date'], df['Search Volume'].fillna(0), df['FIDE Rating'].ffill()

players = [
    'Magnus Carlsen', 'Fabiano Caruana', 'Hikaru Nakamura', 'Arjun Erigaisi',
    'Gukesh Dommaraju', 'Nodirbek Abdusattorov', 'Alireza Firouzja',
    'Ian Nepomniachtchi', 'Yi Wei', 'Viswanathan Anand'
]

def create_line_graph_popularity(name, date, player_search, fide_standard, fide_rapid, fide_blitz):
    player_search = (player_search - np.min(player_search)) / (np.max(player_search) - np.min(player_search))
    fide_standard = (fide_standard - np.min(fide_standard)) / (np.max(fide_standard) - np.min(fide_standard))
    fide_rapid = (fide_rapid - np.min(fide_rapid)) / (np.max(fide_rapid) - np.min(fide_rapid))
    fide_blitz = (fide_blitz - np.min(fide_blitz)) / (np.max(fide_blitz) - np.min(fide_blitz))
    
    data = pd.DataFrame({
        'Date': pd.to_datetime(date),
        f"{name}'s search volume (normalized)": player_search,
        f"{name}'s FIDE standard rating (normalized)": fide_standard,
        f"{name}'s FIDE rapid rating (normalized)": fide_rapid,
        f"{name}'s FIDE blitz rating (normalized)": fide_blitz
    })

    data_melted = data.melt(id_vars=['Date'], var_name='Metric', value_name='Value')

    fig = px.line(
        data_melted, x='Date', y='Value', color='Metric',
        title=f"{name}'s Popularity vs. FIDE Ratings (Normalized)",
        labels={'Value': 'Normalized Value', 'Date': 'Date'},
        template="plotly_white"
    )

    fig.show()

def player_info_returner(name):
    conn = sqlite3.connect("../data/chess.db")
    cursor = conn.cursor()

    player = cursor.execute(
        f"SELECT date, search_rate FROM players_gtrends WHERE name='{name}'"
    ).fetchall()
    
    fide = cursor.execute(
        f"SELECT date, standard, rapid, blitz FROM fide WHERE name='{name}'"
    ).fetchall()

    conn.close()
    

    df_search = pd.DataFrame(player, columns=['Date', 'Search Volume'])
    df_fide = pd.DataFrame(fide, columns=['Date', 'FIDE Standard', 'FIDE Rapid', 'FIDE Blitz'])
    
    df_search['Date'] = pd.to_datetime(df_search['Date'], format='%b %Y')
    df_fide['Date'] = pd.to_datetime(df_fide['Date'], format='%b %Y')
    
    df = pd.merge(df_search, df_fide, on='Date', how='outer').sort_values(by='Date')
    
    return df['Date'], df['Search Volume'].fillna(0), df['FIDE Standard'].ffill(), df['FIDE Rapid'].ffill(), df['FIDE Blitz'].ffill()

def create_line_graph_fide_ratings(name, date, fide_standard, fide_rapid, fide_blitz):
    data = pd.DataFrame({
        'Date': pd.to_datetime(date),
        f"{name}'s FIDE standard rating": fide_standard,
        f"{name}'s FIDE rapid rating": fide_rapid,
        f"{name}'s FIDE blitz rating": fide_blitz
    })

    data_melted = data.melt(id_vars=['Date'], var_name='Metric', value_name='Value')

    fig = px.line(
        data_melted, x='Date', y='Value', color='Metric',
        title=f"{name}'s FIDE Ratings Over Time",
        labels={'Value': 'Rating', 'Date': 'Date'},
        template="plotly_white"
    )
    if name == "Alireza Firouzja":
        fig.write_html("../docs/plots/Alireza_multi_rating_plot.html", full_html=False)
    fig.show()

def player_info_returner(name):
    conn = sqlite3.connect("../data/chess.db")
    cursor = conn.cursor()

    fide = cursor.execute(
        f"SELECT date, standard, rapid, blitz FROM fide WHERE name='{name}'"
    ).fetchall()

    conn.close()

    df_fide = pd.DataFrame(fide, columns=['Date', 'FIDE Standard', 'FIDE Rapid', 'FIDE Blitz'])
    df_fide['Date'] = pd.to_datetime(df_fide['Date'], format='%b %Y')
    df_fide = df_fide.sort_values(by='Date')
    
    return df_fide['Date'], df_fide['FIDE Standard'].ffill(), df_fide['FIDE Rapid'].ffill(), df_fide['FIDE Blitz'].ffill()
