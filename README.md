# Azure-Based Data Pipeline for Real-Time IoT Analytics

This project demonstrates an **end-to-end data pipeline** using **Microsoft Azure services** and **Snowflake** to process, store, and analyze IoT data in **real-time**. The solution securely collects telemetry data from **IoT devices**, processes it through **Azure IoT Hub** and **Azure Functions**, and stores the data in **Azure SQL Database** and **Blob Storage**. **Snowflake** integrates via **Snowpipe** for advanced analytics.

---

## Table of Contents  
1. [Architecture Overview](#architecture-overview)  
2. [Technologies Used](#technologies-used)  
3. [System Workflow](#system-workflow)  
4. [Components Description](#components-description)  
5. [Setup Instructions](#setup-instructions)  
6. [Conclusion](#conclusion)  

---

## Architecture Overview  
This architecture enables seamless data ingestion, processing, and storage from **IoT devices** to **Azure IoT Hub**. IoT data is routed through **Azure Service Bus Queues** to **Azure Functions** for processing. Processed data is stored in **Azure SQL Database** and **Blob Storage**, while **Snowflake** integrates via **Snowpipe** for advanced analytics.

![Screenshot 2024-10-18 110446](https://github.com/user-attachments/assets/cc8549c1-badb-4238-a7e4-f350a9c06599)

---

## Technologies Used  
- **IoT Devices**: Modbus, MQTT over TLS (Authenticated)  
- **Azure Services**:  
  - Azure IoT Hub  
  - Azure Service Bus Queue  
  - Azure Functions  
  - Azure Monitor  
  - Azure Blob Storage  
  - Azure SQL Database  
- **Snowflake**: With **Snowpipe** for automated data ingestion  

---

## System Workflow  

### 1. **IoT Data Ingestion via Azure IoT Hub**  
- **IoT Devices** send telemetry data using **Modbus protocol**.  
- The data is transmitted to **Azure IoT Hub** using **MQTT over TLS** for secure communication.

### 2. **Data Routing via Service Bus Queue**  
- IoT Hub forwards the telemetry data to a **Service Bus Queue** using routing rules.

### 3. **Data Processing with Azure Functions**  
- **Azure Functions** are triggered by new messages arriving in the **Service Bus Queue**.  
- The function processes the data and inserts it into **Azure SQL Database** and **Blob Storage**.

### 4. **Monitoring with Azure Monitor**  
- **Azure Monitor** tracks the performance and health of services across the pipeline and provides alerts for proactive management.

### 5. **Data Ingestion into Snowflake via Snowpipe**  
- Processed data stored in **Azure Blob Storage** is automatically ingested into **Snowflake** using **Snowpipe**.  
- Snowflake provides advanced querying capabilities for analytics and reporting.

---

## Components Description  
### 1. **Azure IoT Hub**  
- Manages secure, bidirectional communication between IoT devices and the cloud.  
- Receives device telemetry and forwards it to **Service Bus Queues** based on routing rules.

### 2. **Service Bus Queue**  
- Decouples communication between IoT Hub and **Azure Functions** for asynchronous processing.  
- Ensures message durability and reliability.

### 3. **Azure Functions**  
- Processes the incoming data from the **Service Bus Queue**.  
- Inserts relevant data into **Azure SQL Database** for structured storage and **Blob Storage** for unstructured data.

### 4. **Azure Monitor**  
- Monitors the health and performance of the pipeline components.  
- Sends alerts for proactive issue detection and resolution.

### 5. **Azure Blob Storage & Snowpipe**  
- **Blob Storage** acts as an intermediate storage for processed data.  
- **Snowpipe** automatically ingests files from Blob Storage into **Snowflake** for advanced analytics.

### 6. **Snowflake**  
- Provides a scalable cloud database for storing and querying telemetry data.  
- Supports advanced analytics to derive insights from the ingested data.

---

## Setup Instructions  

### 1. **Prerequisites:**  
- Azure subscription with IoT Hub, Service Bus, Functions, SQL, and Monitor services enabled.  
- Snowflake account with Snowpipe configured.

### 2. **IoT Device Configuration:**  
- Configure IoT devices to send telemetry data to **Azure IoT Hub** using **MQTT over TLS**.

### 3. **Azure IoT Hub Setup:**  
- Register the IoT devices in **IoT Hub**.  
- Create routing rules to forward incoming telemetry to the **Service Bus Queue**.

### 4. **Service Bus Queue and Azure Function Setup:**  
- Create a **Service Bus Queue** to receive telemetry data from IoT Hub.  
- Develop an **Azure Function** to process the data and insert it into **Azure SQL Database** and **Blob Storage**.

### 5. **Snowflake and Snowpipe Configuration:**  
- Create the required tables in **Snowflake** to store telemetry data.  
- Configure **Snowpipe** to monitor Azure Blob Storage and ingest data as soon as it arrives.

---

## Conclusion  
This project showcases a real-time IoT data pipeline using **Azure IoT Hub**, **Service Bus**, **Azure Functions**, **Azure SQL Database**, **Blob Storage**, and **Snowflake**. It offers a secure and scalable approach to ingest, process, and analyze telemetry data. The integration of **Snowpipe** ensures automated ingestion for advanced analytics, providing actionable insights with minimal latency.

---

For more details, refer to the [GitHub repository](https://github.com/YatindraPabbati/Azure-based-Data-Pipeline-for-Real-time-IoT-Analytics).
