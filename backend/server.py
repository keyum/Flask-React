
import pandas as pd
import simplejson as json
from flask import Flask

app = Flask(__name__)


@app.route('/names/<page>')
def cvs_list(page):
    arr = get_data(page)
    return json.dumps(arr, ignore_nan=True)


def get_data(index):
    csv = pd.read_csv(f'csv/download990xml_2020_{index}.csv', header=None)
    return csv.loc[:, 0].tolist()
