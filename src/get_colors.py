import pandas as pd
import streamlit as st
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the data directory
data_dir = os.path.join(current_dir, 'data')

# Debug information
st.write(f"Current directory: {current_dir}")
st.write(f"Data directory: {data_dir}")

# Check if data directory exists
if os.path.exists(data_dir):
    st.write(f"Files in data directory: {os.listdir(data_dir)}")
else:
    st.error(f"Data directory does not exist: {data_dir}")
    st.write("Current directory contents:", os.listdir(current_dir))

@st.cache_data
def load_csv(file_name):
    try:
        file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(file_path):
            st.error(f"File does not exist: {file_path}")
            return pd.DataFrame()
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading file {file_name}: {str(e)}")
        return pd.DataFrame()

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
    if color_data.empty:
        return '#808080'  # Default to gray if color data couldn't be loaded
    
    # Split the driver name, but use the whole name if it can't be split
    name_parts = driver_name.split('_')
    last_name = name_parts[-1].capitalize()
    
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

# More debug information
st.write(f"Color data loaded: {not color_data.empty}")
st.write(f"Color data shape: {color_data.shape if not color_data.empty else 'N/A'}")
team_colors = load_team_colors()
st.write(f"Team colors loaded: {not team_colors.empty}")
st.write(f"Team colors shape: {team_colors.shape if not team_colors.empty else 'N/A'}")