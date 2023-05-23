#ECM1400 Programming Continuous Assessment
'''This module contains pytest unit tests for each function in utils

Imports:
pytest - The testing framework
utils.sumvalues - Function to be tested
utils.maxvalue - Function to be tested
utils.minvalue - Function to be tested
utils.meanvalue - Function to be tested
utils.countvalue - Function to be tested
'''
#Imports:
import pytest
from utils import sumvalues, maxvalue, minvalue, meannvalue, countvalue

#sumvalues

def test_sumvalues_valid():
    '''Test sumvalues() with a valid list'''
    assert sumvalues([1, 2, 3, 4.5]) == 10.5

def test_sumvalues_empty():
    '''Test sumvalues() with an empty list'''
    assert sumvalues([]) == 0

def test_sumvalues_one():
    '''Test sumvalues() with a list containing only one value'''
    assert sumvalues([5]) == 5

def test_sumvalues_non_numerical():
    '''Test sumvalues() with a list containing non_numerical values'''
    with pytest.raises(ValueError):
        sumvalues(['a', 7])

#maxvalue

def test_maxvalue_valid():
    '''Test maxvalue() with a valid list'''
    assert maxvalue([17, 4.8, 12, 33.4, 1]) == 3

def test_maxvalue_empty():
    '''Test maxvalue() with an empty list'''
    assert maxvalue([]) == 0

def test_maxvalue_one():
    '''Test maxvalue() with a list containing only one value'''
    assert maxvalue([9.2]) == 0

def test_maxvalue_non_numerical():
    '''Test maxvalue() with a list containing non_numerical values'''
    with pytest.raises(ValueError):
        maxvalue([3, 'b'])

#minvalue

def test_minvalue_valid():
    '''Test minvalue() with a valid list'''
    assert minvalue([12.2, 3, 8, 75, 1.8]) == 4

def test_minvalue_empty():
    '''Test minvalue() with an empty list'''
    assert minvalue([]) == 0

def test_minvalue_one():
    '''Test minvalue() with a list containing only one value'''
    assert minvalue([20]) == 0

def test_minvalue_non_numerical():
    '''Test minvalue() with a list containing non_numerical values'''
    with pytest.raises(ValueError):
        minvalue([3, 'b'])

#meannvalue

def test_meannvalue_valid():
    '''Test meannvalue() with a valid list'''
    assert meannvalue([5, 6, 7, 8]) == 6.5

def test_meannvalue_empty():
    '''Test meannvalue() with an empty list'''
    assert meannvalue([]) == 0

def test_meannvalue_one():
    '''Test meannvalue() with a list containing only one value'''
    assert meannvalue([23.7]) == 23.7

def test_meannvalue_non_numerical():
    '''Test meannvalue() with a list containing non_numerical values'''
    with pytest.raises(ValueError):
        meannvalue([12, 'c', 5.02])

#countvalue

def test_countvalue_one_occurrence():
    '''Test countvalue() on a valid list with one occurrence of the given value'''
    assert countvalue([2, 4, 6.5, 9, 30], 4) == 1

def test_countvalue_multiple_occurrence():
    '''Test countvalue() on a valid list with more than one occurrence of the given value'''
    assert countvalue([3, 8, 2, 12, 8, 1, 2, 9, 8], 8) == 3

def test_countvalue_not_in_list():
    '''Test countvalue() on a list where the given value is not present'''
    assert countvalue([12, 7], 15.4) == 0

def test_countvalue_empty():
    '''Test countvalue() with an empty list'''
    assert countvalue([], 5) == 0

def test_countvalue_one():
    '''Test countvalue() with a list containing only one value'''
    assert countvalue([8], 8) == 1

def test_countvalue_non_numerical():
    '''Test countvalue() on a valid list that contains non_numerical characters'''
    assert countvalue([4, 'a', 7, 'b', 'c', '', 0], 'c') == 1

 