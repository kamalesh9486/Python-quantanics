import paho.mqtt.client as mqtt 
import time
import random
import json
import mysql.connector

# MySQL database connection setup
db_connection = mysql.connector.connect(
    host="localhost",    # e.g., "localhost"
    user="root",         # MySQL username
    password="",         # MySQL password
    database="database1" # Database name
)
cursor = db_connection.cursor()

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")



# MQTT broker details
BROKER = "broker.emqx.io"
TOPIC = "/test"

# MQTT client setup
client = mqtt.Client()

client.connect(BROKER)
client.loop_start()
client.on_publish=on_publish

# Function to generate random combinations of 0 and 1 (e.g., [0,0,0,0] or [0,1,0,1])
def generate_random_data():
    # Create a list of random 0s and 1s
    data = [
        random.randint(0, 1),
        random.randint(0, 1),
        random.randint(0, 1),
        random.randint(0, 1)
    ]
    return data  # Return the list (not JSON string)
counter=0
while counter <100:
    # Generate random 4-digit binary data
    data = generate_random_data()
    
    # Convert the data to a JSON string for debugging purposes
    json_data = json.dumps(data)
    print(f"Generated Data: {json_data}")
    random_data=json.dumps(data)
    client.publish(TOPIC, random_data,qos=1)
            
    
    # Insert the data into the MySQL database
    sql_insert_query = """
                INSERT INTO mqtt_data (digit1, digit2, digit3, digit4)
                VALUES (%s, %s, %s, %s)
            """
    data_to_insert = (data[0], data[1], data[2], data[3])
            
    cursor.execute(sql_insert_query, data_to_insert)
    print("Data inserted into the database successfully!")

    db_connection.commit()

    
    # Wait for 2 seconds before generating the next set of data
    time.sleep(2)
    counter+=1



