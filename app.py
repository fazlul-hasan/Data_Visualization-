import folium
import pandas as pd

import matplotlib.pyplot as plt
from ipywidgets import interact, widgets
from IPython.display import display
from flask import Flask, render_template, request

app = Flask(__name__,template_folder='templates')
@app.route("/", methods=['GET', 'POST'])

def index():
    latitude = 40.4637
    longitude = -3.7492

    # Load the data
    data = pd.read_csv('spain_club_data.csv')
    clubs_list = data['club'].unique()  # Get a list of unique clubs for the dropdown

    selected_club = request.args.get('club')  # Get the selected club from the query parameter
    if selected_club:
        # Filter for selected club
        club_data = data[data['club'] == selected_club]
        if not club_data.empty:
            latitude = club_data.iloc[0]['latitude']
            longitude = club_data.iloc[0]['longitude']

    # Create the map
    m = folium.Map(location=[latitude, longitude], zoom_start=6, tiles='OpenStreetMap')

    if selected_club:
        # If a club is selected, show only that club's location
        add_club_marker(m, club_data.iloc[0])
    else:
        # If no club is selected, show all clubs
        for _, row in data.iterrows():
            add_club_marker(m, row)

    # Save the map as HTML and send it to the template
    m = m._repr_html_()

    return render_template('index.html', map=m, clubs=clubs_list, selected_club=selected_club)

def add_club_marker(map_object, row):
    # Helper function to add a marker to the map
    location = [row['latitude'], row['longitude']]
    tooltip_content = f"Club: {row['club']}<br>Stadium Capacity: {row['stadium_capacity']}"
    folium.Marker(
        location=location,
        tooltip=tooltip_content
    ).add_to(map_object)

if __name__ == '__main__':
    app.run(debug=True)

