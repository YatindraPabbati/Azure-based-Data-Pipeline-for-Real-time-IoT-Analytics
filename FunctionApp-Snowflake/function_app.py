import azure.functions as func
import logging
import os
import json
import snowflake.connector
from opencensus.ext.azure.log_exporter import AzureLogHandler

app = func.FunctionApp()

# Set up Application Insights logging
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")}'))
logger.setLevel(logging.INFO)

@app.service_bus_queue_trigger(arg_name="azservicebus", queue_name="kritsnamqueue5",
                               connection="KritsnamNamespace1_SERVICEBUS") 
def servicebus_queue_trigger_snowflake(azservicebus: func.ServiceBusMessage):
    # Log the received message
    message_body = azservicebus.get_body().decode('utf-8')
    logger.info('Received Service Bus Queue message: %s', message_body)
    
    # Parse the message from the queue
    data = parse_service_bus_message(message_body)
    
    # Insert the parsed data into Snowflake
    insert_into_snowflake(data)

def parse_service_bus_message(msg):
    """
    Parse the message body from the Service Bus Queue (assuming JSON format).
    """
    try:
        return json.loads(msg)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse message: {str(e)}")
        return None

def insert_into_snowflake(data):
    """
    Inserts parsed data directly into a Snowflake table.
    """
    if not data:
        logger.error("No data to insert into Snowflake")
        return
    
    # Extract json_ver and flatten teleParam data
    json_ver = data.get('json-ver')
    tele_params = data.get('teleParam', [])

    try:
        # Establish Snowflake connection
        conn = snowflake.connector.connect(
            user="yatindra",
            password="Yatin@snowflake24",
            account="la29961.central-india.azure",
            warehouse="compute_wh",
            database="flowmeter_telemetry",
            schema="public",
        )

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # SQL Insert query to insert the data into your Snowflake table
        insert_query = """
        INSERT INTO telemetry_raw (
            token, status, json_ver, ts, time, created_at, 
            flowrate, discharge, workhour, cummrevdisch, data, 
            cycleslips, nodata, uss
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for param in tele_params:
            # Prepare to log the data being inserted
            logger.info("Inserting data: token=%s, status=%s, json_ver=%s, ts=%s",
                        data['token'], data['status'], json_ver, param['ts'])
            
            # Ensure that 'time' and 'created_at' are correctly extracted from param
            # If not included in the original message, you can assign a default value or log a warning
            time = param.get('time', None)  # Adjust based on your needs
            created_at = param.get('created_at', None)  # Adjust based on your needs

            # Execute the insert for each telemetry parameter
            cursor.execute(insert_query, (
                data['token'], data['status'], json_ver, 
                param['ts'], time, created_at, 
                param['flowRate'], param['discharge'], param['workHour'], 
                param['cummRevDisch'], param['Data'], 
                param['CycleSlips'], param['NoData'], 
                param['USS']
            ))

        # Commit the transaction to Snowflake
        conn.commit()
        logger.info("Data inserted successfully into Snowflake.")

    except Exception as e:
        logger.error(f"Error while inserting data into Snowflake: {str(e)}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
