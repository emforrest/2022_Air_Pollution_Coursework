#ECM1400 Programming Continuous Assessment
'''The monitoring file for the AQUA platform, presenting real-time statistics for a range of monitoring stations and pollutants

Imports:
requests - Used to make a call to the Air Pollution API and retrieve the pollution data
datetime - Used to handle date objects associated with pollutant measurements
plt - Used to plot the graph in compare_two_stations()
main.user_input - Checks that the user's input is valid
utils.meannvalue - Returns the arithmetic mean of all the values in a given sequence

Functions:
one_pollutant_at_different_stations() - Finds the levels of a pollutant at each monitoring station
pollutant_levels_at_a_station() - Displays the average levels of each pollutant at a monitoring station
health_recommendations_per_station() - Displays the air quality band and health recommendations for each pollutant at a monitoring station
compare_two_stations() - Produces a line graph comparing the levels of a pollutant at two monitoring stations
quick_sort() - Sorts the monitoring stations into descending order of pollutant level for the chosen pollutant
partition() - The partitioning algorithm used to arrange values within the quick sort
get_pollutants() - Returns a list of pollutants
get_monitoring_stations() - Returns a dictionary containing the monitoring stations
user_select_pollutant() - Prompts the user to select a pollutant
user_select_monitoring_station - Prompts the user to select a monitoring station
get_live_data - Returns data from the API based on the provided URL
'''
#Imports:
import requests
import datetime
import matplotlib.pyplot as plt
from main import user_input
from utils import meannvalue

#My available functions

def one_pollutant_at_different_stations():
    """Asks the user to choose a pollutant, finds the average values of this pollutant at each monitoring station over the past week, and sorts them using the quick sort and stores the result in a text file, outputting the three stations with the most and the three with the least"""
    station_averages = [] #A 2D array containing each station name and its average value for this polllutant over the past week
    monitoring_stations = get_monitoring_stations()

    #Select a pollutant
    species_code = user_select_pollutant()

    #Get the start and end of the current week
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days = 7)

    print('\nRetrieving live data...')
    for group in monitoring_stations:
        for station in monitoring_stations[group]['values']:
            site_code = station[0]
            site_name = station[1]
            week_values = [] #List of recorded values over the week period for this station
            
            #Retreive the data values
            data = get_live_data('https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json', site_code, species_code, start_date, end_date)
            if data['RawAQData']['Data'][0]['@Value'] != '': #if a value exists
                week_values.append(float(data['RawAQData']['Data'][0]['@Value'])) #append the value into week_values
            
            #Find the average level over this week
            weekly_average = meannvalue(week_values)
            station_averages.append([site_name, weekly_average])
            
    #Sort the averages into descending order
    station_averages = quick_sort(station_averages, 0, len(station_averages) -1)

    #Write the result into a text file
    output_filename =  species_code.lower() + '_results.txt'
    complete_output_filename = './data/' + output_filename
    output_file = open(complete_output_filename, 'w')
    output_file.writelines(f'Average levels of {species_code} from {start_date} to {end_date}, from most to least:')

    for station_average in station_averages:
        station_name = station_average[0]
        station_average_value = station_average[1]
        output_line = f'\n{station_name} : {station_average_value}'
        output_file.writelines(output_line)
    output_file.close()
    
    #Output the top 3 and bottom 3 stations and alert the user that a file has been saved
    print(f'''
The three stations with the most {species_code} from {start_date} to {end_date}:
    
    {station_averages[0][0]} : {station_averages[0][1]}
    {station_averages[1][0]} : {station_averages[1][1]}
    {station_averages[2][0]} : {station_averages[2][1]}
    
The three stations with the least {species_code} from {start_date} to {end_date}:

    {station_averages[-1][0]} : {station_averages[-1][1]}
    {station_averages[-2][0]} : {station_averages[-2][1]}
    {station_averages[-3][0]} : {station_averages[-3][1]}

The results for every monitoring station have been saved to {output_filename}.
''')

