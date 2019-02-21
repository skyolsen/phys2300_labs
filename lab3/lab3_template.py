'''
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Auxiliary Files: None

Special Instructions: None

--------------------------------------------------------------------------------
'''
import sys
import matplotlib.pylab as plt
import numpy as np

# Pseudocode:
#J 1) get the name of the data file from the user on the command line 
#J 2) open the data file
#J 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#J       from all the remaining lines:
#J       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into decimal years for plotting (this would make a great function!)
#       (need to pay attention to leap years here!)
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third column (date)
                        One list with the information from the fourth column (temperature)
    """
    wdates = []             # list of dates data
    wtemperatures = []      # list of temperarture data

    #TODO:
    try:
        with open(infile, mode = 'r') as file:
            file.readline() # to extract the first line so we can skip it
            for line in file:
                line_words = line.split() # split record with space seperator
                wdates.append(line_words[2])
                wtemperatures.append(float(line_words[3]))
    except:
        print('Error Parsing Data')
    return wdates, wtemperatures


def calc_mean_std_dev(wdates, wtemp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param wdates: dictionary with dates fields
    :param wtemp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """
    means = []
    std_dev = []

    #TODO:
    #list of lists to hold monthly temperatures
    monthDayTemp = [ [],[],[],[],[],[],[],[],[],[],[],[] ]

    # Get the month to determin index of list. Then append the temperature the the list of that index.
    try:
        i = 0
        sizeOfList = len(wdates) 
        while i < sizeOfList:
            j = 1
            while j < 13:
                if int(wdates[i][4:6]) == j: 
                    monthDayTemp[j-1].append(wtemp[i])
                    break
                j += 1
            i += 1

    #Calculate the temperature and std dev average
        for monthTemps in monthDayTemp:
            means.append(np.average(monthTemps))
            std_dev.append(np.std(monthTemps))

    except:
        print('Error with data when calculating Mean and StdDev')
        exit(0)

    return means, std_dev

 #TODO:
def calc_year_daytemps(wdates):
    """
    Cast years to int variable. Append to list
    :param years: List with year fields
    :return: Decimal Years 
    """
    years = []

    try:
        sizeOfList = len(wdates)
        i = 0
        while i < sizeOfList:
            years.append(int(wdates[i][0:4]))
            i += 1
    except:
        print('Error calculating decimal year')
    return years


def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per
    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")
    plt.ylim([-20, 100])
    plt.xlim([1970, 2015])


    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()      # display plot


def plot_data_task2(xxx):
    """
    Create plot for Task 2. Describe in here what you are plotting
    Also modify the function to take the params you think you will need
    to plot the requirements.
    :param: xxx??
    """
    pass


def main(infile):
    weather_data = infile

    # take data file as input parameter to file
    wdates, wtemperatures = parse_data(weather_data)

    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wdates, wtemperatures)

    # TODO: Make sure you have a list of:
    #       1) years, 2) temperature, 3) month_mean, 4) month_std
    wyear = calc_year_daytemps(wdates)
    plot_data_task1(wyear, wtemperatures, month_mean, month_std)

    # TODO: Create the data you need for this
    # plot_data_task2(xxx)



if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    
    try:
        infile = sys.argv[1]
    except:
        print('No File Passed')
        exit(0)
    
    #infile = sys.argv[1]
    main(infile)
    exit(0)
