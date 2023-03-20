# Vinter-meteomatics

Vinter-meteomatics is a repository that interacts with the Meteomatics API and provides a REST API via FastApi that allows the user to query a location's weather parameters by specifying a latitude, a longitude and a time range. 15 basic parameters are covered, and these are further classified into 'wind', 'temperature' and 'misc'.

## Installation

Install the dependencies in the requirements.txt file. A working PostgreSQL database is also required to store and query the data.

## Usage and schema explained

The user specifies 4 parameters in the FastApi. Latitude and Longitude are both floats, and StartTime and EndTime are datetime strings.

Following this the program queries (if available), the data from the PostgreSQL database. If the data is not present, a call is made to the Meteomatics API to get the data and then store it in the PostgreSQL database.

The program also stores the locations queries in a pickle file, and updates the data periodically using Cron.

Data is available in both the wide and long (only for wind and temperature) format.

Error handling is incorporated using HTTPException from FastApi.

The models file includes the instructions for creating the tables, and the schema file is included to make data handling easier.

One good thing about the database schema is that it is easy and intuitive to follow. That being said, we can probably develop a more efficient schema to reduce API calls given that 'all' paramaters are a superset of 'wind', 'temperature' and 'misc'.

Further additions can be made to encrypt the API keys/provide a sample config file instead of exposing private credentials.

Also, a few data validation functions are present, but more can be added to ensure integrity of the data received from the Meteomatics API prior to storing it in the database.

Hope you enjoy playing around with the API!