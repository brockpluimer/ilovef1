import os
import pandas as pd

def get_years():
    """Get all available years in descending order."""
    return sorted([int(year) for year in os.listdir('race_data') if year.isdigit()], reverse=True)

def get_grand_prix(year):
    """Get all available Grand Prix for a given year."""
    year_path = f'race_data/{year}'
    gp_folders = sorted([folder for folder in os.listdir(year_path) if folder.startswith('round_')])
    gp_list = [f"Round {folder.split('_')[1]} -- {' '.join(folder.split('_')[2:-1] if folder.endswith('grand_prix') else folder.split('_')[2:])}" for folder in gp_folders]
    return sorted(gp_list, key=lambda x: int(x.split(' -- ')[0].split(' ')[1]))

def format_status(status):
    """Format race status."""
    if status == 'Finished' or status.startswith('+'):
        return status
    else:
        return f"DNF -- {status}"