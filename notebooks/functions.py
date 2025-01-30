# Importing necessary packages
import os
import json
import requests
import pandas as pd
import numpy as np
import subprocess

from serpapi import GoogleSearch

from dotenv import load_dotenv

from tqdm.notebook import tqdm
tqdm.pandas()

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
