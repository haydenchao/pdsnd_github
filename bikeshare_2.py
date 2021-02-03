import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


MONTHS = ['january','february', 'march', 'april', 'may', 'june']

def month_name(num):
    m_name = ['january','february', 'march', 'april', 'may', 'june']
    return m_name[num - 1]

def print_error(value):
    #function to print error value to reduce repetitive code
    print("-- Your input is incorrect: [ {} ]. Please try again! --".format(value))

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Users are able to exit the program if 'exit' keyword is input

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('-'*40)
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        print()
        city = input("Would you like to see data for Chicago, New york city or Washington (or 'exit' if you wanna leave this program) \nPlease type the name in here: ").lower()
        if city in ['chicago','new york city', 'washington']:
            break
        elif city in ['exit']:
            return
        else:
            print_error(city)
            continue
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWould you like to filter by month? Between January, February, March, April, May or June?. Type \"all\" if no filter.\n').lower()
        if month in MONTHS: #Global variable contains list of months
            break
        elif month == 'all':
            break
        else:
            print_error(month)
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nFilter out which day? Please type your response as an integer (e.g 0 = Sunday ... 6 = Saturday). Type \"all\" if no filter.\n').lower()
        if day == 'all':
            break
        else:
            try:
                day = int(day)
                if day in list(range(7)):
                    break
            except:
                print_error(day)

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
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start time to datetime and create 2 new columns as month and day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = MONTHS.index(month) + 1 #using global variable MONTHS
        df = df[df['Month'] == month]

    if day != 'all':
        weekday = ['Sunday', 'Monday','Tuesday','Wednesday','Thursday', 'Friday','Saturday']
        df = df[df['Day_of_Week'] == weekday[day]]

    #pd.set_option('max_columns', None)
    #print(df.head(10))
    return df


def time_stats(df,month, day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (Dataframe) df - dataframe of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].value_counts()
    most_freq_m = tuple(common_month.items())
    monthNum, counts = most_freq_m[0][0], most_freq_m[0][1]
    print("1) Most popular month: {}, Count: {}, Filter: {}".format(month_name(monthNum).title(), counts , month))

    # display the most common day of week
    common_day = df['Day_of_Week'].value_counts()
    most_freq_d = tuple(common_day.items())
    # Convert the return from value_counts() into Tuple, then extract the first element index and value
    print("2) Most popular day: {}, Count: {}, Filter: {}".format(most_freq_d[0][0], most_freq_d[0][1], day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].value_counts()
    most_freq_h = tuple(common_hour.items())
    print("3) Most popular hour: {}, Count: {}".format(most_freq_h[0][0], most_freq_h[0][1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Popular Start Station: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Popular End Station: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("Popular combination of Start and End Station: ", (df['Start Station'] + " " + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print("Total Travel Time: {}".format(str(dt.timedelta(seconds=total_travel_time))))

    # display mean travel time
    print("Average Travel Time in sec: ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    No output display if column is not exist.

    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' not in df.columns:
        # Skip the calcuation on Gender if this column not exist
        print('Column User Type is not exist.')
        print('-'*40)
    else:
        # Display counts of user types
        print("Counts of each user type as below:")
        print(df['User Type'].value_counts())
        print()


    if 'Gender' not in df.columns:
        # Skip the calcuation on Gender if this column not exist
        print('Column Gender is not exist.')
        print('-'*40)

    else:
        # Display counts of gender
        print("Counts of each gender as below:")
        df['Gender'].fillna('Unknown', inplace=True)
        print(df['Gender'].value_counts().sort_index())

        # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print('\nDisplay earliest, most recent, and most common year of birth')
        print("-- The earliest birth year among all the users is year: {}".format(earliest))
        print("-- Most recent birth year among all the users is year: {}".format(most_recent))
        print("-- The most common year of birth is year: {}".format(most_common))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_more_data(df):
    """
    Display data 5 lines of raw data at a time, continue display when user type yes

    """
    df = df.drop(['Month', 'Day_of_Week', 'hour'], axis=1)
    sn = 0 #slice_num
    more_data = input("Would you like to see some raw data? Type \'yes\' to continue\n")
    while more_data.lower() == 'yes':
        df_slice = df.iloc[sn: sn + 5]
        df_dict = df_slice.to_dict('index')
        print(df_dict)
        for col, row in df_dict.items():
            print()
            for key in row:
                print("\'{}\': \'{}\' ".format(key, row[key]))

        sn += 5
        more_data = input("\nWould you like to see some raw data? Type \'yes\' to continue\n")


def main():
    while True:
        try:
            """Exit the program if the user input exit in the first place"""
            city, month, day = get_filters()
        except TypeError:
            print("\nExiting the program. See you next time.\n")
            return

        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_more_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
