# # unit tests
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import mock

import evaluation
from database import Database
db = Database()

def test_eval_and_write(mocker):
    print(os.getcwd())
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'evaluation.evaluation_loop',
        return_value=(.555, .444, .333)
    )
    evaluation.eval_and_write(db, 'test')
    assert True
