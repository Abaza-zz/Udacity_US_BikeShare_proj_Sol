import time
import pandas as pd
import numpy as np
import os
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        try:
            city_selection = input('To view the available bikeshare data, type:\n Chicago\n New York City\n Washington\n  ').lower()
            # Terminate the loop once getting a right answer
            if city_selection in CITY_DATA.keys() :
                city=city_selection
                break 
        except KeyboardInterrupt:
            print('\nNO Input Taken!')
        else:
            print('Invalid City choice!!')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            time_filter =input('\n Would you like to filter {}\'s data by month, day, or not at all? type month or day or none: \n'.format(city.title())).lower()
            # Terminate the loop once getting a right answer
            if time_filter in ['month','day','none'] :
                
                if time_filter == 'none':
                    print('\n Filtering for {} for the 6 months period \n'.format(city.title()))
                    month='all'
                    day='all'
                elif time_filter == 'month':
                    while True:
                        try:
                            month_selection=input("Choose month from ['january', 'february', 'march', 'april', 'may', 'june'] & type it \n ").lower()
                            if month_selection in ['january', 'february', 'march', 'april', 'may', 'june'] :
                                month=month_selection
                                day='all'
                                break 
                        except KeyboardInterrupt:
                            print('\nNO Input Taken!')
                        else:
                            print('Invalid month choice!!')
                    
                elif time_filter == 'day':
                    
                    while True:
                        try:
                            day_selection=input("Choose month from Sunday to Saturday & type it \n ").title()
                            if day_selection in ['Monday', 'Tuesday','Wednesday','Thursday', 'Friday', 'Saturday','Sunday'] :
                                day=day_selection
                                month='all'
                                break 
                        except KeyboardInterrupt:
                            print('\nNO Input Taken!')
                        else:
                            print('Invalid day choice!!')
                            
                
                break 
        except KeyboardInterrupt:
            print('\nNO Input Taken!')
        else:
            print('Invalid choice!!')

    # get user input for day of week (all, monday, tuesday, ... sunday)


    print('-'*40)
    return city, month, day, time_filter


def load_data(city, month, day):
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
    df = pd.read_csv(os.path.join(sys.path[0],CITY_DATA[city.lower()]))
    # convert the Start Time column to datetime
    df['Start Time'] = pd.DatetimeIndex(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    #df['day_of_week'] = df['Start Time'].dt.dayofweek.map(dayOfWeek)
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
        
    # filter by day of week if applicable
    
    if day != 'all':
        # filter by day of week to create the new dataframe
        #df = df.loc[df['day_of_week'] == day.title()]
        df= df[df['day_of_week'] == day.title()]
     
    return df



def time_stats(df,time_filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if time_filter =='none' or time_filter =='day' :
        df['month'] = df['Start Time'].dt.month

        print("The Most Common Month is : {}\n".format((df['month']).mode()[0]))

    # display the most common day of week
    if time_filter =='none' or time_filter =='month' :
        dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
        df['weekday'] = df['Start Time'].dt.dayofweek.map(dayOfWeek)

        print("The Most Common Day is : {}\n".format((df['weekday']).mode()[0]))
        
    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print("The Most Common Hour is : {}\n".format((df['Hour']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df = df.rename(columns={'Start Station': 'SStation', 'End Station': 'EStation'})

    # display most commonly used start station
    start_station_count=df['SStation'].value_counts()

    most_common_start=start_station_count.index[0]
    print("most common Start Station is: {}\n".format(most_common_start))

    # display most commonly used end station

    end_station_count=df['EStation'].value_counts()

    most_common_end=end_station_count.index[0]
    print("most common End Station is: {}\n".format(most_common_end))

    # display most frequent combination of start station and end station trip
    df['trips'] = list(zip(df.SStation, df.EStation))

    trip_count=df['trips'].value_counts()

    most_common_trip=trip_count.index[0]
    
    print('The most common Trip(Start,End) is : {}\n'.format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration=round(df['Trip Duration'].sum(),2)
    seconds=total_trip_duration
    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60

    days = seconds // seconds_in_day
    hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
    minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) 
    print('Total Trip Duration is {} days, {} hours and {} mins'.format(days, hours, minutes))

    # display mean travel time
    avg_trip_duaration=round(df['Trip Duration'].mean()/60, 2)
    print('Avg Trip Duration is: {} min'.format(avg_trip_duaration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser Types:\n {}".format(df['User Type'].value_counts()))

    # Display counts of gender
    if city =='chicago' or city =='new york city' :
        
        print("\nUsers Genders:\n {}".format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if city =='chicago' or city =='new york city' :
        print("youngest User birth year:\n {}".format(df['Birth Year'].min()))
        print("Oldest User birth year:\n {}".format(df['Birth Year'].max()))
        print("Most common year of birth:\n {}".format(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city) :
    
        print('\n Raw data is available to check... \n')
        display_raw = input("May you want to have a look on the raw data? Type yes or no\n")
        try:
            while display_raw == 'yes':
                try:
                    for chunk in pd.read_csv(os.path.join(sys.path[0],CITY_DATA[city.lower()]), chunksize=5):
                        print(chunk)
                        display_raw =input("May you want to have a look on the raw data? Type yes or no\n")
                        if display_raw == 'no':
                            print('Thank You')
                            print('-'*40)
                            break
                        elif display_raw == 'yes':
                            continue
                        break
                    break
                except KeyboardInterrupt:
                    print('Thank you.')

        except KeyboardInterrupt:
            print('\nNO Input Taken!')
        


def main():
    while True:
        city, month, day,time_filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df,time_filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()