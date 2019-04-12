import time
import pandas as pd
import numpy as np

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

    # Def function for user to input city
    def get_city():
        while True:
            city = input('For which city would you like to explore the data? You can choose between: \nChicago?\nNew York City?\nWashington?\n').lower()
            if city in (CITY_DATA.keys()):
                return city
            else:
                print(f'Sorry, your input: "{city.title()}" is not a valid city, please input "Chicago", "New York City", or "Washington".')

    # Get user to input city, and ask user to verify the chosen city
    while True:
        city = get_city()
        city_check = input(f'Okay, let\'s explore the data from {city.title()}!\nWould you like to continue?\nY/N: ').lower()
        while city_check not in ('y', 'n'):
            city_check = input(f'Sorry, "{city_check}" is not a valid answer, please input "Y" for "Yes" and "N" for "No".')
        if city_check == ('y'):
            break
        else:
            continue

        # Get user input for month (all, january, february, ... , june)
    while True:
        month = input(f'Do you want to investigate all months or one particular month? Please enter one of the following: \nAll \nJanuary\nFebruary\nMarch,\nApril,\nMay,\nJune\n').lower()
        if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print(f'Your choice is "{month.title()}", let\'s continue!')
            break
        else:
            print(f'Sorry, "{month}" is not a valid answer, please choose again\n')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
         day = input(f'Do you want to investigate all days of the week or a particular day? Please enter one of the following: \nAll \nMonday \nTuesday \nWednesday \nThursday \nFriday \nSaturday \nSunday\n').lower()
         if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print(f'Your choice is: "{day.title()}", let\'s continue!')
            break
         else:
            print(f'Your choice {day.title()} is not a valid answer, please choose again')

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

    #load data into DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day and start hour from the Start Time column to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour

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

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display most common month, day and hour
    popular_month = df['month'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]
    popular_hour = df['start_hour'].mode()[0]
    print('Most Popular Month:', popular_month)
    print('Most Popular Day:', popular_day)
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station is:', popular_start_station)
    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station is:', popular_end_station)

    # Display most frequent combination of start station and end station trip
    df['Com_Station'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    popular_comb_station = df['Com_Station'].mode()[0]
    print('Most popular combination of start and end station is:', popular_comb_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('The total travel time is:', df['Trip Duration'].sum())

    # Display mean travel time
    print('The mean travel time is:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Type and count of users:\n', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Type and count of gender:\n', df['Gender'].value_counts())
    else:
        print('Sorry, there is no data available for Gender in your database')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth:\n', df['Birth Year'].min())
        print('Most recent year of birth:\n', df['Birth Year'].max())
        print('Most common year of birth:\n', df['Birth Year'].mode()[0])
    else:
        print('Sorry, there is no data available for Birth Year in your database')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #ask if user wants to see the first 5 raw data lines of the chosen dataset
        raw_data = input('\nWould you like to see the first 5 rows of raw data?\nPlease enter yes or no\n').lower()
        if raw_data in ('yes', 'y'):
            i = 0
        while True:
            print(df.iloc[i:i+5])
            i += 5
            more_data = input('Would you like to see more data? Please enter yes or no:\n').lower()
            if more_data not in ('yes', 'y'):
                break
        # User interaction for requestion to restart
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
