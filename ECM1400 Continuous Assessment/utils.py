#ECM1400 Programming Continuous Assessment
'''The utils file for the AQUA platform, containing functions that may be used throughout multiple parts of the system

Functions:
sumvalues() - Calculates the sum of all values in the given sequence
maxvalue() - Returns the index of the maximum value in a given sequence
minvalue() - Returns the index of the minimum value in a given sequence
meannvalue() - Returns the arithmetic mean of all the values in a given sequence
countvalue() - Returns the number of occurences of a certain value within a given sequence
'''
def sumvalues(values):
    """Calculates the sum of the values in the given sequence, raising an exception if there are non-numerical values
    
    Paramaters:
    values - The sequence of values to calculate the sum of
    
    Return values:
    values_sum - The total of each element in values
    """
    if len(values) == 0:
        return 0   
    values_sum = 0
    for item in values:
        if (isinstance(item, float) or isinstance(item, int)): #check the data type is valid
            values_sum += item
        else:
            raise ValueError('Non-numerical value found while trying to calculate sum.')
    return values_sum

def maxvalue(values):
    """Finds the index of the maximum value in the given sequence, raising an exception if there are non-numerical values
    
    Paramaters:
    values - The sequence of values to find the maximum value of
    
    Return values:
    max_value_index - The index of the found maximum within the sequence
    """       
    max_value_index = 0
    for item in values:
        if (isinstance(item, float) or isinstance(item, int)): 
            if item > values[max_value_index]:
                max_value_index = values.index(item)
        else:
            raise ValueError('Non-numerical value found while trying to find maximum.')
    return max_value_index

def minvalue(values):
    """Finds the index of the minimum value in the given sequence, raising an exception if there are non-numerical values
    
    Paramaters:
    values - The sequence of values to find the minimum value of
    
    Return values:
    min_value_index - The index of the found minimum within the sequence
    """    
    min_value_index = 0
    for item in values:
        if (isinstance(item, float) or isinstance(item, int)): 
            if item < values[min_value_index]:
                min_value_index = values.index(item)
        else:
            raise ValueError('Non-numerical value found while trying to find minimum.')
    return min_value_index

def meannvalue(values):
    """Calculates the arithmetic mean of the values in the given sequence, raising an exception if there are non-numerical values
    
    Paramaters:
    values - The sequence of values to find the mean of
    
    Return values:
    values_mean - The calculated mean value
    """    
    #Deal with an empty list
    if len(values) == 0:
        return 0
    
    total = sumvalues(values) #if non-numerical values are found n exception is raised in sumvalues()
    values_mean = total / len(values)
    return values_mean
 
def countvalue(values,xw):
    """Counts the number of occurrences of a given value within a given sequence
    
    Paramaters:
    values - The sequence of values to find the entry in
    xw - The entry to be counted
    
    Return values:
    xw_occurrences - The number of ocurrences of xw in values
    """   
    xw_occurrences = 0
    for item in values:
        if item == xw:
            xw_occurrences +=1
    return xw_occurrences


