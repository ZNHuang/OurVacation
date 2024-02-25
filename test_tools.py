import pytest
from tools import *

def test_csv_to_dictionary():
    result, count = csv_to_dictionary("education_example.csv")
    assert count == 3