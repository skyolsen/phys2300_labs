'''
Assignment to learn how to interpolate data1
'''
import sys
from datetime import datetime as dt
import matplotlib.pylab as plt
import numpy as np

# "We need a code that will read in temperature time series, 
# read  in a GPS time series, and use an interpolation algorithm to produce a plot of temperature vs. altitude."

# Atmospheric data
## Note the first file contains three columns of temperature data. We will be using the first temperature senser column 
## Here we care about columns 2 (Time) and 4 (Ch1:Deg F)

# GPS data (GPSData.txtPreview the document)- 
## The transmission log file from the in-flight telemetry data. 
## Here the time is spread across columns 1, 2, 3 (GPS HOURS, MIN, SEC) also column 7 (Altitude) 

def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    times = []             # list to hold wx times
    temperatures = []      # list to hold wx temperartures
 
    # Open file and skip first row. 
    # Split each row by comma seperator.
    # Capture the time and temperature of wx data and append to lists 
    with open(wx_file, mode = 'r') as file: 
        file.readline() 
        for line in file: 
            line_words = line.split(",") 
            times.append(line_words[1]) 
            temperatures.append(float(line_words[3])) 
        harbor_data['wx_temps'] = temperatures # add temperature list to dictionary

    # Convert string time to float hours for easier plotting
    init_time = times[0]              # take first time which will be your time zero
    harbor_data['wx_times'] = []     # list to hold the data
    for h_time in times:
        delta_t = dt.strptime(h_time,'%H:%M:%S') - dt.strptime(init_time,'%H:%M:%S')  # get delta time
        harbor_data['wx_times'].append(float(delta_t.total_seconds()/3600))           # convert to hours
    
    
def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    times = []             # list of dates data
    alt = []      # list of temperarture data
 
    # Open file and skip first two rows. 
    # Split each row by space seperator.
    # Capture hour, minute, and seconds and append to time string in format HH:MM:SS
    # Append formatted times to times list
    # Capture altitude, cast to float type, and append to list 
    with open(gps_file, mode = 'r') as file:
        file.readline() # extract first row to skip
        file.readline() # extract second row to skip
        for line in file:
            line_words = line.split()
            time = line_words[0]+":"+line_words[1]+":"+line_words[2]
            times.append(time)
            alt.append(float(line_words[6]))
        harbor_data['gps_alt'] = alt
        
        # Convert string time to float hours for easier plotting
        init_time = times[0]              # take first time which will be your time zero
        harbor_data['gps_times'] = []     # list to hold the data
        for h_time in times:
            delta_t = dt.strptime(h_time,'%H:%M:%S') - dt.strptime(init_time,'%H:%M:%S')  # get delta time
            harbor_data['gps_times'].append(float(delta_t.total_seconds()/3600))           # convert to hours
    
   



def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    # Lists to hold ascention and descention data
    wx_ascalt = []
    wx_asctemp = []
    wx_desalt = []
    wx_destemp = []

    # Variables to hold max altitude and max GPS time
    max_alt = max(harbor_data["gps_alt"])
    max_gpstime = harbor_data["gps_times"][-1]
    
    # Variables to hold Beginning and Ending altitueds in a specified range
    start_alt = harbor_data["gps_alt"][0]
    last_alt = harbor_data["gps_alt"][1]

    # List to hold interpolated altitudes (estimated altitudes between recorded altitudes).
    introp_alt = []

    
    i = 0 # wx temperature iterator
    j = 0 # GPS altitude and time iterator
    count = 0 # wx range count
    sizeOfList = len(harbor_data["wx_times"]) # Number of wx temperatures

    while i <= sizeOfList: # Loop for every measured WX time
        if harbor_data["wx_times"][i] <= harbor_data["gps_times"][j]: # Count how many wx are taken inbetween GPS times
            count+=1
        else: # When wx time is equal to gps time (actually when the time finally exceeps the current GPS time)
            introp_range = list(np.linspace(start_alt,last_alt,count, endpoint=False)) # Create an estimate (range) of altitudes for temperatures recorded between GPS measurements
            introp_alt.extend(introp_range)# Append the range list to an interpolated data list
            start_alt = last_alt # Set the starting GPS altitude to be used in next range
            count=1 # Reset the count (set to 1 so we don't skip the exceeded wx time)               
            if harbor_data["gps_times"][j] >= max_gpstime: # if the GPS time at iter j is our last GPS time, break from loop
                introp_alt.append(last_alt) #append the last GPS altitude
                break
            j+=1 # increment GPS iterator 
            last_alt = harbor_data["gps_alt"][j] # set the ending GPS altitude to be used in next range
        i+=1 # increment wx temp iterator


    sizeOfList = len(introp_alt) 
    flag = False
    i = 0
    
    # Now that we have an altitude for every wx temperatures, make an ascention and descention altitude and time list
    while i < sizeOfList:
        if introp_alt[i] == max_alt: # When max altitude, set flag to start recording descention. Append last Ascention record
            flag = True
            wx_ascalt.append(introp_alt[i])
            wx_asctemp.append(harbor_data["wx_temps"][i])
        if flag: # if flag is set, switch to descention list
            wx_desalt.append(introp_alt[i])
            wx_destemp.append(harbor_data["wx_temps"][i])
        else: # if flag not set, add to ascention list
            wx_ascalt.append(introp_alt[i])
            wx_asctemp.append(harbor_data["wx_temps"][i])
        i+=1

    # add lists to harbor data dictionary
    harbor_data["alt_up"] = wx_ascalt
    harbor_data["temp_up"] = wx_asctemp 
    harbor_data["alt_dn"]  = wx_desalt
    harbor_data["temp_dn"] = wx_destemp

# plot the ascention and descention graphs
def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    pass
    plt.figure()
    # plt.subplot(2, 1, 1)                # select first subplot
    # plt.title("Harbor Flight Data")
    # plt.plot(harbor_data['wx_times'], harbor_data['wx_temps'])      
    # plt.ylabel("Temperature, F")
    # plt.xlabel("Elapsed hours")
    # plt.ylim([-60, 80])
    # plt.xlim([0, 2.5])

    # plt.subplot(2, 1, 2)                # select second subplot
    # plt.plot(harbor_data['gps_times'], harbor_data['gps_alt'])  
    # plt.ylabel("Altitude Ft")
    # plt.xlabel("Elapsed hours")
    # plt.xlim([0, 2.5])
    # plt.ylim([0, 100000])

    # Plot = Row, Col, selected sublot
    plt.subplot(1, 2, 1)                # select first subplot
    plt.title("Harbor Ascent Flight Data")
    plt.plot(harbor_data['temp_up'], harbor_data['alt_up'])      
    plt.ylabel("Altidude, Ft")
    plt.xlabel("Temperature, F")
    plt.ylim([0, 100000])
    plt.xlim([-50, 100])

    plt.subplot(1, 2, 2)                # select fourth subplot
    plt.title("Harbor Ascent Flight Data")
    plt.plot(harbor_data['temp_dn'], harbor_data['alt_dn'])  
    plt.xlabel("Temperature, F")
    #plt.xlabel("Elapsed hours")
    plt.ylim([0, 100000])
    plt.xlim([-60, 120])


    plt.show()      # display plot


def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}
    wx_file = sys.argv[1]                   # first program input param
    gps_file = sys.argv[2]                  # second program input param

    read_wx_data(wx_file, harbor_data)      # collect weather data
    read_gps_data(gps_file, harbor_data)    # collect gps data
    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures


if __name__ == '__main__':
    main()
    exit(0)
