#ECM1400 Programming Continuous Assessment
'''The intelligence file for the AQUA platform, allowing the user to analyse the walkability of a certain area based on a map image

Imports:
mat_plot - Used to open and save images
np - Used to edit numpy arrays which contain image data

Functions:
find_red_pixels() - Outputs a file highlighting all the red pixels from the input image
find_cyan_pixels() - Outputs a file highlighting all the cyan pixels from the input image
detect_connected_components() - Makes a list of all connected components within the result of find_red_pixels() or find_cyan_pixels()
detect_connected_components_sorted() - Sorts the previous list into decreasing order of size
'''
#Imports:
from matplotlib import pyplot as mat_plot 
import numpy as np

def bubble_sort(array):
    '''Given an array containing the connected components, sorts its elements into descending order of size using the bubble sort algorithm
    
    Paramaters:
    array - The array containing the connected components
    
    Return values:
    array - The sorted array of connected components
    '''
    for i in range(len(array)-1, 0, -1):
        swap = False #stop sorting once no swaps have been made
        for j in range(0, i):
            if int(array[j].strip().split('= ')[1]) < int(array[j+1].strip().split('= ')[1]): #the length of each component must be extracted from the line, so they can be ordered
                array[j], array[j+1] = array[j+1], array[j] #switch the order of the lines being compared
                swap = True
        if not swap:
            return array

def find_neighbours(current_pixel_indices, max_x, max_y):
    '''Given the indices of a pixel, finds the 8 neighbours of the pixel or as many as are within the bounds of the image
    
    Paramaters:
    current_pixel_indices - The x and y coordinates of the pixel within the image (starting from the top left corner as (0, 0))
    max_x - The maximum x value that a pixel can have (if it were greater it would not be within the image)
    max_y - The maximum y value a pixel can have
    
    Return values:
    neighbour_indices - A list containing the coordinates of the pixel's neigbouring pixels
    '''
    neighbour_indices = []
    #Top left
    if current_pixel_indices[0] -1 >=0 and current_pixel_indices[1] -1 >=0:
        neighbour_indices.append((current_pixel_indices[0] -1, current_pixel_indices[1] -1))
    #Top middle
    if current_pixel_indices[1] -1 >=0:
        neighbour_indices.append((current_pixel_indices[0],current_pixel_indices[1]-1))
    #Top right
    if current_pixel_indices[0] +1 <=max_x and current_pixel_indices[1] -1 >=0:
        neighbour_indices.append((current_pixel_indices[0] +1, current_pixel_indices[1] -1))
    #Middle left
    if current_pixel_indices[0] -1 >=0:
        neighbour_indices.append((current_pixel_indices[0] -1, current_pixel_indices[1]))
    #Middle right
    if current_pixel_indices[0] +1 <=max_x:
        neighbour_indices.append((current_pixel_indices[0] +1, current_pixel_indices[1]))
    #Bottom left
    if current_pixel_indices[0] -1 >=0 and current_pixel_indices[1] +1 <=max_y:
        neighbour_indices.append((current_pixel_indices[0] -1, current_pixel_indices[1] +1))
    #Bottom middle
    if current_pixel_indices[1] +1 <=max_y:
        neighbour_indices.append((current_pixel_indices[0], current_pixel_indices[1] +1))
    #Bottom right
    if current_pixel_indices[0] +1 <= max_x and current_pixel_indices[1] +1 <= max_y:
        neighbour_indices.append((current_pixel_indices[0] +1, current_pixel_indices[1] +1)) 

    return neighbour_indices 

def find_red_pixels(map_filename, upper_threshold = 100, lower_threshold = 50):
    """Given an input file, iterates over each pixel and returns an image containing the red pixels with any other colours black
    
    Paramaters:
    map_filename - Contains the filename for the input map image
    upper_threshold - Contains the upper threshold for the RGB channels, used to decide whether a pixel is red
    lower_threshold - Cotains the lower threshold for RGB channels, used to decide whether a pixel is red
    
    Return values:
    result - Confirmation that a new image has been saved
    """
    #Read the image
    map_filename = './data/' + map_filename
    map_file = mat_plot.imread(map_filename)
    
    #Create a copy which will be modified
    new_image = np.copy(map_file)
    new_image = np.multiply(new_image, 256).astype(int) #scale up the values to be a number between 0 and 255, and convert to integers

    #Iterate over the array to get each pixel's colour values
    for x in range(new_image.shape[0]):
        for y in range(new_image.shape[1]):
            
            #Decide whether this pixel is red (its red value is above the upper threshold and its blue and green values are below the lower threshold)
            if new_image[x][y][0] > upper_threshold and new_image[x][y][1] < lower_threshold and new_image[x][y][2] < lower_threshold:
                new_image[x][y] = np.array([255, 255, 255, 256])
            else:
                new_image[x][y] = np.array([0, 0, 0, 256])
    
    #Save the array as an image
    new_image= np.multiply(new_image, 1/256).astype(float)
    mat_plot.imsave('./data/map-red-pixels.jpg', new_image)

    result = "\nThe result has been successfully saved as 'map-red-pixels.jpg'."
    return result