def pollutant_levels_at_a_station():
    """Asks the user to choose a monitoring station, finds and displays the average pollutant levels for each pollutant over the past week"""
    #Select a monitoring station
    site_code, site_name = user_select_monitoring_station()
    
    #Get the start and end of the current week
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days = 7)

    #Get the average pollutant levels for each pollutant over the last week
    pollutant_averages = {} 
    pollutant_values = [] #values for each specific pollutant in turn
    pollutant_codes = []
    pollutants = get_pollutants()
    for x in pollutants:
        pollutant_codes.append(x[0])

    data = get_live_data('https://api.erg.ic.ac.uk/AirQuality/Data/Site/SiteCode={site_code}/StartDate={start_date}/EndDate={end_date}/Json', site_code, start_date, end_date)
    for species_data in data['AirQualityData']['Data']:
        if species_data['@SpeciesCode'] in pollutant_codes: #make sure the code corresponds to a pollutant
            if species_data['@Value'] != '' : #ignore when there is no data
                    pollutant_values.append(float(species_data['@Value']))
            pollutant_average = meannvalue(pollutant_values)
            pollutant_averages[species_data['@SpeciesCode']] = pollutant_average

    #Output the result
    pollutant_codes = list(pollutant_averages.keys())
    print(f'\nAverage pollutant values at {site_name} from {start_date} to {end_date}:')
    for i in range(len(pollutant_codes)):
        print(f'\n    {pollutant_codes[i]} : {pollutant_averages[pollutant_codes[i]]}')

def health_recommendations_per_station():
    """Asks the user to choose a monitoring station, checks the air quality index last recorded for each pollutant and outputs relevant health recommendations"""
    #Get the health recommendations for each air quality band
    health_data = {'Low' : {'At-risk individuals': 'Enjoy your usual outdoor activities.', 'General population':'Enjoy your usual outdoor activities.'}, 'Moderate': {'At-risk individuals': 'Adults and children with lung problems, and adults with heart problems, who experience symptoms, should consider reducing strenuous physical activity, particularly outdoors.', 'General population':'Enjoy your usual outdoor activities.'}, 'High':{'At-risk individuals': 'Adults and children with lung problems, and adults with heart problems, should reduce strenuous physical exertion, particularly outdoors, and particularly if they experience symptoms. People with asthma may find they need to use their reliever inhaler more often. Older people should also reduce physical exertion.', 'General population':'Anyone experiencing discomfort such as sore eyes, cough or sore throat should consider reducing activity, particularly outdoors.'}, 'Very High': {'At-risk individuals' : 'Adults and children with lung problems, adults with heart problems, and older people, should avoid strenuous physical activity. People with asthma may find they need to use their reliever inhaler more often.', 'General population':'Reduce physical exertion, particularly outdoors, especially if you experience symptoms such as cough or sore throat.'}}
    
    #Selet a monitoring station
    site_code, site_name = user_select_monitoring_station()
 
    #Output the air quality data and relevant health advice
    air_quality_data = get_live_data('https://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/Latest/SiteCode={site_code}/Json', site_code)
    for pollutant in air_quality_data['DailyAirQualityIndex']['LocalAuthority']['Site']['Species']:
        print(f'''
    {pollutant['@SpeciesCode']}:
    Air Quality Index = {pollutant['@AirQualityIndex']}
    Air Quality Band = {pollutant['@AirQualityBand']}

    Health advice for individuals at {site_name} based on {pollutant['@SpeciesCode']} levels:
    General population : {health_data[pollutant['@AirQualityBand']]['General population']}
    At-risk individuals : {health_data[pollutant['@AirQualityBand']]['At-risk individuals']}
''')

