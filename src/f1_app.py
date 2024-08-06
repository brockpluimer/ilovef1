import streamlit as st
import pandas as pd
import os

# Function to get all available years
def get_years():
    return sorted([int(year) for year in os.listdir('race_data') if year.isdigit()])

# Function to get all available Grand Prix for a given year
def get_grand_prix(year):
    year_path = f'race_data/{year}'
    gp_folders = sorted([folder for folder in os.listdir(year_path) if folder.startswith('round_')])
    gp_list = [f"Round {folder.split('_')[1]} -- {' '.join(folder.split('_')[2:-1] if folder.endswith('grand_prix') else folder.split('_')[2:])}" for folder in gp_folders]
    return sorted(gp_list, key=lambda x: int(x.split(' -- ')[0].split(' ')[1]))

# Function to load results
def load_results(year, grand_prix, result_type):
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
        st.error(f"File not found: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    return df

# Function to format race status
def format_status(status):
    if status == 'Finished' or status.startswith('+'):
        return status
    else:
        return f"DNF -- {status}"

# Streamlit app
st.title('F1 Results Viewer')

# Year selection
years = get_years()
selected_year = st.selectbox('Select Year', years)

# Grand Prix selection
grand_prix_list = get_grand_prix(selected_year)
selected_gp = st.selectbox('Select Grand Prix', grand_prix_list, index=0)

# Result type selection
result_type = st.radio("Select Result Type", ['Race', 'Qualifying', 'Sprint'])

# Load and display results
results = load_results(selected_year, selected_gp, result_type)

if results is not None:
    st.header(f'{selected_year} {selected_gp} {result_type} Results')
    
    if result_type == 'Race' or result_type == 'Sprint':
        for _, row in results.iterrows():
            col1, col2, col3, col4 = st.columns([1, 2, 2, 3])
            
            with col1:
                st.write(f"**P{row['position']}**")
            
            with col2:
                st.write(f"**{row['driver']}**")
                st.write(f"*{row['constructor']}*")
            
            with col3:
                st.write(f"Start: P{row['grid']}")
                st.write(f"Laps: {row['laps']}")
            
            with col4:
                status = format_status(row['status'])
                st.write(f"Status: {status}")
                st.write(f"Points: {int(row['points'])}")
            
            st.markdown("---")
    
    elif result_type == 'Qualifying':
        qualifying_sessions = [col for col in results.columns if col.startswith('Q')]
        if qualifying_sessions:
            selected_session = st.selectbox("Select Qualifying Session", qualifying_sessions)
            
            for _, row in results.iterrows():
                col1, col2, col3 = st.columns([1, 2, 3])
                
                with col1:
                    st.write(f"**P{row['position']}**")
                
                with col2:
                    st.write(f"**{row['driver']}**")
                    st.write(f"*{row['constructor']}*")
                
                with col3:
                    st.write(f"{selected_session}: {row.get(selected_session, 'N/A')}")
                
                st.markdown("---")
        else:
            st.error("No qualifying session data available.")

else:
    if result_type == 'Qualifying':
        st.error("No Qualifying data available. Qualifying data aren't available until Round 17 of 2002 at the Japanese Grand Prix.")
    elif result_type == 'Sprint':
        st.error("No sprint data available. Sprint races started in 2021, Round 10 at the British Grand Prix. Only select races use them since then.")
    else:
        st.error("No data available for the selected race.")