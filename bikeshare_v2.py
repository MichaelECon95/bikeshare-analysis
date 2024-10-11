import time
import pandas as pd
import numpy as np
import plotly.express as px


# insert path if different than the script location
# Constants for city data files and valid months and days for filtering
CITY_DATA = {'chicago': '/chicago.csv', 
             'new york city': '/new_york_city.csv',
             'washington': '/chwashington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
CITIES = list(CITY_DATA.keys())


# Function to get user input with validation
def get_user_input(prompt, valid_choices):
    while True:
        choice = input(prompt).lower()
        if choice in valid_choices:
            return choice
        else:
            print("Sorry, I didn't catch that. Try again.")


# Function to get filters for city, month, and day
def get_filters():
    print('\nHello! Let\'s explore some US bikeshare data!')
    city = get_user_input("\nWhich city would you like to filter by? New York City, Chicago or Washington?\n", CITIES)
    month = get_user_input("\nWhich month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n", months)
    day = get_user_input("\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n", days_of_week)
    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
   	 	# use the index of the months list to get the corresponding int
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

    #display the most common month

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)


    #display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)


    #display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Function to calculate station-related statistics
def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Finding and displaying the most common start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station:', Start_Station)

    # Finding and displaying the most common end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nThe most commonly used end station:', End_Station)

    # Finding and displaying the most common combination of start and end stations
    most_common_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\nThe most commonly used combo of start station and end station is:', most_common_combo[0], " & ", most_common_combo[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time

    travel_time = sum(df['Trip Duration'])
    print('The total travel time is {}'.format(travel_time))


    #display mean travel time

    mean_time = df['Trip Duration'].mean()
    print('The mean travel time is {}'.format(mean_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Function to calculate user-related statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types

    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n', user_types)

    #Display counts of gender

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    #Display earliest, most recent, and most common year of birth

    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nThe earliest birth year is:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nThere is no data available.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\The recent birth year is:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Year:\nThere is no data available.")

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nThe most common birth year is:', Most_Common_Year)
    except KeyError:
      print("\nMost Common Year:\nThere is no data available.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to show raw data based on user's request
def show_raw_data(df):
    start_time = time.time()

    i = 0
    raw_data = input('Would you like to see raw data? Y or N?\n').lower()
    while True:
        if raw_data == 'y':
            # Asking for the number of rows to display
            num_rows = input('How many rows would you like to see? (Enter a number): ')
            num_rows = int(num_rows)
            print(df.iloc[i:i + num_rows, :])
            i += num_rows
            raw_data = input('Would you like to see more? Y or N:').lower()
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

# Function to plot most common start stations
def plot_start_stations(df):
    # Count occurrences of each start station
    station_counts = df['Start Station'].value_counts().reset_index()
    station_counts.columns = ['Start Station', 'Count']
    # Create and display a horizontal bar plot
    fig = px.bar(station_counts, x='Count', y='Start Station', orientation='h', title='Most Common Start Stations')
    fig.show()

# Function to plot most common end stations
def plot_end_stations(df):
    # Count occurrences of each end station
    station_counts = df['End Station'].value_counts().reset_index()
    station_counts.columns = ['End Station', 'Count']
    # Create and display a horizontal bar plot
    fig = px.bar(station_counts, x='Count', y='End Station', orientation='h', title='Most Common End Stations')
    fig.show()

# Function to plot distribution of trip durations
def plot_trip_duration_distribution(df):
    # Create and display a histogram
    fig = px.histogram(df, x='Trip Duration', nbins=50, title='Distribution of Trip Durations')
    fig.show()

# Function to plot breakdown of user types
def plot_user_types(df):
    # Count occurrences of each user type
    user_types = df['User Type'].value_counts().reset_index()
    user_types.columns = ['User Type', 'Count']
    # Create and display a pie chart
    fig = px.pie(user_types, values='Count', names='User Type', title='Breakdown of User Types')
    fig.show()

def main():
    while True:
        city, month, day = get_filters()  # Get user input for filters
        df = load_data(city, month, day)  # Load data based on filters

        # Display text-based statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        # Prompt and display visualizations
        if input('Would you like to see the most common start stations? (Y/N): ').lower() == 'y':
            plot_start_stations(df)
        if input('Would you like to see the most common end stations? (Y/N): ').lower() == 'y':
            plot_end_stations(df)
        if input('Would you like to see the distribution of trip durations? (Y/N): ').lower() == 'y':
            plot_trip_duration_distribution(df)
        if input('Would you like to see the breakdown of user types? (Y/N): ').lower() == 'y':
            plot_user_types(df)

        # Ask if user wants to restart
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break

# Entry point of the script
if __name__ == "__main__":
    main()
