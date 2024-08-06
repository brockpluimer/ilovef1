import os
import pandas as pd
import streamlit as st

def load_results(year, grand_prix, result_type):
    """Load Grand Prix Race results."""
    year_path = f'race_data/{year}'
    round_num = grand_prix.split(' -- ')[0].split(' ')[1]
    gp_name = '_'.join(grand_prix.split(' -- ')[1].lower().split())
    
    if 'indianapolis 500' in grand_prix.lower():
        gp_folder = f"round_{round_num}_indianapolis_500"
        csv_file = f'{year}_indianapolis_500_{result_type.lower()}_results.csv'
    else:
        gp_folder = f"round_{round_num}_{gp_name}_prix"
        csv_file = f'{year}_{gp_name}_prix_{result_type.lower()}_results.csv'
    
    file_path = os.path.join(year_path, gp_folder, csv_file)
    
    if not os.path.exists(file_path):
        return None
    
    df = pd.read_csv(file_path)
    return df

def load_lap_times_data(year, grand_prix):
    """Load lap times data."""
    year_path = f'race_data/{year}'
    round_num = grand_prix.split(' -- ')[0].split(' ')[1]
    gp_name = '_'.join(grand_prix.split(' -- ')[1].lower().split())
    
    if 'indianapolis 500' in grand_prix.lower():
        gp_folder = f"round_{round_num}_indianapolis_500"
        csv_file = f'{year}_indianapolis_500_lap_times.csv'
    else:
        gp_folder = f"round_{round_num}_{gp_name}_prix"
        csv_file = f'{year}_{gp_name}_prix_lap_times.csv'
    
    file_path = os.path.join(year_path, gp_folder, csv_file)
    
    if not os.path.exists(file_path):
        return None
    
    df = pd.read_csv(file_path)
    return df

def load_wdc_data(year):
    """Load WDC standings data for a given year."""
    file_path = f'complete_WDC_standings/{year}_WDC_standings.xlsx'
    if not os.path.exists(file_path):
        return None
    
    # Read all sheets (rounds) from the Excel file
    xls = pd.ExcelFile(file_path)
    sheets = xls.sheet_names
    
    # Create a dictionary to store data from each round
    data = {sheet: pd.read_excel(xls, sheet) for sheet in sheets}
    return data