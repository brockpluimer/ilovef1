import pandas as pd
import streamlit as st

@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

# Load the color data
color_data = load_csv('driver_colors.csv')

def get_driver_color(driver_name, year, results_df):
    """
    Get the color for a driver based on their name, year, and the results DataFrame.
    
    :param driver_name: The name of the driver
    :param year: The year of the race
    :param results_df: The results DataFrame containing driver and constructor information
    :return: The color code for the driver
    """
    # Split the driver name, but use the whole name if it can't be split
    name_parts = driver_name.split('_')
    last_name = name_parts[-1].capitalize()
    first_name = name_parts[0].capitalize() if len(name_parts) > 1 else ''

    # Find the matching row in the color data
    matching_rows = color_data[(color_data['Year'] == year) & 
                               (color_data['Last Name'].str.lower() == last_name.lower())]
    
    if not matching_rows.empty:
        return matching_rows.iloc[0]['Color']
    
    # If no exact match found, try to find the color based on the constructor
    try:
        constructor = results_df[results_df['driver'].str.lower() == driver_name.lower()]['constructor'].iloc[0]
        constructor_rows = color_data[(color_data['Year'] == year) & 
                                      (color_data['Last Name'].str.lower() == constructor.lower())]
        
        if not constructor_rows.empty:
            return constructor_rows.iloc[0]['Color']
    except IndexError:
        pass  # If constructor is not found, continue to default color

    # If still no match, return a default color
    return '#808080'  # Default to gray

def load_team_colors():
    """Load team colors from CSV file."""
    return load_csv('f1_team_colors.csv').set_index('Team Name')