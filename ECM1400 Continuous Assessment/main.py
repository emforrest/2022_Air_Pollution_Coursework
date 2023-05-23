#ECM1400 Programming Continuous Assessment
'''The main file for the AQUA platform, handling user navigation between each module and allowing them to choose what functionality to access

Imports:
datetime - Used to handle date objects for reporting.peak_hour_date()
os - Used to check whether the file needed for intelligence.detect_connected_components() exists
mat_plot - Used to open IMG, the result of intelligence.find_red_pixels() or intelligence.find_cyan_pixels()
reporting - Contains functions from the PR module
intelligence - Contains functions from the IR module
monitoring - Contains functions from the MI module

Functions:
user_input() - User input validation
main_menu() - Navigation between modules
reporting_menu() - Navigation of the PR module
intelligence_menu() - Navigation of the MI module
monitoring_menu() - Navigation of the RM module
about() - Print the About text
quit() - Exit the platform
'''

#Imports:
import datetime
import os
from matplotlib import pyplot as mat_plot 
import reporting
import intelligence
import monitoring

#Functions:
def user_input(options):
    '''Repeadedly asks for user input until they input one of the available options
    
    Paramaters:
    options - List of available option strings

    Return values:
    selected - The valid option that the user chose
    '''
    selected = input('>>>')
    while selected not in options:
        print('Invalid input. Please only enter one of the available options (without quotation marks).')
        selected = input('>>>')
    return selected

def main_menu():
    """The main menu for the system, allowing the user to choose which module they would like to access"""
    while True: #the main menu is called until the user chooses to quit
    
        #Output options
        print('''
This is the NetZero AQUA platform.
    
Enter one of the following options:
    "R" - Access the Pollution Reporting module
    "I" - Access the Mobility Intelligence module
    "M" - Access the Real-time Monitoring module
    "A" - Return the About text
    "Q" - Quit the platform
''')

        #Handle the user's input
        selected = user_input(["R", "I", "M", "A", "Q"])
    
        #Direct the user to the indicated function
        if selected == 'R':
            reporting_menu()
        elif selected == 'I':
            intelligence_menu()
        elif selected == 'M':
            monitoring_menu()
        elif selected == 'A':
            about()
        elif selected == 'Q':
            quit()

def reporting_menu():
    """The menu for the PR module, letting the user explore the different options for analysing pollutant data"""
    #Select a monitoring station
    
    #Output options
    print('''
Select a monitoring station:
    "1" - Marylebone Road
    "2" - N. Kensington
    "3" - Harlington
''')

    #Handle user input
    monitoring_station = user_input(["1", "2", "3"])

    #Read the relevant data file
    if monitoring_station == '1':
        data = open('./data/Pollution-London Marylebone Road.csv') 
    elif monitoring_station == '2':
        data = open('./data/Pollution-London N Kensington.csv')
    elif monitoring_station == '3':
        data = open('./data/Pollution-London Harlington.csv')

    #Select a pollutant 

    #Output options
    print('''
Select a pollutant:
    "1" - Nitric oxide 
    "2" - PM10 inhalable particulate matter
    "3" - PM2.5 inhalable particulate matter
''')

    #Handle user input
    pollutant = user_input(["1", "2", "3"])

    #Select a function
    selected = ''
    while selected != "B": #"B" is used to return to the main menu

        #Output options
        print('''
Select an option:
    "1" - Calculate daily averages
    "2" - Calculate daily medians
    "3" - Calculate hourly averages
    "4" - Calculate monthly averages
    "5" - Calculate the peak hour for a given date
    "6" - Count missing data entries
    "7" - Enter a missing data entry
    "B" - Back to main menu    
''')
        #Handle user input
        selected = user_input(['1', '2', '3', '4', '5', '6', '7', 'B'])

        #Call the selected function
        if selected == '1':
            result = reporting.daily_average(data, monitoring_station, pollutant)
            print(result) 
        elif selected == '2':
            result = reporting.daily_median(data, monitoring_station, pollutant)
            print(result)
        elif selected == '3':
            result = reporting.hourly_average(data, monitoring_station, pollutant)
            print(result)
        elif selected == '4':
            result = reporting.monthly_average(data, monitoring_station, pollutant)
            print(result)
        elif selected == '5':
            #Input the date to work on
            print('Enter the date to use in the format dd/mm/yyyy:')
            user_date = input('>>>')
            valid_date = False

            while not valid_date:
                try: #test whether the user's input corresponds to a valid date
                    user_date = user_date.split('/') #split user_date into a list with the day, month and year
                    if len(user_date) == 3: #check there were the correct number of values
                        user_date = list(map(int, user_date)) #convert each to an integer
                        user_date = datetime.date(user_date[2], user_date[1], user_date[0]) #convert to a datetime date object
                        if datetime.date(2021, 1, 1) <= user_date <= datetime.date(2021, 12, 31): #check the date is within the range of available dates
                            valid_date = True #the while loop only breaks if all these conditions are met
                except ValueError:
                    pass #if there was an error interpreting the input as a date, it also counts as invalid so nothing extra needs to be done

                #Re-input if the date was not valid
                if not valid_date:
                    print('Invalid input. Please enter a date between 01/01/2021 and 31/12/2021 using that format.')
                    user_date = input('>>>')
            
            #Call the function
            result = reporting.peak_hour_date(data, user_date, monitoring_station, pollutant)
            print(result)
        elif selected == '6':
            result = reporting.count_missing_data(data, monitoring_station, pollutant)
            print(result)
        elif selected == '7':
            #Input a new value to replace the missing values
            print('Enter a value to replace the missing data with:')
            new_value = input('>>>')

            #Call the function
            result = reporting.fill_missing_data(data, new_value, monitoring_station, pollutant)
            print(result)
            
    data.close()

