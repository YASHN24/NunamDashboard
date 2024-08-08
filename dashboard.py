import pandas as pd
import streamlit as st
import plotly.express as px
import requests
from requests.auth import HTTPBasicAuth


# Function to load data from REST API
def load_all_data(cell_identifier, sheet_identifier):
    try:
        response = requests.get(f'http://localhost:5000/api/data/{cell_identifier}/{sheet_identifier}',
                                params={'all': 'true'},
                                auth=HTTPBasicAuth('yash', '7388957687'))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error occurred: {req_err}")
    except ValueError:
        st.error("Received an invalid JSON response from the API.")
    return None


# Sidebar for navigation
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio("Go to", ["Dashboard", "Cell Data"])

if nav_option == "Dashboard":
    # Main dashboard page
    st.title("Dashboard")
    st.subheader("State of Health")

    # Calculate SoH for each cell
    soh_5308 = (2992.02 / 3000) * 100
    soh_5329 = (2822.56 / 3000) * 100

    # Pie charts
    fig_5308 = px.pie(values=[soh_5308, 100 - soh_5308], names=['Healthy', 'Degraded'], title="Cell ID 5308 SoH")
    fig_5329 = px.pie(values=[soh_5329, 100 - soh_5329], names=['Healthy', 'Degraded'], title="Cell ID 5329 SoH")

    st.plotly_chart(fig_5308)
    st.plotly_chart(fig_5329)

elif nav_option == "Cell Data":
    # Cell data page
    st.sidebar.title("Cell ID Selector")
    cell_id = st.sidebar.selectbox("Select Cell ID", ["5308", "5329"])
    sheet_name = st.sidebar.selectbox("Select Data Type",
                                      ["Voltage vs Time", "Current vs Time", "Temperature vs Time", "Capacity vs Time"])

    st.title(f"Cell ID {cell_id} Data")

    # Define the sheet suffixes based on the cell ID
    suffix_map = {
        "5308": "67_3_5",
        "5329": "67_3_1"
    }

    # Mapping of sheet names and columns for different data types
    sheet_map = {
        "Voltage vs Time": ("DetailVol", "Realtime", "Auxiliary channel TU1 U(V)"),
        "Current vs Time": ("Detail", "Relative Time(h:min:s.ms)", "Cur(mA)"),
        "Temperature vs Time": ("DetailTemp", "Realtime", "Auxiliary channel TU1 T(°C)"),
        "Capacity vs Time": ("Detail", "Relative Time(h:min:s.ms)", "CapaCity(mAh)")
    }

    sheet_identifier, x_column, y_column = sheet_map[sheet_name]
    sheet_identifier = f"{sheet_identifier}_{suffix_map[cell_id]}"

    data = load_all_data(cell_id, sheet_identifier)
    if data and 'data' in data:
        df = pd.DataFrame(data['data'])
        if df.empty:
            st.warning("No data available for the selected options.")
        elif x_column not in df.columns or y_column not in df.columns:
            st.error(f"Expected columns '{x_column}' and '{y_column}' not found in the data.")
        else:
            fig = px.line(df, x=x_column, y=y_column, title=f'{sheet_name} for Cell ID {cell_id}')
            st.plotly_chart(fig)
    else:
        st.error("Failed to load data or data is in unexpected format.")
