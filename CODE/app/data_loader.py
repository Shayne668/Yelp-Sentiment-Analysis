
# app/data_loader.py
import os
import pandas as pd
from flask_caching import Cache
from .constants import state_abbreviations

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

# Configuration for Flask-Caching
# Hopefully reduced the time to generate business specify analysis without re-reading entire csv file.
config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300,
}

cache = Cache(config=config)

@cache.memoize()
def load_csv_data(state):
    #print(DATA_FOLDER)
    csv_filename = os.path.join(DATA_FOLDER, f"{state}.csv")
    #print(csv_filename)
    return pd.read_csv(csv_filename).set_index("business_id")
