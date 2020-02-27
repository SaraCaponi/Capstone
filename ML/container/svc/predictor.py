# Implements a Flask server in order to do predictions.

from __future__ import print_function

import os
import pickle

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