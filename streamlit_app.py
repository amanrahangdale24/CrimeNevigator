import altair as alt
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Crime Navigator App",  # App title
    page_icon="🔍",  # App icon
    layout="wide"  # Wide layout
)

# Load CSS file
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# File paths to datasets
file_paths = [
    'data/01_District_wise_crimes_committed_IPC_2013.csv',
    'data/02_01_District_wise_crimes_committed_against_SC_2001_2012.csv',
    'data/01_District_wise_crimes_committed_IPC_2014.csv',
    # Add more files as needed
]

# Read and combine the datasets
dataframes = [pd.read_csv(file_path) for file_path in file_paths]
data = pd.concat(dataframes, ignore_index=True)

# Crime categories to visualize
crime_columns = ['Murder', 'Rape', 'KIDNAPPING & ABDUCTION', 'Arson', 'Grievous Hurt']

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Select a view:",
    ("Home", "Crime Data Visualization")
)

# Home Page
if option == "Home":
    st.write("Welcome to the Crime Navigator App!")
    st.write("Use the sidebar to navigate through different views of the crime data.")

# Crime Data Visualization Page
elif option == "Crime Data Visualization":
    # Dropdown for state selection
    states = data['States/UTs'].unique()
    selected_state = st.selectbox('Select a state:', states)

    # Filter the data for the selected state
    state_data = data[data['States/UTs'] == selected_state]

    # Dropdown for city selection (within the selected state)
    cities_in_state = state_data['District'].unique()
    selected_city = st.selectbox('Select a city in the state:', cities_in_state)

    # Filter data based on the selected city
    city_data = state_data[state_data['District'] == selected_city]

    # Display filtered data
    st.subheader(f'Crime Data for {selected_city} in {selected_state}')
    st.write(city_data)

    # Data Visualization: Show crime counts per category
    st.subheader(f'Crime Statistics in {selected_city}')
    # Dynamically handle columns available in the dataset
    available_columns = [col for col in crime_columns if col in city_data.columns]

    # Sum of crimes for each available category
    crime_counts = city_data[available_columns].sum()
    # Sort the crime counts in descending order
    sorted_crime_counts = crime_counts.sort_values(ascending=False)

    # Display the sorted crime counts
    st.bar_chart(sorted_crime_counts)

    # Comparison Visualization: Crime data for all cities in the selected state
    st.subheader(f'Crime Comparison in {selected_state}')
    state_crime_totals = state_data.groupby('District')[available_columns].sum().reset_index()

    # Create a bar chart comparison of crimes across cities in the selected state
    state_crime_chart = alt.Chart(state_crime_totals).mark_bar().encode(
        x='District:N',
        y='sum(Murder):Q',
        color='District:N',
        tooltip=available_columns
    ).properties(
        title=f'Comparison of Crime across Cities in {selected_state}'
    )
    st.altair_chart(state_crime_chart, use_container_width=True)

