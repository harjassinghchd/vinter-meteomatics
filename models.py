from sqlalchemy import Column, Float, DateTime, String, VARCHAR

from database import Base

class AllParameterswide(Base):
	__tablename__ = "allparameterswide"
	lat = Column(Float, primary_key=True)
	lon = Column(Float, primary_key=True)
	validdate = Column(DateTime, primary_key=True)
	wind_speed_10m = Column(Float)
	wind_dir_10m = Column(Float)
	wind_gusts_10m_1h = Column(Float)
	wind_gusts_10m_24h = Column(Float)
	t_2m = Column(Float)
	t_max_2m_24h = Column(Float)
	t_min_2m_24h = Column(Float)
	msl_pressure = Column(Float)
	precip_1h = Column(Float)
	precip_24h = Column(Float)
	weather_symbol_1h = Column(Float)
	weather_symbol_24h = Column(Float)
	uv = Column(Float)
	sunrise = Column(DateTime)
	sunset = Column(DateTime)


class WindParameterswide(Base):
	__tablename__ = "windparameterswide"
	lat = Column(Float, primary_key=True)
	lon = Column(Float, primary_key=True)
	validdate = Column(DateTime, primary_key=True)
	wind_speed_10m = Column(Float)
	wind_dir_10m = Column(Float)
	wind_gusts_10m_1h = Column(Float)
	wind_gusts_10m_24h = Column(Float)

class TemperatureParameterswide(Base):
	__tablename__ = "temperatureparameterswide"
	lat = Column(Float, primary_key=True)
	lon = Column(Float, primary_key=True)
	validdate = Column(DateTime, primary_key=True)
	t_2m = Column(Float)
	t_max_2m_24h = Column(Float)
	t_min_2m_24h = Column(Float)

class MiscParameterswide(Base):
	__tablename__ = "miscparameterswide"
	lat = Column(Float, primary_key=True)
	lon = Column(Float, primary_key=True)
	validdate = Column(DateTime, primary_key=True)
	msl_pressure = Column(Float)
	precip_1h = Column(Float)
	precip_24h = Column(Float)
	weather_symbol_1h = Column(Float)
	weather_symbol_24h = Column(Float)
	uv = Column(Float)
	sunrise = Column(DateTime)
	sunset = Column(DateTime)



class WindParameterslong(Base):
	__tablename__ = "windparameterslong"
	lat = Column(Float, primary_key=True)
	lon = Column(Float, primary_key=True)
	validdate = Column(DateTime, primary_key=True)
	variable = Column(VARCHAR(255))
	value = Column(Float)

class TemperatureParameterslong(Base):
	__tablename__ = "temperatureparameterslong"
	lat = Column(Float, primary_key=True)
	lon = Column(Float, primary_key=True)
	validdate = Column(DateTime, primary_key=True)
	variable = Column(VARCHAR(255))
	value = Column(Float)

