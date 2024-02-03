import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    
    #month10 = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-10.csv.gz'
    #month11 = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-11.csv.gz'
    #month12 = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-12.csv.gz'

    base_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-'

    taxi_dtypes = {
        'VendorID': 'Int64',
        'store_and_fwd_flag': 'str',
        'RatecodeID': 'Int64',
        'PULocationID': 'Int64',
        'DOLocationID': 'Int64',
        'passenger_count': 'Int64',
        'trip_distance': 'float64',
        'fare_amount': 'float64',
        'extra': 'float64',
        'mta_tax': 'float64',
        'tip_amount': 'float64',
        'tolls_amount': 'float64',
        'ehail_fee': 'float64',
        'improvement_surcharge': 'float64',
        'total_amount': 'float64',
        'payment_type': 'float64',
        'trip_type': 'float64',
        'congestion_surcharge': 'float64',
        'lpep_pickup_datetime': 'int64',  # Keep as integer for now
        'lpep_dropoff_datetime': 'int64'  # Keep as integer for now
    }

    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    
    #return pd.read_csv(month10, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates)

    data = pd.concat([pd.read_csv(f'{base_url}{month:02d}.csv.gz', sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates) for month in range(10, 13)])

    data['lpep_pickup_datetime'] = pd.to_datetime(data['lpep_pickup_datetime'], unit='ms')
    data['lpep_dropoff_datetime'] = pd.to_datetime(data['lpep_dropoff_datetime'], unit='ms')

    return data
    

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

