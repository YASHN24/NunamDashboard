# NunamDashboard
A simple dashboard



This project is a dashboard for visualizing Li-ion cell data using a REST API. The dashboard is built with Streamlit and Plotly, and the backend API is developed using Flask with a PostgreSQL database.

## Project Structure

- `app.py`: The Flask application serving the REST API.
- `dashboard.py`: The Streamlit application for the dashboard.
- `data_loader.py`: Script to load Excel data into the PostgreSQL database.
- `test_app.py`: Unit tests for the API.

## Prerequisites

- Python 3.8 or later
- PostgreSQL installed and running
- Required Python packages (listed in `requirements.txt`)
  (some default libraries are also in requirements.txt as Pycharm is being used)

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YASHN24/NunamDashboard.git
   cd NunamDashboard


2. **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt

4. Set up the PostgreSQL database:
  -Create a new PostgreSQL database named nunamdb.
  -Update the database credentials in app.py and data_loader.py if necessary.

5. Load the data into the database:
```bash
python data_loader.py

6. Run the Flask API:
```bash
python app.py

7.Run the Streamlit dashboard:
```bash
streamlit run dashboard.py

8. To run the unit tests:
```bash
python -m unittest test_app.py
