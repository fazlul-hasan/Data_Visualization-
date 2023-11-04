import folium
import pandas as pd

import matplotlib.pyplot as plt
from ipywidgets import interact, widgets
from IPython.display import display
from flask import Flask, render_template, request

app = Flask(__name__,template_folder='templates')
@app.route("/", methods=['GET', 'POST'])

def index():
    # Read data
    data = pd.read_csv('spain_club_data.csv')
    latitude = 40.4637
    longitude = -3.7492

    # Create map
    m = folium.Map(location=[latitude, longitude], zoom_start=6, tiles='OpenStreetMap')
    for index, row in data.iterrows():
        location = [row['latitude'], row['longitude']]
        tooltip_content = f"Club: {row['club']}<br>Stadium Capacity: {row['stadium_capacity']}"
        icon = folium.features.CustomIcon(
            icon_image='laliga.png',
            icon_size=(45, 70)
        )
        folium.Marker(
            location=location,
            icon=icon,
            tooltip=tooltip_content
        ).add_to(m)

    # Render the map as an HTML string
    map_html = m._repr_html_()

    # Pass the HTML string to the frontend
    return render_template('map.html', map_html=map_html)


if __name__ == '__main__':
    app.run(debug=True)