def find_cyan_pixels(map_filename, upper_threshold = 100, lower_threshold = 50):
    """Given an input file, iterates over each pixel and returns an image containing the cyan pixels with any other colours black
    
    Paramaters:
    map_filename - Contains the filename for the input map image
    upper_threshold - Contains the upper threshold for the RGB channels, used to decide whether a pixel is cyan
    lower_threshold - Cotains the lower threshold for RGB channels, used to decide whether a pixel is cyan
    
    Return values:
    result - Confirmation that a new image has been saved
    """
    #Read the image
    map_filename = './data/' + map_filename
    map_file = mat_plot.imread(map_filename)
    
    #Create a copy which will be modified
    new_image = np.copy(map_file)
    new_image = np.multiply(new_image, 256).astype(int) 

    #Iterate over the array to get each pixel's colour values
    for x in range(new_image.shape[0]):
        for y in range(new_image.shape[1]):
            
            #Decide whether this pixel is cyan (its green and blue values are above the upper threshold and its red value is below the lower threshold)
            if new_image[x][y][0] < upper_threshold and new_image[x][y][1] >lower_threshold and new_image[x][y][2] > lower_threshold:
                new_image[x][y] = np.array([255, 255, 255, 256])
            else:
                new_image[x][y] = np.array([0, 0, 0, 256])
    
    #Save the array as an image
    new_image= np.multiply(new_image, 1/256).astype(float)
    mat_plot.imsave('./data/map-cyan-pixels.jpg', new_image)

    result = "\nThe result has been successfully saved as 'map-cyan-pixels.jpg'."
    return result

def detect_connected_components(IMG):
    """Given an input file containing a set of pixels, returns all the connected components within the image
    
    Paramaters:
    IMG - The file returned from one of the previous two functions from which connected components will be found
    
    Return values:
    result - Confirmation that a new text file containing the list of connected components has been saved
    MARK - A 2D array that records which pixels in IMG have been visited while traversing a connected component
    """
    upper_threshold = 200 #ensures that all pixels with colour values above this value are considered to be white pixels
    component_count = 0 #number of connected components
    connected_components = {} #contains the component number and its length

    #Initialise MARK to show all pixels as unvisited
    MARK = np.array([[0]*IMG.shape[1]]*IMG.shape[0])

    #Create Q, an empty queue-like ndarray
    Q = np.empty((0, 3))
    Q_indices = [] #not in Algorithm 1, contains the x and y coordinates of each pixel in Q
    
    #Iterate over each pixel in the image, when a pavement image is found its connected component should be traversed.
    for x in range(IMG.shape[0]):
        for y in range(IMG.shape[1]):

            if IMG[x][y][0] > upper_threshold and MARK[x][y] == 0: #if this pixel is part of the pavement and it hasn't been visited
                MARK[x][y] = 1 #mark this pixel as visited
                Q = np.append(Q, [IMG[x][y]], axis = 0) 
                Q_indices.append((x, y)) #adjust the new array accordingly
                pixels_traversed = 0 #not in Algorithm 1, measures the length of the connected component

                while np.any(Q): #while Q is not empty
                    current_pixel = Q[0]
                    current_pixel_indices = Q_indices[0] #get the first pixel's indices from the new array accordingly

                    #Remove the first pixel from Q
                    Q = Q[1:] 
                    Q_indices = Q_indices[1:] #remove the indices from the new array accordingly
                    
                    #Find the neighbours of the current pixel
                    neighbour_indices = find_neighbours(current_pixel_indices, IMG.shape[0]-1, IMG.shape[1]-1)
                    pixels_traversed+=1 #add to the new variable, as each neighbour is 1 pixel away from the current pixel

                    for neighbour_xy in neighbour_indices:
                        #Check if this neighbour is a pavement pixel that hasn't already been visited
                        if IMG[neighbour_xy[0]][neighbour_xy[1]][0] > upper_threshold and MARK[neighbour_xy[0]][neighbour_xy[1]] == 0:
                            MARK[neighbour_xy[0]][neighbour_xy[1]] = 1 #mark the neighbour as visited
                            Q = np.append(Q, [IMG[neighbour_xy[0]][neighbour_xy[1]]], axis = 0)
                            Q_indices.append(neighbour_xy) #add the neighbour's indices into the new array accordingly

                #Not in Algorithm 1 - Add the traversed component to the dictionary
                component_count +=1
                connected_components[component_count] = pixels_traversed
                           
    #Save the components and their lengths into a text file
    output_file = open('./data/cc-output-2a.txt', 'w')
    for component in connected_components:
        output_file.writelines(f'Connected Component {component}, number of pixels = {connected_components[component]}\n')
    output_file.writelines(f'Total number of connected components = {len(connected_components)}')
    output_file.close()

    result = 'The connected component lengths have been successfully saved to "cc-output-2a.txt".'        
    return result, MARK

