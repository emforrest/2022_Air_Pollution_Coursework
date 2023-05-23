#ECM1400 Programming Continuous Assessment
'''The reporting file for the AQUA platform, allowing the user to view statistics generated from the air pollution datasets for each of the three monitoring stations

Imports:
csv - Used to save changes to a file in fill_missing_data()
utils.meannvalue - Returns the arithmetic mean of all the values in a given sequence
utils.maxvalue - Returns the index of the maximum value in a given sequence
utils.countvalue - Returns the number of occurences of a certain value within a given sequence

Functions:
daily_average() - Calculates average pollutant levels per day
daily_median() - Calculates median pollutant levels per day
hourly_average() - Calculates average pollutant levels per hour
monthly_average() - Calculates average pollutant levels per month
peak_hour_date() - Finds the hour on a given day with the highest pollution level
count_missing_data() - Count the number of 'No data' entries
fill_missing_data() - Replace the 'No data' entries with a new value
'''
#Imports:
import csv
from utils import meannvalue, maxvalue, countvalue

def daily_average(data, monitoring_station, pollutant):
    """Calculate the average pollutant level per day for the given monitoring station and pollutant
    
    Parameters: 
    data - CSV file containing pollution data for the chosen station
    monitoring_station - Number corresponding to the chosen station
    pollutant - Number corresponding to the chosen pollutant
    
    Return values:
    result - A list of the averages to be displayed to the user
    """
    pollutant_levels = [] #list of pollutant levels per day
    averages = [] 
    line = data.readline() #the first line can be skipped as it contains the data headers
    line = data.readline()
    while line != '': #end of file
        values = line.strip().split(',') #a list containing each data item in the line

        try:
            #Add this value to the day's total
            pollutant_level = float(values[int(pollutant)+1]) #picks the value in the column with index 2, 3 or 4 depending on the pollutant
            pollutant_levels.append(pollutant_level)
            
        except ValueError:
            #This occurs if there is no data for this particular hour
            pass #move on to the next value
            
        #Check if this was the last measurement of the day
        if values[1] == '24:00:00':

            #Calculate the average
            day_average = meannvalue(pollutant_levels)
            averages.append(day_average)
            pollutant_levels = []
        
        #Read a new line
        line = data.readline()
    else:
        data.seek(0) #return to the start of the file if subsequent functions are called

    result = f'\nDaily averages:\n{averages}'
    return result
        
def daily_median(data, monitoring_station, pollutant):
    """Calculate the median pollutant level per day for the given monitoring station and pollutant
    
    Parameters: 
    data - CSV file containing pollution data for the chosen station
    monitoring_station - Number corresponding to the chosen station
    pollutant - Number corresponding to the chosen pollutant
    
    Return values:
    result - A list of the medians to be displayed to the user
    """
    medians = []
    pollutant_levels = [] 
    line = data.readline() 
    line = data.readline()
    while line != '': 
        values = line.strip().split(',')

        try:
            #Add this value to the list of values for this day
            pollutant_level = float(values[int(pollutant)+1]) 
            pollutant_levels.append(pollutant_level)
        except ValueError:
            pass

        #Check if this was the last measurement of the day
        if values[1] == '24:00:00':
            if pollutant_levels == []:
                median_value = 0
                medians.append(median_value)
            else:
                #Calculate the median
                pollutant_levels.sort(key = float)
                middle = (len(pollutant_levels)-1)/2
                if middle == round(middle): #if middle is an integer
                    medians.append(pollutant_levels[int(middle)])
                else:
                    #Take the sum of the central two values and divide by two
                    median_value = (pollutant_levels[int(middle-0.5)] + pollutant_levels[int(middle-0.5)])/2
                medians.append(median_value)
            pollutant_levels = []
        
        #Read a new line
        line = data.readline()
    else:
        data.seek(0) 

    result = f'\nDaily medians:\n{medians}'
    return result
    
def hourly_average(data, monitoring_station, pollutant):
    """Calculate the average pollutant level per hour for the given monitoring station and pollutant
    
    Parameters: 
    data - CSV file containing pollution data for the chosen station
    monitoring_station - Number corresponding to the chosen station
    pollutant - Number corresponding to the chosen pollutant
    
    Return values:
    result - A list of the averages to be displayed to the user
    """
    hourly_values = {} #contains lists of pollutant levels for each hour
    averages = []
    line = data.readline() 
    line = data.readline()
    while line != '': 
        values = line.strip().split(',')

        try:
            pollutant_level = float(values[int(pollutant)+1])
            hour = values[1]

            #Add this value into hourly_values
            if hour in hourly_values:
                hourly_values[hour].append(pollutant_level)
            else:
                hourly_values[hour] = [pollutant_level]
        except ValueError:
            pass    

        #Read a new line
        line = data.readline()
    else:
        data.seek(0)

        #Calculate the averages for each hour
        pollutant_levels = list(hourly_values.values())
        for hour_levels in pollutant_levels:
            hour_average = meannvalue(hour_levels)
            averages.append(hour_average) 

    result = f'\nHourly averages:\n{averages}'
    return result
    
