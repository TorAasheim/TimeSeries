import pandas as pd
import matplotlib.pyplot as plt
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.models import RNNModel
from darts.metrics import mape
from darts.utils.timeseries_generation import datetime_attribute_timeseries

df = pd.read_csv('processedData.csv')
df = df.loc[df['trip_id'] == 1.0]  # 1, 34, 42, 600.0, 602.0, 603.0, 1672.0, 1725.0,
data = df[['timestamp_utc', 'speed_kmh']]
data = data.sort_values(by='timestamp_utc', ascending=True)
data['timestamp_utc'] = pd.to_datetime(data['timestamp_utc']).dt.tz_localize(None)

ts = TimeSeries.from_dataframe(df=data, time_col='timestamp_utc', value_cols=None, freq="5s")
train, val = ts.split_before(0.7)

transformer = Scaler()
train_transformed = transformer.fit_transform(train)
val_transformed = transformer.transform(val)
series_transformed = transformer.transform(ts)

date_series = datetime_attribute_timeseries(pd.date_range(start=ts.start_time(), freq=ts.freq_str, periods=1000),
                                            attribute='year', one_hot=False)
series = Scaler().fit_transform(date_series)
covariates_series = datetime_attribute_timeseries(series, attribute='month', one_hot=True)
covariates = series.stack(covariates_series)
cov_train, cov_val = covariates.split_before(0.5)

model = RNNModel(
    model='LSTM', #LSTM #RNN Defines wich NN model will be used
    hidden_dim=20,
    dropout=0,
    batch_size=1,
    n_epochs=300,
    model_name='LSTM', #LSTM #RNN
    random_state=42,
    training_length=40,
    force_reset=True,
    n_rnn_layers= 5,
    input_chunk_length=5
)

model.fit(train_transformed,
          future_covariates=covariates,
          val_series=val_transformed,
          val_future_covariates=covariates,
          verbose=True)


def eval_model(model):
    pred_series = model.predict(n=25, future_covariates=covariates)
    plt.figure(figsize=(8, 5))
    series_transformed.plot(label='actual')
    pred_series.plot(label='forecast')
    plt.title('MAPE: {:.2f}%'.format(mape(pred_series, val_transformed)))
    plt.legend();
    plt.show()


eval_model(model)

