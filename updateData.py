
import pickle
import traceback
import schema
import meteomatics.api as mt
from dateutil import parser
from datetime import timedelta
from config import config
import pandas as pd
from meteomatics.exceptions import Forbidden
from database import engine
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
import time


try:
	with open('locationsRequested.p','rb') as pfile:
		locationsRequested = pickle.load(pfile)
except:
	locationsRequested = []

if locationsRequested:
	for location in locationsRequested:
		lat = location[0]
		lon = location[1]
		endtime = location[2]
		endtimeDateTime = parser.parse(endtime)
		for type_of_data in schema.dataTypes:
			try:
				if type_of_data in ['wind', 'temperature', 'misc']:
					interimData = mt.query_time_series([(lat, lon)], endtimeDateTime, endtimeDateTime + timedelta(hours=1),
					                                   timedelta(hours=1),
					                                   schema.availableParams[type_of_data], config['username'],
					                                   config['password'])


				elif type_of_data == 'all':
					interimData_1 = mt.query_time_series([(lat, lon)],endtimeDateTime, endtimeDateTime + timedelta(hours=1),
					                                     timedelta(hours=1),
					                                     schema.availableParams['wind'] + schema.availableParams[
						                                     'temperature'], config['username'], config['password'])
					interimData_2 = mt.query_time_series([(lat, lon)], endtimeDateTime, endtimeDateTime + timedelta(hours=1),
					                                     timedelta(hours=1),
					                                     schema.availableParams['misc'], config['username'],
					                                     config['password'])
					interimData = pd.concat([interimData_1, interimData_2], axis=1)

			except Forbidden as e:
				pass

			interimData.rename(columns=schema.columnNames[type_of_data], inplace=True)
			tableName = type_of_data + "parameterswide"
			try:
				interimData.to_sql(tableName, engine, if_exists='append')
			except IntegrityError as e:
				if isinstance(e.orig, UniqueViolation):
					pass
				else:
					print(traceback.format_exc())
