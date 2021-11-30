import pandas as pd

# Path to the files created by merge.py
mergedTrip = 'Telemotix_email/ToBeMerged/trip/combined_trip.csv'
mergedLoc = 'Telemotix_email/ToBeMerged/loc/combined_loc.csv'

# Path to suspected "complete" telemotix data
telemotixTrip = 'telemotix/trip.csv'
telemotixLoc = 'telemotix/loc.csv'

dtype={

}
# loads files into dataframe
mt = pd.read_csv(mergedTrip, sep=',')
ml = pd.read_csv(mergedLoc, sep=',', na_filter=False)
tt = pd.read_csv(telemotixTrip, sep=',')
tl = pd.read_csv(telemotixLoc, sep=',')

# Shape of the dataframes
print('Merged trip Rows and columns: %s' % str(mt.shape))
print('Telemotix trip Rows and columns: %s' % str(tt.shape))

print('Merged loc Rows and columns: %s' % str(ml.shape))
print('Telemotix loc Rows and columns: %s' % str(tl.shape))