def detect_connected_components_sorted(MARK):
    """Sorts the connected components from detect_connected_components() into descending order and saves the largest two into a new image
    
    Paramaters:
    MARK - Contains the array MARK returned from detect_connected_components(), whic records the pavement pixels that have been visited
    
    Return values:
    result - Confirmation that a new text file containing the connected components in decreasing order and a new image showing the largest two connected components have been saved
    """
    if MARK != []: #If the user has not yet run detect_connected_components(), yet the file './data/cc-output-2a.txt' already exists, MARK will be an empty array and this function should not be used
    
        #Open the file containing the connected components
        connected_components_filename = './data/cc-output-2a.txt'
        connected_components_file = open(connected_components_filename)
        connected_components_array = connected_components_file.readlines()
        connected_components_file.close()
        connected_components_array = connected_components_array[:-1] #don't include the line specifying the total number of components
  
        #Sort the components into descending order
        connected_components_array = bubble_sort(connected_components_array)

        #Save the sorted array into a new file
        output_file = open('./data/cc-output-2b.txt', 'w')
        output_file.writelines(connected_components_array)
        output_file.writelines(f'Total number of connected components = {len(connected_components_array)}')
        output_file.close()
        
        #Find the two largest components in MARK by traversing it in a similar way to in detect_connected_components()
        array_per_component = np.array([[0]*MARK.shape[1]]*MARK.shape[0]) #An array like MARK, which will contain each individual component in turn
        top_two_components = np.array([[0]*MARK.shape[1]]*MARK.shape[0]) #An array like MARK, which will contain the top two components
        Q_indices = []
        for x in range(MARK.shape[0]):
            for y in range(MARK.shape[1]):
                if MARK[x][y] == 1: #if the pixel is part of a connected component
                    MARK[x][y] = 0 #otherwise the algorithm will keep looping between pixels
                    array_per_component[x][y] = 1
                    Q_indices.append((x, y))
                    component_size = 0 #contains the size of this component
                    while np.any(Q_indices): 
                        current_pixel_indices = Q_indices[0]
                        Q_indices = Q_indices[1:]
                        neighbour_indices = find_neighbours(current_pixel_indices, MARK.shape[0]-1, MARK.shape[1]-1)
                        component_size +=1
                        for neighbour_xy in neighbour_indices:
                            if  MARK[neighbour_xy[0]][neighbour_xy[1]] == 1:
                                MARK[neighbour_xy[0]][neighbour_xy[1]] = 0
                                array_per_component[neighbour_xy[0]][neighbour_xy[1]] = 1
                                Q_indices.append(neighbour_xy)
                    else:

                        #Mark these pixels as 1 if they compose either the largest or second-largest component
                        largest_component = int(connected_components_array[0].strip().split('= ')[1])
                        second_largest_component = int(connected_components_array[1].strip().split('= ')[1])
                        if component_size == largest_component or component_size == second_largest_component:

                            #Copy these pixels into top_two_components
                            for x in range(MARK.shape[0]):
                                for y in range(MARK.shape[1]):
                                    if array_per_component[x][y] == 1:
                                        top_two_components[x][y] = 1
                        array_per_component = array_per_component = np.array([[0]*MARK.shape[1]]*MARK.shape[0]) #reset to deal with the next component

        #Construct a new array with the pixel colour values corresponding with top_two_components
        output_array = np.zeros((MARK.shape[0], MARK.shape[1], 4)) #initialise the array to contain zeros
        for x in range(MARK.shape[0]):
            for y in range(MARK.shape[1]):
                if top_two_components[x][y] == 1:
                    output_array[x][y] = [255, 255, 255, 256]
                else:
                    output_array[x][y] = [0, 0, 0, 256]
        
        #Save the array as an image
        output_array= np.multiply(output_array, 1/256).astype(float)
        mat_plot.imsave('./data/cc-top-2.jpg', output_array)

        result = 'The connected components have been sorted into decreasing order of size and saved to "cc-output-2b.txt", and an image containing the top two components has been saved as "cc-top-2.jpg".'
    
    else:
        result = 'You should use the option "Detect connected components" before selecting this option.'

    return result