from sqlalchemy.orm import Session
import meteomatics.api as mt
import models, schema
from datetime import timedelta
import pandas as pd
from config import config
from database import engine
from dateutil import parser
from meteomatics.exceptions import Forbidden
from fastapi import HTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
import pickle

def get_parameters(db: Session, lat: float, lon: float, starttime: str, endtime: str, type_of_data: str = 'all', type_of_table: str = 'wide'):
	if type_of_data in ['all','misc'] and type_of_table == 'long':
		raise HTTPException(status_code=406,detail="Only wide data supported for data-type {}".format(type_of_data) )


	attributeName = type_of_data.title() + "Parameters" + type_of_table
	tableName = type_of_data + "parameters" + type_of_table
	starttimeDateTime = parser.parse(starttime)
	endtimeDateTime = parser.parse(endtime)
	try:
		with open('locationsRequested.p','rb') as pfile:
			locationsRequested = pickle.load(pfile)
		locationsRequested.append((lat, lon, endtime))
	except:
		locationsRequested = [(lat, lon, endtime)]
	with open('locationsRequested.p', 'wb') as pfile:
		pickle.dump(locationsRequested, pfile)
	data_to_return = db.query(getattr(models, attributeName)).filter(getattr(models, attributeName).lat == lat, getattr(models, attributeName).lon == lon,  starttimeDateTime < getattr(models, attributeName).validdate,  getattr(models, attributeName).validdate < endtimeDateTime).first()
	if data_to_return is None:
		try:
			if type_of_data in ['wind', 'temperature', 'misc']:
				interimData = mt.query_time_series([(lat, lon)], starttimeDateTime, endtimeDateTime, timedelta(hours=1),
				                               schema.availableParams[type_of_data], config['username'], config['password'])


			elif type_of_data == 'all':
				interimData_1 = mt.query_time_series([(lat, lon)], starttimeDateTime, endtimeDateTime, timedelta(hours=1),
				                                   schema.availableParams['wind'] + schema.availableParams['temperature'], config['username'], config['password'])
				interimData_2 = mt.query_time_series([(lat, lon)], starttimeDateTime, endtimeDateTime, timedelta(hours=1),
				                                   schema.availableParams['misc'], config['username'], config['password'])
				interimData = pd.concat([interimData_1, interimData_2], axis=1)

		except Forbidden as e:
			raise HTTPException(status_code=405, detail=str(e))

		if type_of_table == 'wide':
			interimData.rename(columns=schema.columnNames[type_of_data], inplace=True)
			try:
				interimData.to_sql(tableName, engine, if_exists='append')
			except IntegrityError as e:
				if isinstance(e.orig, UniqueViolation):
					pass
				else:
					raise HTTPException(status_code=408,detail=str(e))
		elif type_of_table == 'long':
			interimData.reset_index(inplace=True)
			colTitles = interimData.columns.values.tolist()
			indexTitles = ['lat', 'lon', 'validdate']
			interimData = pd.melt(interimData, id_vars=indexTitles,
			                   value_vars=[col for col in colTitles if col not in indexTitles])
			interimData.set_index(indexTitles)
			return list(interimData.to_dict('records'))

		else:
			raise HTTPException(status_code=407,
			                    detail="Only wide and long data table formats supported")

	return db.query(getattr(models, attributeName)).filter(
		getattr(models, attributeName).lat == lat, getattr(models, attributeName).lon == lon, starttimeDateTime < getattr(models, attributeName).validdate,  getattr(models, attributeName).validdate < endtimeDateTime).all()


