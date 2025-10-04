import configparser
import json
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)
DATABASE = 'database.db'
CONFIG_FILE = 'config.ini'


def parse_config(file_path):
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
        if not config.sections():
            raise ValueError("Config file is empty or improperly formatted.")

        config_data = {}
        for section in config.sections():
            config_data[section] = dict(config.items(section))
        return config_data

    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading config: {str(e)}")
        return None


def save_to_database(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            json_data TEXT NOT NULL
        )
    ''')

    # Convert dict to JSON string
    json_data = json.dumps(data)

    # Insert into database
    cursor.execute("INSERT INTO config_data (json_data) VALUES (?)", (json_data,))
    conn.commit()
    conn.close()


def get_latest_config():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT json_data FROM config_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return json.loads(row[0])
    else:
        return {"message": "No config data found."}


@app.route('/config', methods=['GET'])
def fetch_config():
    config_data = get_latest_config()
    return jsonify(config_data)


if __name__ == '__main__':
    parsed_data = parse_config(CONFIG_FILE)
    if parsed_data:
        print("Configuration File Parser Results:")
        for section, values in parsed_data.items():
            print(f"{section}:")
            for key, val in values.items():
                print(f"- {key}: {val}")
        save_to_database(parsed_data)

    app.run(debug=True)
