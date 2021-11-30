import pandas as pd
from darts import TimeSeries
from darts.models import ExponentialSmoothing
from darts.metrics import mape
import matplotlib.pyplot as plt
from darts.dataprocessing.transformers.scaler import Scaler

df = pd.read_csv('processedData.csv')
df = df.loc[df['trip_id'] == 34.0]  # 1, 34, 42, 600.0, 602.0, 603.0, 1672.0, 1725.0,
data = df[['timestamp_utc', 'speed_kmh']]
data = data.sort_values(by='timestamp_utc', ascending=True)
data['timestamp_utc'] = pd.to_datetime(data['timestamp_utc']).dt.tz_localize(None)

ts = TimeSeries.from_dataframe(data, 'timestamp_utc', value_cols = None, freq="5s")
trainData, testData = ts.split_before(0.7)
transformer = Scaler()

train_transformed = transformer.fit_transform(trainData)
test_transformed = transformer.transform(testData)
series_transformed = transformer.transform(ts)

# Train
model = ExponentialSmoothing(trend=None, seasonal=None) #simple exponential smoothing, see darts documentation for explanation
model.fit(train_transformed)

# predict
prediction = model.predict(n=25, num_samples=2) #Cange samples for nr of timesteps, n can be set to len(test_transformed) to predict rest of the series

# plot
series_transformed.plot(label='actual')
prediction.plot(label='predict')
plt.title('MAPE: {:.2f}%'.format(mape(prediction, test_transformed)))
plt.legend()
plt.show()









