import os
import glob
import pandas as pd

# specifies path to folder where the files that will be merged are located (change to trip/loc to merge trip/loc files)
os.chdir("Telemotix_email/ToBeMerged/loc")

# Extension will be used to match
extension = 'csv'

# Matches files in path that has extension csv
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# Combines the files saved in all_filenames
combined_csv = pd.concat([pd.read_csv(f, encoding='ascii', engine='python') for f in all_filenames], sort=True, )


print('Rows and columns: %s' % str(combined_csv.shape))
combined_csv = combined_csv.drop_duplicates()
print('Rows and columns: %s' % str(combined_csv.shape))
print(pd.unique(combined_csv['serial_number']))
for col in combined_csv.columns:
    print(col)

# export to csv
combined_csv.to_csv("combined_loc.csv", index=False, encoding='utf-8-sig')