def compare_two_stations():
    """Plots a line graph comparing the levels of a pollutant at two different monitoring stations over the last week"""
    #Select a pollutant
    species_code = user_select_pollutant()

    #Select two monitoring stations
    print('Select two monitoring stations to compare.')
    print('\nMonitoring station 1:')
    site_1_code, site_1_name = user_select_monitoring_station()
    print('\nMonitoring station 2:')
    site_2_code, site_2_name = user_select_monitoring_station()

    #Get the start and end of the current week
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days = 7)
    
    #Get the values for this pollutant at each monitoring station over this week
    site_code = site_1_code
    data_times = [] #contains the dates and times for which each value was recorded
    site_1_data = []
    data = get_live_data('https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json', site_code, species_code, start_date, end_date)
    for x in data['RawAQData']['Data']:
        data_times.append(datetime.datetime.strptime(x['@MeasurementDateGMT'], "%Y-%m-%d %H:%M:%S"))
        if x['@Value'] != '': #handle missing data
            site_1_data.append(float(x['@Value']))
        else:
            site_1_data.append(None)

    site_code = site_2_code
    site_2_data = []
    data = get_live_data('https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json', site_code, species_code, start_date, end_date)
    for x in data['RawAQData']['Data']:
        if x['@Value'] != '':
            site_2_data.append(float(x['@Value']))
        else:
            site_2_data.append(None)
    
    plt.clf() #clears the figure so if this function is called multiple times the results of the previous call do not affect the current call

    #Set up the labels for the graph
    plt.title(f'{species_code} Levels')
    plt.xlabel('Date')
    plt.ylabel('Pollutant level')

    #Plot the values onto the graph
    plt.plot_date(data_times, site_1_data, '-g', label = site_1_name)
    plt.plot_date(data_times, site_2_data, '-b', label = site_2_name)
    plt.legend()

    #Save the graph
    output_filename = species_code.lower() + '_' + site_1_name.lower().replace(' ', '_') + '_' + site_2_name.lower().replace(' ', '_') + '_graph.png'
    complete_output_filename = './data/' + output_filename
    plt.savefig(complete_output_filename)
    print(f'\nA line chart showing the levels of {species_code} at these two stations has been saved to {output_filename}.')
    print('\nNote that not all monitoring stations have data for all pollutants, so not all graphs generated will have two lines. An example of a graph which does have two lines is O3 at Thurrock - London Road (Grays) and Lewisham - Honor Oak Park.')

#Other functions used in this section

def quick_sort(station_values, start_index, end_index):
    '''Given a list containing the average pollutant values for each station, sorts its elements into descending order using the quick sort
    
    Paramaters:
    station_values - The list containing the station codes and their average values
    start_index - The index of the first item to be sorted within this iteration
    end_index - The index of the last item to be sorted within this iteration
    
    Return values:
    station_values - The sorted list
    '''
    if start_index < end_index: #if the indices are the same then they point to the same element - don't try to sort it with itself
        pivot_index = partition(station_values, start_index, end_index) #the index with which to split the array
        
        #Sort the two halves of the array
        station_values = quick_sort(station_values, start_index, pivot_index -1)
        station_values = quick_sort(station_values, pivot_index, end_index)
    return station_values

def partition(station_values, start_index, end_index):
    '''The partitioning function used in the quick sort algorithm, finding the central element and placing other elements before or after it depending on their value
    
    Paramaters:
    station_values - The list containing the station codes and their average values
    start_index - The index of the first item to be sorted within this iteration
    end_index - The index of the last item to be sorted within this iteration
    
    Return values:
    i + 1 - The position of the pivot element after the current array has been sorted around it
    '''
    pivot = int(station_values[end_index][1]) #extract the component length of the final component, this is our pivot value
    i = start_index -1
    for j in range (start_index, end_index):
        element = int(station_values[j][1])
        if element >= pivot: #if a greater element is found it should be moved to before the pivot
            i+=1

            #Swap the elements at i and j
            station_values[i], station_values[j] = station_values[j], station_values[i]

    #Make sure the pivot is in the correct place
    station_values[i+1], station_values[end_index] = station_values[end_index], station_values[i+1]
    return i+1

def get_pollutants():
    '''Returns a list of the pollutants with data available
    
    Return values:
    pollutants - The list of pollutants
    '''
    print('\nGetting pollutants...')
    pollutants = []
    pollutants_data = get_live_data('https://api.erg.ic.ac.uk/AirQuality/Information/Species/Json')

    #Format the returned data
    for species in pollutants_data['AirQualitySpecies']['Species']:
        pollutants.append([species['@SpeciesCode'], species['@SpeciesName']])
    
    return pollutants

