import time
import pandas as pd
import numpy as np
import calendar as cl

#Import data sources
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Function to get input for filters on CITY, MONTH & DAY
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_list = ["chicago", "new york city", "washington"]
    month_list = ["all", "january", "february", "march", "april", "may", "june"]
    day_list = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    print('-'*40)
    print('Hello! Bicycle-sharing systems allow users to rent bicycles on a short-term basis for a price. \nLet\'s explore some US bikeshare data for three select cities!')
    # Get user input for city in city_list. While loop used to handle invalid inputs
    while True:
        city = input("\nWhich city's data would you like to explore? \nSelect Chicago, New York City, or Washington.\n")
        city = city.lower() #converts input to lowercase
        if city in city_list:
            print("\n", city.title(), "Selected") #displays seleceted choice
            break;
        else:
            print("\nOpps, I didn't catch that. Please double check your spelling.")  #displays error and reasks user for input

    # Get user input for months in month_list. While loop used to handle invalid inputs.
    while True:
        month = input("\nWhich month's data would you like to explore? \nSelect from the choices below: \n\nAll \nJanuary \nFebruary \nMarch \nApril \nMay \nJune \n")
        month = month.lower() #converts input to lowercase
        if month in month_list:
            print("\n", month.title(), "Selected") #displays seleceted choice
            break;
        else:
            print("Opps, I didn't catch that. Please double check your spelling.") #displays error and reasks user for input


    # Get user input for months in day_list. While loop used to handle invalid inputs.
    while True:
        day = input("\nWhich day would you like to explore? \nSelect from the choices below: \n\nAll \nMonday \nTuesday \nWednesday \nThursday \nFriday \nSaturday \nSunday \n")
        day = day.lower() #converts input to lowercase
        if day in day_list:
            print("\n", day.title(), "Selected") #displays seleceted choice
            break;
        else:
            print("Opps, I didn't catch that. Please double check your spelling.")  #displays error and reasks user for input

    print('-'*40)
    return city, month, day #collect input values

#Function to load dataframe and apply input filters from above
def load_data(city, month, day): #load selected input values
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

#Function to determine stats related to frequently used times
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Determine the most common month
    most_common_month = df['month'].mode()[0]


    # Determine the most common day of week
    most_common_dow = df['day_of_week'].mode()[0]

    # Determine the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    most_common_hour = df['hour'].mode()[0]

    #Display Travel Time Information
    print("Most Frequent Month:", cl.month_name[most_common_month], "\nMost Frequent Day:", most_common_dow, "\nMost Frequent Hour:", most_common_hour)

    #Display processing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to determine stats for most popular stations and routes
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Determine most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]

    # Determine most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]

    # Determine most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'].str.cat(df['End Station'],sep=" to ")
    most_common_route = df['Route'].mode()[0]

    #Display Station & Route Information
    print('Most Frequently Used Start Station:', most_common_start_station, '\nMost Frequently Used End Station:', most_common_end_station, '\nMost Frequently used Route:', most_common_route)

    #Display processing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function to calculate stats for Trip Duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time
    total_travel_time = round((df['Trip Duration'].sum()) / 60, 1)

    # Calculate mean travel time
    average_travel_time = round((df['Trip Duration'].mean(axis=0)) / 60, 1)

    #Display Trip Duration Information
    print('Total Travel Time:', total_travel_time, 'Minutes \nAverage Trip Duration:', average_travel_time, 'Minutes')

    #Display processing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function for determining user stats and demographics for cities with demographic data
def user_stats_with_demo(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Replace Null values in Gender with Unknown
    df["Gender"].fillna("Unknown", inplace = True)

    # Determine counts of user types
    user_types = df['User Type'].value_counts()

    # Determine counts of gender - replace null values with unknown
    user_gender = df['Gender'].value_counts()

    # Determine earliest, most recent, and most common year of birth
    oldest_birth_year = int(df['Birth Year'].min()) #earliest birth year
    youngest_birth_year = int(df['Birth Year'].max()) #most recent birth year
    most_common_birth_year = int(df['Birth Year'].mode()[0]) #most common birth year

    #Display User Information & Demographics where available
    print('Users by Type\n', user_types, '\n\nUsers Genders:\n',user_gender, '\n\nOldest Birth Year:', oldest_birth_year, '\nYoungest Birth Year:', youngest_birth_year, '\nMost Frequent Birth Year:', most_common_birth_year)

    #Display processing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Function for determining user stats and demographics for cities without demographic data
def user_stats_no_demo(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Determine counts of user types
    user_types = df['User Type'].value_counts()


    #Display User Information & Demographics where available
    print('Users by Type\n', user_types, '\n\nUser Genders: No Gender Information Available for this City.', '\nUser Birth Year: No Birth Year Information Available for this City.')

    #Display processing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    #Function to Prompt the user if they want to see 5 lines of raw data. Continues to and displays until the user says 'no'.
def individual_data(df):
    start_row = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or any other key to continue.\n')
    view_data = view_data.lower() #converts input to lowercase
    while view_data == 'yes':
            print(df.iloc[start_row : start_row + 5])
            start_row += 5
            view_data = input('Would you like to see 5 more rows of data? yes or any other key to continue.\n').lower()


    #Main function that call all the other functions, applies the filters and restarts the program
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df) #display time stats
        station_stats(df) #display station stats
        trip_duration_stats(df) #display trip duration stats
        if city == 'washington': #displays different user stats for cities with demographic data inluded
            user_stats_no_demo(df)
        else:
            user_stats_with_demo(df)
        individual_data(df) #displays individual data 5 rows at a time until users stops

        restart = input('\nWould you like to restart? Enter yes or any other key to continue.\n') #restarts program
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
