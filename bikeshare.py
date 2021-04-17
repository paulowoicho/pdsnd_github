import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = None
    while (city != 'chicago' and city != 'new york city' and city != 'washington'):
        city = input("What city do you want information for? ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("\n")
            print("Please type in either 'Chicago', 'New York City', or 'Washington'")
            print("\n")



    month = None
    while (month not in months):
        month = input("What month do you want an analysis for? ").lower()
        if month not in months:
            print("\n")
            print("Please input a month from January to June or type 'all' for all months")
            print("\n")



    day = None
    while (day not in days_of_week):
        day = input("What day of the week are you interested in? ").lower()
        if day not in days_of_week:
            print("\n")
            print("Type in a day from Monday to Sunday or 'all' for all days of the week")
            print("\n")
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
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.capitalize()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    month = df['month'].mode()[0]
    month = months[month]
    print("The most common month is: {}".format(month.capitalize()))



    day = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {}".format(day))


    df['Start Hour'] = df['Start Time'].dt.hour
    hour = df['Start Hour'].mode()[0]
    print("The most common start hour is: {}:00".format(hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    start_station = df['Start Station'].mode()[0]
    print("The most common start station is: {}".format(start_station))


    end_station = df['End Station'].mode()[0]
    print("The most common end station is: {}".format(end_station))


    grouped_df = df.groupby(['Start Station', 'End Station']).size().reset_index(name="Count")
    max_count = grouped_df['Count'].idxmax()
    start_station = grouped_df.iloc[max_count]['Start Station']
    end_station = grouped_df.iloc[max_count]['End Station']
    print("The most frequent combination of start and end station trip is from {} to {}".format(start_station, end_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time across all stations is: {} minutes".format(total_travel_time))



    average_travel_time = df['Trip Duration'].mean()
    print("The average travel time across all stations is: {} minutes".format(average_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    user_counts = pd.DataFrame(df['User Type'].value_counts().reset_index())
    print("Here are the counts of the different types of users: ")
    for i in range(len(user_counts)):
        print(user_counts.iloc[i]['index'], user_counts.iloc[i]['User Type'])
    
    print("-"*40)


    try:
        gender = pd.DataFrame(df['Gender'].value_counts().reset_index())
        print("Here are the counts of the different types of the different genders: ")
        for i in range(len(gender)):
            print(gender.iloc[i]['index'], gender.iloc[i]['Gender'])
        print("-"*40)
    except:
        pass #dataframe does not have a gender column
    

    try:
        print("The most recent year of birth is: {}".format(int(df['Birth Year'].max())))
        print("The earliest year of birth is: {}".format(int(df['Birth Year'].min())))
        print("The most common year of birth is: {}".format(int(df['Birth Year'].mode()[0])))
    except:
        pass #dataframe does not have a birth year column


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays 5 rows of raw data after prompting the user"""

    user_choice = input("Would you like to see 5 rows of raw data from your city of choice? Type 'yes' to accept or anything else to skip ").lower()
    start_index = 0

    while user_choice == "yes":
        print(df[start_index: start_index + 5])
        user_choice = input("Would you like to continue? Type 'yes' to accept or anything else to skip ").lower()
        start_index += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        user_choice = input("Would you like some time stats about your chosen city, month and day? Enter yes or anything else to skip. \n").lower()
        if user_choice == 'yes':
            time_stats(df)
        
        user_choice = input("Would you like some station stats about your chosen city, month and day? Enter 'yes' to accept or anything else to skip. \n").lower()
        if user_choice == 'yes':
            station_stats(df)
            print('\n')
        
        user_choice = input("Would you like some trip duration stats about your chosen city, month and day? Enter 'yes' to accept or anything else to skip. \n").lower()
        if user_choice == 'yes':
            trip_duration_stats(df)
            print('\n')
        
        user_choice = input("Would you like some user stats about your chosen city, month and day? Enter 'yes' to accept or anything else to skip. \n").lower()
        if user_choice == 'yes':
            user_stats(df)
            print('\n')
        
        display_raw_data(df)

        user_choice = input('\nWould you like to restart? Enter yes or anything else to skip. \n')
        if user_choice.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