def intelligence_menu():
    """The menu for the MI module, allowing the user to explore the different options for walkability analysis"""
    MARK = [] #Generated in option 3, and must exist in order to use option 4

    #Select a function
    selected = ''
    while selected != "B":

        #Output options
        print('''
Select an option:
    "1" - Find red pixels
    "2" - Find cyan pixels
    "3" - Detect connected components
    "4" - Sort connected components
    "B" - Back to main menu    
''')
        #Handle user input
        selected = user_input(['1', '2', '3', '4', 'B'])

        #Call the selected function
        if selected == '1':
            #Enter the filename for the map file
            print('Enter the name of the image file containing the road map (e.g. "map.png"):')
            map_filename = input('>>>')
            if os.path.exists('./data/'+map_filename):
                result = intelligence.find_red_pixels(map_filename, upper_threshold = 100, lower_threshold = 50)
            else:
                result = f'The file "{map_filename}" was not found in the data folder.'
            print(result)

        elif selected == '2':
            print('Enter the name of the image file containing the road map (e.g. "map.png"):')
            map_filename = input('>>>') 
            if os.path.exists('./data/'+map_filename):
                result = intelligence.find_cyan_pixels(map_filename, upper_threshold = 100, lower_threshold = 50)
            else:
                result = f'The file "{map_filename}" was not found in the data folder.'
            print(result)

        elif selected == '3':
            #Select which image to use
            print('''
Find connected components for all red pixels or all cyan pixels?
    "1" - Red pixels
    "2" - Cyan pixels
''')
            selected = user_input(['1', '2'])
                
            #Check if the required file exists
            if selected == '1':
                components_filename = './data/map-red-pixels.jpg'
                if os.path.exists(components_filename): 
                    IMG = mat_plot.imread(components_filename)
                    #Call the function
                    result, MARK = intelligence.detect_connected_components(IMG)
                else:

                    #Alert the user that the file was not found.
                    result = 'The required file "map-red-pixels.jpg" was not found. You should use the option "Find red pixels" before selecting this option.'
            elif selected == '2':
                components_filename = './data/map-cyan-pixels.jpg'
                if os.path.exists(components_filename):
                    result, MARK = intelligence.detect_connected_components(components_filename)
                else:
                    result = 'The required file "map-cyan-pixels.jpg" was not found. You should use the option "Find cyan pixels" before selecting this option.'
           
            print(result) 
        
        elif selected == '4':
            #The file 'cc_output_2a.txt' must be present in order to use this feature, do not allow access if it doesn't exist.
            connected_components_filename = './data/cc-output-2a.txt'
            if os.path.exists(connected_components_filename):
                result = intelligence.detect_connected_components_sorted(MARK)
                print(result) 
            else:
                #Alert the user that they need to use option 3 before using this option
                print('You should use the option "Detect connected components" before selecting this option.')

def monitoring_menu():
    """The Menu for the RM module, providing analytics on real time data from the London Air API"""
    #Select a function
    selected = ''
    while selected != "B":

        #Output options
        print('''
Select an option:
    "1" - Compare the levels of a pollutant at different monitoring stations
    "2" - See the levels of different pollutants at a monitoring station
    "3" - See the air pollution stats and health advice at a monitoring station
    "4" - Compare the levels of a pollutant at two monitoring stations
    "B" - Back to main menu    
''')
        #Handle user input
        selected = user_input(['1', '2', '3', '4', 'B'])

        #Call the selected function
        if selected == '1':
            monitoring.one_pollutant_at_different_stations()
        elif selected == '2':
            monitoring.pollutant_levels_at_a_station()
        elif selected == '3':
            monitoring.health_recommendations_per_station()
        elif selected == '4':
            monitoring.compare_two_stations()

def about():
    """Prints the module code and my candidate number"""
    print('''
Module Code : ECM1400
Candidate Number : 234689''')

def quit():
    """Exits the program"""
    print('\nThank you for using the AQUA platform.')
    exit()

if __name__ == '__main__':
    main_menu()
