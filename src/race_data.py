import streamlit as st
import plotly.graph_objects as go
from load_data import load_results, load_lap_times_data
from utils import format_status
from get_colors import get_driver_color

def race_results_view(year, grand_prix, result_type):
    results = load_results(year, grand_prix, result_type)

    if results is not None:
        st.subheader(f'{year} {grand_prix} {result_type} Results')
        
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

def create_race_chart(df, year, race_name, results_df):
    """Create a race chart using Plotly."""
    fig = go.Figure()
    
    for driver in df['driver'].unique():
        driver_data = df[df['driver'] == driver].sort_values('lap')
        try:
            color = get_driver_color(driver, int(year), results_df)
        except Exception as e:
            st.error(f"Error getting color for {driver}: {str(e)}")
            color = '#808080'  # Default to gray if there's an error
        
        fig.add_trace(go.Scatter(
            x=driver_data['lap'],
            y=driver_data['position'],
            mode='lines',
            name=driver,
            line=dict(color=color),
            hovertemplate=(
                f"Driver: {driver}<br>"
                "Lap: %{x}<br>"
                "Position: %{y}<br>"
                "Time: %{text}<extra></extra>"
            ),
            text=driver_data['time']
        ))
    
    fig.update_layout(
        title=f"Race Positions - {year} {race_name}",
        xaxis_title="Lap",
        yaxis_title="Position",
        yaxis_autorange='reversed',
        legend_title="Drivers",
        height=800,
        hovermode="closest"
    )
    
    return fig

def lap_times_view(year, grand_prix):
    lap_times_data = load_lap_times_data(year, grand_prix)
    
    if lap_times_data is not None:
        race_results = load_results(year, grand_prix, 'Race')
        
        if race_results is not None:
            fig = create_race_chart(lap_times_data, year, grand_prix.split(' -- ')[1], race_results)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No race results available for color mapping.")
    else:
        st.error("No lap times data available for the selected race.")