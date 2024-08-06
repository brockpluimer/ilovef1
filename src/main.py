import streamlit as st
from utils import get_years, get_grand_prix
from load_data import load_results, load_lap_times_data, load_wdc_data
from get_colors import get_driver_color, load_team_colors
from plot_wdc import wdc_visualization_view, plot_wdc_progression, plot_wdc_standings
from race_data import race_results_view, lap_times_view, create_race_chart

def main():
    st.set_page_config(page_title="F1 Results Viewer", layout="wide")
    
    st.title('F1 Results Viewer and Data Visualizer')
    
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose the mode",
                                ["Race Results", "Lap Times Visualization", "WDC Standings"])
    
    # Year selection
    years = get_years()
    selected_year = st.sidebar.selectbox('Select Year', years)

    if app_mode in ["Race Results", "Lap Times Visualization"]:
        # Grand Prix selection
        grand_prix_list = get_grand_prix(selected_year)
        selected_gp = st.sidebar.selectbox('Select Grand Prix', grand_prix_list, index=0)
        
        if app_mode == "Race Results":
            st.header("Race Results")
            result_type = st.radio("Select Result Type", ['Race', 'Qualifying', 'Sprint'])
            race_results_view(selected_year, selected_gp, result_type)
        elif app_mode == "Lap Times Visualization":
            st.header("Lap Times Visualization")
            lap_times_view(selected_year, selected_gp)
    elif app_mode == "WDC Standings":
        wdc_visualization_view()

if __name__ == "__main__":
    main()