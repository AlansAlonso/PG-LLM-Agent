import streamlit as st 
from agent import Agent

import folium
from folium.plugins import MarkerCluster, MeasureControl
from streamlit_folium import folium_static
import logging
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

LOGGER = logging.getLogger(__name__)

st.set_page_config(layout="wide")

### Initialization
def initialize_session_state():
    if "marker" not in st.session_state:
        st.session_state.marker = []

def initialize_map(center, zoom=10):
    if "map" not in st.session_state or st.session_state.map is None:
        st.session_state.center = center
        st.session_state.zoom = zoom
        folium_map = folium.Map(
            location=center,
            zoom_start=zoom)
        st.session_state.map = folium_map
    return st.session_state.map

initialize_session_state()
### Dashboard
st.title("Welcome to the Tourism Agent App!")
st.write("This app will help you plan your travels with detailed tips and suggestions.")
points_coordinates = []

agent = Agent(API_KEY)

col1, col2 = st.columns(2)

with col1:
    request = st.text_area("Where would you like to travel? Please describe your request in Portuguese.")
    button = st.button("Get Travel Tips")
    
    box = st.container(height=300)
    with box:
        container = st.empty()
        container.header("Itinerary Suggestions")

if button and request:
    itinerary = agent.get_tips(request)
    try:
        container.write(itinerary["itinerary"])
    except KeyError:
        container.write("""
        Sorry, I couldn't generate an itinerary for your request.
        Please try again with a different request.
        """)
    try:
        coordinates = itinerary["coordinates"]
        points_coordinates = []
        days = json.loads(coordinates)
        for day in days["days"]:
            locations = day.get("locations", [])
            for loc in locations:
                points_coordinates.append(
                    [loc["lat"], loc["lon"]]
                )
        st.session_state['marker'] = [
            folium.Marker(location=point) for point in points_coordinates
        ]
        
    except KeyError:
        LOGGER.warning("No coordinates found in the itinerary response.")
        pass

with col2:
    folium_map = initialize_map(center=[ -23.5612, -46.6559], zoom=12)
    fg = folium.FeatureGroup(name="Markers")
    for marker in st.session_state['marker']:
        fg.add_child(marker)
    fg.add_to(folium_map)
    folium_static(folium_map)