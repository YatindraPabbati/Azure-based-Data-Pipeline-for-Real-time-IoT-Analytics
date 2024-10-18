import os
import json
import logging
from datetime import datetime
import azure.functions as func
import psycopg2

# Import Application Insights
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Set up Application Insights tracing
APPINSIGHTS_CONNECTION_STRING = os.getenv('APPINSIGHTS_CONNECTION_STRING')
exporter = AzureMonitorTraceExporter.from_connection_string(APPINSIGHTS_CONNECTION_STRING)
provider = TracerProvider()
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Function App definition
app = func.FunctionApp()

@app.service_bus_queue_trigger(arg_name="azservicebus", queue_name="postgres_queue",
                               connection="KritsnamNamespace1_SERVICEBUS")
def postgresql_function(azservicebus: func.ServiceBusMessage):
    message_body = azservicebus.get_body().decode('utf-8')
    logging.info(f'Received message from Service Bus Queue: {message_body}')
    
    # Start tracing for this message processing
    with tracer.start_as_current_span("process_message"):
        try:
            logging.info('Parsing the message JSON.')
            data = json.loads(message_body)
            logging.info(f"Parsed JSON data successfully: {data}")
            
            # Insert data into PostgreSQL
            insert_into_postgres(data)
        
        except Exception as e:
            logging.error(f"Error processing the message: {str(e)}")
            print(f"Error processing the message: {str(e)}")
            raise e  # This ensures the message stays in the queue if an error occurs

def insert_into_postgres(data):
    conn = None
    cursor = None
    try:
        logging.info("Extracting fields from the JSON payload.")
        token = data.get("token", "")
        status = data.get("status", "")
        json_ver = data.get("json-ver", "")
        tele_params = data.get("teleParam", [])

        logging.info(f"Token: {token}, Status: {status}, JSON Version: {json_ver}")
        print(f"Token: {token}, Status: {status}, JSON Version: {json_ver}")
        
        # Establish connection to PostgreSQL
        logging.info("Connecting to PostgreSQL.")
        conn = psycopg2.connect(
            host="kritsnampostgressqlserver1.postgres.database.azure.com",
            database="kritsnamdb1",
            user="Yatindra",
            password="Kritsnam@24",
            port="5432"
        )
        logging.info("PostgreSQL connection established.")
        print("PostgreSQL connection established.")

        cursor = conn.cursor()

        # Insert telemetry data into PostgreSQL
        for param in tele_params:
            ts = param['ts']
            timestamp_value = datetime.utcfromtimestamp(ts / 1000)  # Convert to timestamp
            current_timestamp = datetime.utcnow()  # Current timestamp for 'created_at'
            flow_rate = param['flowRate']
            discharge = param['discharge']
            work_hour = param['workHour']
            cumm_rev_disch = param['cummRevDisch']
            data_value = param['Data']
            cycle_slips = param['CycleSlips']
            no_data = param['NoData']
            uss = param['USS']

            logging.info(f"Inserting data with timestamp: {timestamp_value} and flowrate: {flow_rate}")
            print(f"Inserting data with timestamp: {timestamp_value} and flowrate: {flow_rate}")

            insert_query = """
                INSERT INTO telemetry_raw 
                (token, status, json_ver, ts, time, created_at, flowrate, discharge, workhour, cummrevdisch, data, cycleslips, nodata, uss)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                token, status, json_ver, ts, timestamp_value, current_timestamp, 
                flow_rate, discharge, work_hour, cumm_rev_disch, data_value, 
                cycle_slips, no_data, uss
            ))

        # Commit transaction
        conn.commit()
        logging.info("Data successfully inserted into PostgreSQL.")
        print("Data successfully inserted into PostgreSQL.")

    except Exception as e:
        logging.error(f"Error inserting into PostgreSQL: {str(e)}")
        print(f"Error inserting into PostgreSQL: {str(e)}")
        raise e  # Raise the error to keep the message in the queue and retry

    finally:
        if cursor:
            cursor.close()
            logging.info("PostgreSQL cursor closed.")
            print("PostgreSQL cursor closed.")
        if conn:
            conn.close()
            logging.info("PostgreSQL connection closed.")
            print("PostgreSQL connection closed.")



@app.service_bus_queue_trigger(arg_name="azservicebus", queue_name="kritsnamqueue5",
                               connection="KritsnamNamespace1_SERVICEBUS") 
def servicebus_trigger_snowflake(azservicebus: func.ServiceBusMessage):
    logging.info('Python ServiceBus Queue trigger processed a message: %s',
                azservicebus.get_body().decode('utf-8'))
