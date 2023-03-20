dataTypes = ['all','wind','temperature', 'misc' ]
availableParams = {
	'wind': [
		'wind_speed_10m:ms',
		'wind_dir_10m:d',
		'wind_gusts_10m_1h:ms',
		'wind_gusts_10m_24h:ms'
	],
	'temperature': [
		't_2m:C',
		't_max_2m_24h:C',
		't_min_2m_24h:C'
	],
	'misc': [
		'msl_pressure:hPa',
		'precip_1h:mm',
		'precip_24h:mm',
		'weather_symbol_1h:idx',
		'weather_symbol_24h:idx',
		'uv:idx',
		'sunrise:sql',
		'sunset:sql'
	]
}
columnNames = {}
columnNames['all'] = {}
for key in availableParams.keys():
	columnNames[key] = {}
	for param in availableParams[key]:
		columnNames[key][param] = param.split(":")[0]
		columnNames['all'][param] = param.split(":")[0]
