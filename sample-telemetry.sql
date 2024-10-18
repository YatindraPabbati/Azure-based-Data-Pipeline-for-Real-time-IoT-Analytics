CREATE DATABASE flowmeter_telemetry;
USE DATABASE flowmeter_telemetry;
CREATE TABLE telemetry_raw (
   token VARCHAR(255),
   status VARCHAR(50),
   json_ver VARCHAR(50),
   ts BIGINT,
   time TIMESTAMP,
   created_at TIMESTAMP,
   flowrate FLOAT,
   discharge INTEGER,
   workhour INTEGER,
   cummrevdisch INTEGER,
   data INTEGER,
   cycleslips INTEGER,
   nodata INTEGER,
   uss BIGINT
);
SELECT * FROM telemetry_raw;
