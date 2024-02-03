if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    # Specify your transformation logic here

    zero_passenger_count = data[data['passenger_count'].isin([0])]
    zero_trip_distance = data[data['trip_distance'].isin([0])]
    
    data = data[~data['passenger_count'].isin([0])]
    data = data[~data['trip_distance'].isin([0])]

    # Convert 'lpep_pickup_datetime' to datetime
    data['lpep_pickup_datetime'] = pd.to_datetime(data['lpep_pickup_datetime'])

    # Create the new column 'lpep_pickup_date' by extracting the date
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    
    return data