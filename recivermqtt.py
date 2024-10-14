import paho.mqtt.client as mqtt
import mysql.connector
import time
import json  # Import the json library

# MySQL database connection setup
db_connection = mysql.connector.connect(
    host="localhost",    # e.g., "localhost"
    user="root",         # MySQL username
    password="",         # MySQL password
    database="database1" # Database name
)

cursor = db_connection.cursor()

# Define the callback for when the client receives a message
def on_message(client, userdata, message):
    # Decode the message and parse the JSON data
    received_data = message.payload.decode('utf-8')
    
    try:
        # Load the received data as JSON
        json_data = json.loads(received_data)
        print(f"Received JSON data: {json_data}")
        
        # Check if the data is a list of 4 digits
        if isinstance(json_data, list) and len(json_data) == 4:
            digit1, digit2, digit3, digit4 = json_data
            
            # Print each digit for debugging
            print(f"Digit 1: {digit1}, Digit 2: {digit2}, Digit 3: {digit3}, Digit 4: {digit4}")
            
            # Insert the data into the MySQL database
            sql_insert_query = """
                INSERT INTO mqtt_data (digit1, digit2, digit3, digit4)
                VALUES (%s, %s, %s, %s)
            """
            data_to_insert = (digit1, digit2, digit3, digit4)
            
            cursor.execute(sql_insert_query, data_to_insert)
            db_connection.commit()
            
            print("Data inserted into the database successfully!")
        else:
            print(f"Unexpected data format: {json_data}")
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from received data: {received_data}")

# Define the callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code: {rc}")
    client.subscribe("/test")  # Replace with the correct topic

# Create a new MQTT client instance
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_publish=on_publish

# Connect to the MQTT broker (Replace with your broker's IP/hostname and port)
broker_address = "broker.emqx.io"  # e.g., "mqtt.eclipseprojects.io"
broker_port = 1883

client.connect(broker_address, broker_port)

# Start the loop to listen for incoming messages indefinitely
client.loop_forever()

# Close the database connection when done (if stopping the loop manually)
db_connection.close()
