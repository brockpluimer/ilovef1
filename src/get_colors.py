import pandas as pd
import streamlit as st
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the project root
project_root = os.path.dirname(current_dir)
# Construct the path to the data directory
data_dir = os.path.join(project_root, 'data')

# Debug information
st.write(f"Current directory: {current_dir}")
st.write(f"Project root: {project_root}")
st.write(f"Data directory: {data_dir}")

# Check if data directory exists
if os.path.exists(data_dir):
    st.write(f"Files in data directory: {os.listdir(data_dir)}")
else:
    st.error(f"Data directory does not exist: {data_dir}")
    st.write("Current directory contents:", os.listdir(current_dir))
    st.write("Project root contents:", os.listdir(project_root))

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

# ... rest of your code remains the same ...

def load_team_colors():
    """Load team colors from CSV file."""
    return load_csv('f1_team_colors.csv').set_index('Team Name')

# More debug information
st.write(f"Color data loaded: {not color_data.empty}")
st.write(f"Color data shape: {color_data.shape if not color_data.empty else 'N/A'}")
team_colors = load_team_colors()
st.write(f"Team colors loaded: {not team_colors.empty}")
st.write(f"Team colors shape: {team_colors.shape if not team_colors.empty else 'N/A'}")