# Implements a Flask server in order to do predictions.

from __future__ import print_function

import os
import pickle
from io import StringIO

import flask

import pandas as pd

prefix = '/opt/ml/'

model_path = os.path.join(prefix, 'model')


class ScoringService(object):
    model = None

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""

        if cls.model == None:
            with open(os.path.join(model_path, 'svc-model.pkl'), 'r') as f:
                cls.model = pickle.load(f)

        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, make and return the predictions.

        Args:
            input (a pandas dataframe): The data on which to make the predictions. 
                There will be one prediction per row in the dataframe."""

        classifier = cls.get_model()

        return classifier.predict(input)

app = flask.Flask(__name__)

@app.route('ping', methods=['POST'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully.
    """

    health = ScoringService.get_model() is not None

    status = 200 if health else 404

    return flask.Response(response='\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    """Make predictions on a single batch of data. In this sample server, we take data as 
    # TODO Input data specs??
    convert it to a pandas dataframe for internal use and then convert the predictions back to 
    # TODO Output data specs??
    """

    data = None

    # TODO Input data spec
    if flask.request.content_type == 'TBD':
        data = flask.request.data.decode('utf-8')
        s = StringIO.StringIO(data)
        # TODO Input data spec
        data = pd.read_csv(s, header=None)
    else:
        # TODO Input data spec
        return flask.Response(response='The predictor only supports TDB data', status=415, mimetype='text/plain')

    print('Invoked with {} records.'.format(data.shape[0]))

    predictions = ScoringService.predict(data)

    out = StringIO.StringIO()
    # TODO Output data spec
    pd.DataFrame({'results':predictions}).to_csv(out, header=False, index=False)
    result = out.getvalue()

    return flask.Response(response=result, status=200, mimetype='text/csv')