def get_monitoring_stations():
    '''Returns a dictionary containing each group and its related monitoring station codes and names
    
    Return values:
    stations - The dictionary of monitoring stations
    '''
    print('\nGetting monitoring stations...')
    stations = {} #A dictionary of the form {group name : {'description' = description, values = [[station code, station name] ...]} ...}
    groups = [] #A list of group names
    group_descriptions = {} #The lowercase group names and their corresponding description
    
    #Get each group name
    groups_data = get_live_data("https://api.erg.ic.ac.uk/AirQuality/Information/Groups/Json")
    for x in groups_data['Groups']['Group']:
        if x['@GroupName'].islower() and x['@Description'] != 'sub domain test': #lowercase names correspond to groups
            groups.append(x['@GroupName'])
            group_descriptions[x['@GroupName']] = x['@Description']
    
    #Iterate over each group to get its stations
    for group in groups:
        site_data = get_live_data(('https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName={group_name}/Json'), group_name = group)
        if site_data['Sites'] != None:
            for x in site_data['Sites']['Site']:
                if type(x) == dict:
                    station = [x['@SiteCode'], x['@SiteName']]

                    #Add this station to the dictionary
                    if group in stations:
                        stations[group]['values'].append(station)
                    else:
                        stations[group] = {'description': group_descriptions[group], 'values' : [station]}
                        
    return stations

def user_select_pollutant():
    '''Prompts the user to select a pollutant
    
    Return values:
    species_code - The code used to represent the selected pollutant
    '''
    #Output the pollutants
    pollutants = get_pollutants()
    print('\nSelect a pollutant:')
    for pollutant_index, pollutant in enumerate(pollutants):
        species_code = pollutant[0]
        species_name = pollutant[1]
        print(f'    "{pollutant_index+1}" - {species_name} {species_code}')
    
    #Handle the user input
    selected_pollutant_number = int(user_input([str(i) for i in range(len(pollutants)+1)]))
    selected_pollutant = pollutants[selected_pollutant_number -1]
    species_code = selected_pollutant[0]

    return species_code

def user_select_monitoring_station():
    '''Prompts the user to select a monitoring station
    
    Return values:
    site_code - The code used to represent the chosen station
    site_name - The name of the chosen station
    '''
    stations = get_monitoring_stations()
    print('\nSelect a location:')
    for group_index, group in enumerate(stations): #there are too many stations to select from all at once, so the user is prompted to choose a group first
        group_description = stations[group]['description']
        print(f'    "{group_index+1}" - {group_description}')
    selected_group_number = int(user_input([str(i) for i in range(len(stations)+1)]))
    stations_as_list = list(stations)
    selected_group = stations_as_list[selected_group_number -1]

    print('\nSelect a monitoring station:')
    group_stations = stations[selected_group]['values']
    for station_index, station_data in enumerate(group_stations):
        station_name = group_stations[station_index][1]
        print(f'    "{station_index+1}" - {station_name}')
    selected_station_number = int(user_input([str(i) for i in range(len(group_stations)+1)]))
    stations_as_list = list(group_stations)
    selected_station = stations_as_list[selected_station_number -1]

    site_code = selected_station[0]
    site_name = selected_station[1]
    return site_code, site_name

def get_live_data(endpoint, site_code='MY1',species_code='NO',start_date=None,end_date=None, group_name = None, date = None):
    """Return data from the LondonAir API using its AirQuality API
    
    Paramaters:
    endpoint - URL which leads to the desired data to retreive from the API
    site_code - The code used to represent a monitoring station
    species_code - The code used to represent a pollutant
    start_date - The date from which to begin collecting data
    end_date - The date from which to stop collecting data
    group_name - The name of a location containing multiple monitoring stations
    date - A single date to collect data from

    Return values:
    res - The resulting data from the API call
    """   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date,
        group_name = group_name,
        date = date
    )

    #Send a request to the API
    res = requests.get(url)
    return res.json()

#Provided function

def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date
    
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json