def monthly_average(data, monitoring_station, pollutant):
    """Calculate the average pollutant level per month for the given monitoring station and pollutant
    
    Parameters: 
    data - CSV file containing pollution data for the chosen station
    monitoring_station - Number corresponding to the chosen station
    pollutant - Number corresponding to the chosen pollutant
    
    Return values:
    result - A list of the averages to be displayed to the user
    """
    pollutant_levels = [] #list of pollutant levels per month
    previous_month = '01'
    averages = [] 
    line = data.readline() 
    line = data.readline()
    while line != '': 
        values = line.strip().split(',')

        try:
            #Add this value to the month's total
            pollutant_level = float(values[int(pollutant)+1])
            pollutant_levels.append(pollutant_level) 

        except ValueError:
            pass 
            
        #Check if this was the last measurement of the month
        if values[0][5:7] != previous_month or (values[0] == '2021-12-31' and values[1] == '24:00:00'): #checking if a new month works for all but December, so the average must also be calculated when December 31 at 24:00 is reached
            #Calculate the average
            month_average = meannvalue(pollutant_levels)
            averages.append(month_average)

            previous_month = values[0][5:7]

            pollutant_levels = []
        
        #Read a new line
        line = data.readline()
    else:
        data.seek(0) 
    
    result = f'\nMonthly averages:\n{averages}'
    return result
     
def peak_hour_date(data, date, monitoring_station,pollutant):
    """Given a specific date, returns the hour with the highest level of pollution along with its value
    
    Parameters: 
    data - CSV file containing pollution data for the chosen station
    date - Chosen date to be analysed
    monitoring_station - Number corresponding to the chosen station
    pollutant - Number corresponding to the chosen pollutant
    
    Return values:
    result - The hour with the highest pollutant level and its value
    """
    level_per_hour = {} #contains the pollutant level for each hour in the chosen day
    line = data.readline() 
    line = data.readline()
    while line != '': 
        values = line.strip().split(',')

        #Check if this date matches the chosen date
        if values[0] == str(date):
            try:
                pollutant_level = float(values[int(pollutant)+1])
                level_per_hour[values[1]] = pollutant_level #add the pollutant level for this hour to the dictionary
            except ValueError:
                pass

        line=data.readline()
    else:
        data.seek(0)
    
    #Find the highest pollutant level
    pollutant_levels = list(level_per_hour.values())
    max_index = maxvalue(pollutant_levels)
    max_level = pollutant_levels[max_index]
    max_hour = list(level_per_hour.keys())[max_index]

    #Format the result into a string
    max_hour = max_hour[:5]
    max_level = str(max_level)
    result = f'\nHighest pollution level:\n({max_hour} , {max_level})'
    return result    

def count_missing_data(data,  monitoring_station,pollutant):
    """Return the number of 'No data' entries there are for the given monitoring station and pollutant
    
    Parameters: 
    data - CSV file containing pollution data for the chosen station
    monitoring_station - Number corresponding to the chosen station
    pollutant - Number corresponding to the chosen pollutant
    
    Return values:
    result - The number of missing values
    """
    pollutant_levels = []
    line = data.readline() 
    line = data.readline()
    while line != '': 
        values = line.strip().split(',')

        #Add this value into a list, pollutant_levels
        pollutant_level = values[int(pollutant)+1]
        pollutant_levels.append(pollutant_level)
        
        line = data.readline()
    else:
        data.seek(0)
    
    #Count the number of 'No data' entries
    no_data_count = countvalue(pollutant_levels, 'No data')

    result = f"\nNumber of 'No data' entries: {no_data_count}"
    return result

def fill_missing_data(data, new_value,  monitoring_station,pollutant):
    """Replace any instances of 'No data' for this station and pollutant with a given value
    
    Parameters: 
    data - CSV file containing pollution data for the chosen station
    new_value - Value chosen by the user to replace the 'No data' entries
    monitoring_station - Number corresponding to the chosen station
    pollutant - Number corresponding to the chosen pollutant
    
    Return values:
    result - Confirmation of changes
    """
    new_data = [] #Will be a 2D array containing each row, with the 'No data' entries replaced.
    line = data.readline() 
    line = data.readline()
    while line != '': 
        values = line.strip().split(',')
        new_data.append(values) #So new_file also contains the rows which aren't amended
        pollutant_level = values[int(pollutant)+1]
        
        #Check if this is a 'No data' entry
        if pollutant_level == 'No data':
            adjusted_values = values[:int(pollutant)+1] + [new_value] + values[int(pollutant)+2:] #replace the 'No data' entry with the chosen value 
            new_data[new_data.index(values)] = adjusted_values #replace the row in new_file to include this change

        line = data.readline()
    else:
        data.seek(0)

    #Get the filename of a new file to copy the changes into
    if monitoring_station == '1':
        new_file_name = './data/Pollution-London Marylebone Road copy.csv'
    elif monitoring_station == '2':
        new_file_name = './data/Pollution-London N Kensington copy.csv'
    elif monitoring_station == '3':
        new_file_name = './data/Pollution-London Harlington copy.csv'
    
    #Save a copy of the file with these changes
    new_csv_file = open(new_file_name, 'w', newline = '')
    csv_writer = csv.writer(new_csv_file) #using the imported module csv.writer to save as a csv file
    csv_writer.writerows(new_data)
    new_csv_file.close()

    new_file_name = new_file_name[7:] #remove the relative path section as the user doesn't need to see this
    result = f'\nChanges saved to "{new_file_name}".' 
    return result

    