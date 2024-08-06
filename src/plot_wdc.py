import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from load_data import load_wdc_data
from get_colors import load_team_colors

def plot_wdc_standings(year):
    """Create a plot of WDC standings for a given year using Plotly."""
    data = load_wdc_data(year)
    team_colors = load_team_colors()
    
    if data is None:
        st.error(f"No data available for {year}")
        return
    
    # Get the final round data
    final_round = list(data.keys())[-1]
    final_standings = data[final_round]
    
    # Sort by points in descending order
    final_standings = final_standings.sort_values('Points', ascending=True)
    
    # Create the plot
    fig = go.Figure()
    
    for _, driver in final_standings.iterrows():
        team = driver['Constructor']
        color = team_colors.loc[team, 'Color'] if team in team_colors.index else '#808080'
        fig.add_trace(go.Bar(
            y=[driver['Driver']],
            x=[driver['Points']],
            orientation='h',
            marker_color=color,
            name=driver['Driver'],
            text=f"Points: {driver['Points']}<br>Wins: {int(driver['Wins'])}",
            hoverinfo='text'
        ))
    
    fig.update_layout(
        title=f'{year} World Drivers\' Championship Final Standings',
        xaxis_title='Points',
        yaxis_title='Driver',
        height=800,
        barmode='stack',
        showlegend=False
    )
    
    return fig

def plot_wdc_progression(year):
    """Create a line plot showing the progression of top drivers throughout the season using Plotly."""
    data = load_wdc_data(year)
    team_colors = load_team_colors()
    
    if data is None:
        st.error(f"No data available for {year}")
        return
    
    # Combine data from all rounds
    combined_data = pd.concat([df.assign(Round=round_name) for round_name, df in data.items()])
    
    # Get top 5 drivers from the final round
    final_round = list(data.keys())[-1]
    top_drivers = data[final_round].nlargest(20, 'Points')['Driver'].tolist()
    
    # Filter data for top drivers
    top_driver_data = combined_data[combined_data['Driver'].isin(top_drivers)]
    
    # Create the plot
    fig = go.Figure()
    
    for driver in top_drivers:
        driver_data = top_driver_data[top_driver_data['Driver'] == driver]
        team = driver_data['Constructor'].iloc[0]
        color = team_colors.loc[team, 'Color'] if team in team_colors.index else '#808080'
        fig.add_trace(go.Scatter(
            x=driver_data['Round'],
            y=driver_data['Points'],
            mode='lines+markers',
            name=driver,
            line=dict(color=color),
            hovertemplate='Round: %{x}<br>Points: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        title=f'{year} World Drivers\' Championship Progression',
        xaxis_title='Round',
        yaxis_title='Points',
        height=600,
        legend_title='Drivers',
        hovermode='closest'
    )
    
    return fig

def wdc_visualization_view():
    st.header("World Drivers' Championship Visualizations")
    
    years = sorted([int(f.split('_')[0]) for f in os.listdir('complete_WDC_standings') if f.endswith('.xlsx')], reverse=True)
    selected_year = st.selectbox('Select Year', years)
    
    st.subheader("Final Standings")
    fig_standings = plot_wdc_standings(selected_year)
    st.plotly_chart(fig_standings, use_container_width=True)
    
    st.subheader("Championship Progression")
    fig_progression = plot_wdc_progression(selected_year)
    st.plotly_chart(fig_progression, use_container_width=True)