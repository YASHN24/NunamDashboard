import pandas as pd
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yash:postgres@localhost:5432/nunamdb'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# Hardcoded username and password (you can use a more secure method in production)
users = {
    "yash": "7388957687"
}


@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None


@app.route('/api/data/<cell_id>/<sheet_name>', methods=['GET'])
@auth.login_required
def get_data(cell_id, sheet_name):
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/nunamdb')
    table_name = f'"cell_{cell_id}_{sheet_name}"'

    # Check if 'all' parameter is present
    fetch_all = request.args.get('all', 'false').lower() == 'true'

    # Pagination parameters (only used if not fetching all)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Filtering
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')

    # Base query
    query = f"SELECT * FROM {table_name}"

    if filter_column and filter_value:
        query += f" WHERE {filter_column} = '{filter_value}'"

    data = pd.read_sql_query(query, con=engine)

    if fetch_all:
        return jsonify({
            'total': len(data),
            'data': data.to_dict(orient='records')
        })
    else:
        # Pagination logic
        total = len(data)
        start = (page - 1) * per_page
        end = start + per_page
        data_paginated = data.iloc[start:end]

        return jsonify({
            'total': total,
            'page': page,
            'per_page': per_page,
            'data': data_paginated.to_dict(orient='records')
        })


if __name__ == '__main__':
    app.run(port=5000, debug=True)
