import pandas as pd


loc = 'Telemotix_email/ToBeMerged/loc/combined_loc.csv'
df = pd.read_csv(loc, delimiter=',')
# id is needed for easier merge later
df.index = [x for x in range(1, len(df.values) + 1)]
df.index.name = 'id'

df = df.sort_values('trip_id')
#df = df.sort_values(by='timestamp_utc', ascending=True)
df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'], utc=True, errors='coerce')


ddf = df[['timestamp_utc', 'trip_id', 'serial_number', 'trigger_type']]
ddfs = ddf.trigger_type.str.split(',', expand=True)

# start and end trip
ddf.loc[ddf.trigger_type == 'S_TRIP', 'S_TRIP'] = int(1)  # S_TRIP and E_TRIP are always singular in the row
ddf.loc[ddf.trigger_type == 'E_TRIP', 'E_TRIP'] = int(1)

# remove start and stop
ddfs = ddfs[ddfs != 'S_TRIP']
ddfs = ddfs[ddfs != 'E_TRIP']
# drop empty rows
#ddfs = ddfs.dropna(how='all')

for n in [0, 1, 2]:
    ddfsu = ddfs[n].str.split('_', expand=True)  # split rows on _
    ddf = pd.concat([ddf, ddfsu.loc[ddfsu[1] == 'BRK', 2]], axis=1).rename(columns={2: 'BRK_{}'.format(n)})
    ddf = pd.concat([ddf, ddfsu.loc[ddfsu[1] == 'ACC', 2]], axis=1).rename(columns={2: 'ACC_{}'.format(n)})
    ddf = pd.concat([ddf, ddfsu.loc[ddfsu[1] == 'TRN', 2]], axis=1).rename(columns={2: 'TRN_{}'.format(n)})
    ddf = pd.concat([ddf, ddfsu.loc[ddfsu[1] == 'G', 2]], axis=1).rename(columns={2: 'G_{}'.format(n)})

df_out = pd.merge(df, ddf, how='left', on=['id', 'serial_number', 'timestamp_utc', 'trip_id'])
df_out.rename(columns={'trigger_type_x': 'trigger_type'}, inplace=True)

dropColumns = [  # 'timestamp_utc',
    # 'trip_id',
    # 'serial_number',
    'gateway_iccid',
    # 'odometer_km',
    'fuel_level',
    # 'speed_kmh',
    # 'speed_limit_kmh',
    'road_category',
    # 'geo_lat',
    # 'geo_long',
    'geo_quality',
    'post_number',
    'trigger_type',
    'rpk',
    'car_voltage',
    'fuel_usage_maf',
    # 'temperature_celsius',
    'wind_direction_degrees',
    'wind_speed_meters_per_sec',
    'wind_gust_meters_per_sec',
    # 'humidity_percent',
    'pressure_hpa',
    'cloudiness_percent',
    # 'fog_percent',
    # 'low_clouds_percent',
    # 'medium_clouds_percent',
    # 'high_clouds_percent',
    # 'dew_point_temperature',
    'time_forecast',
    # 'precipitation_mm',
    # 'precipitation_id',
    's_trip',
    'e_trip',
    'brk_0',
    'acc_0',
    'trn_0',
    'g_0',
    'brk_1',
    'acc_1',
    'trn_1',
    'g_1',
    'brk_2',
    'acc_2',
    'trn_2',
    'g_2',
    'acc_3',
    'brk_3',
    'g_3',
    'trn_3',
    'geom',
    'pkey',
    'S_TRIP',  # uppercased fields are updated from trigger_type
    'E_TRIP',
    # 'BRK_0',
    # 'ACC_0',
    # 'TRN_0',
    # 'G_0',
    # 'BRK_1',
    # 'ACC_1',
    # 'TRN_1',
    # 'G_1',
    # 'BRK_2',
    # 'ACC_2',
    # 'TRN_2',
    # 'G_2',
]

for columns in df_out.columns:
    if columns in dropColumns:
        df_out = df_out.drop(columns, axis=1)

df_out.drop('trigger_type_y', axis=1, inplace=True)
#df_out = df_out.dropna(axis=0, how='all')
df_out = df_out.fillna(value=0)
# df_out = preprocessing.normalize(df_out)

trip_id = pd.unique(df_out['trip_id'])
for x in trip_id:
    print(x)

'''

#drop trips on the weekends
weekDay = 0
weekEnd = 0
for index, row in df_out.iterrows():
    if row['timestamp_utc'].dayofweek > 4:
        df_out.drop(index, inplace=True)
        weekEnd = weekEnd + 1
        print('Weekend: ', weekEnd)
    else:
        print('Weekday: ', weekDay)
        weekDay = weekDay + 1
'''

# Removes weekends from the data, for testing
# df_out['day_of_week'] = df_out['timestamp_utc'].dt.day_name()
# df_out = df_out[df_out.day_of_week != 'Saturday']
# df_out = df_out[df_out.day_of_week != 'Sunday']


df_out.to_csv("processedData.csv", index=False, encoding='utf-8', )
