import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH_NAMES = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global city #declared global as it will be used in user_stats()
    city = "none"
    month = "none"
    day = "none"
    print('Hello friends! Let\'s explore the US bikeshare data')
    
    while city not in CITY_DATA:
        city = input("Enter the city as chicago or new york city or washington: ")
        city = city.lower()
    
    while month not in MONTH_NAMES:
        month = input("Enter the complete name of month to filter by (type 'all' to apply no month filter): ")
        month = month.lower()
        
    while day not in DAYS:
        day = input("Enter the complete day (type 'all' to apply no day filter): ")
        day = day.lower()
        
    print('-'*40)
    return city, month, day

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
    
    if city == 'chicago':
        df = pd.read_csv('chicago.csv')
    elif city == 'new york city':
        df = pd.read_csv('new_york_city.csv')
    else:
        df = pd.read_csv('washington.csv')
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month 
    
    # extract day of week from the Start Time column to create an day_of_week column
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        month = MONTH_NAMES.index(month)+1
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    # display some raw data to the user if the user wants to see
    raw_data_check = input('\nDo you want to see first five lines of raw data. Enter yes or no: ')
    i=5
    if raw_data_check.lower() == 'yes':
        while True:
            raw_data = df.head(i)
            print(raw_data)
            #increment counter for 5 more records
            i=i+5 
            more_data = input('\nDo you want to see five records more this time. Enter yes or no: ')
            if more_data.lower() != 'yes':
                break

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nNow we will see the most frequent times of travel...\n')
    
    # extract hour from the Start Time column to create a hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour of travel: ', popular_hour)
    
    popular_month = df['month'].mode()[0]
    # get the month name from MONTH_NAMES using index minus one
    popular_month = MONTH_NAMES[popular_month-1]
    print('Most popular month of travel: ', popular_month.title())
    
    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day of travel: ', popular_day)
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nNow we will see most popular stations and trip...\n')
    popular_start = df['Start Station'].mode()[0]
    print('Most popular start station: ', popular_start)
    
    popular_end = df['End Station'].mode()[0]
    print('Most popular end station: ', popular_end)
    
    # concatenate the Start Station and End Station and name the new column as start_end
    df['start_end'] = df['Start Station'] + "->" + df['End Station']
    popular_start_end = df['start_end'].mode()[0]
    print('Most popular start-end station combination: ', popular_start_end)
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nNow we will see some statistics related to trip duration...\n')
    total_travel_time = df['Trip Duration'].sum()
    #divide by 60 to convert seconds in raw data to minutes
    print('Total travel time in minutes: ', total_travel_time/60)
    
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time in minutes: ', mean_travel_time/60)
    print('-'*40)
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nNow we will see some user stats...\n')
    print('Below are the type of users and count of users under each type-\n', df.groupby(['User Type']).size())
    
    # gender and birth year information not present in washington.csv
    if city != 'washington':
        print('\nBelow are the number of users in each gender-\n', df.groupby(['Gender']).size())
        
        #convert type to int as it is float by default
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        popular_year = int(df['Birth Year'].mode()[0])
        
        print('\nEarliest year of birth: ', earliest_year)
        print('\nMost recent year of birth: ', recent_year)
        print('\nMost popular year of birth: ', popular_year)
       
    print('-'*40)
                                         
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nDo you want to see similar stats with different inputs? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            
if __name__ == "__main__":
    main()
