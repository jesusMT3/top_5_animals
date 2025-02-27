"""
Module to store all the code that make the data treatment
for the input google sheets csv.
"""
import pandas as pd

def import_data(url: str):
    """
    Imports a csv from a url into a pandas dataframe.

    Args:
        url (str): Url to download the csv

    Returns:
        data (pd.DataFrame): Data converted into a pandas dataframe.
    """
    # read data
    data = pd.read_csv(url, delimiter = ",").dropna(axis=1, how='all')

    # data treatment
    last_five_cols = data.columns[-5:]
    data[last_five_cols] = data[last_five_cols].astype(str).apply(
        lambda x: x.str.lower().str.strip()
    )
    data[last_five_cols] = data[last_five_cols].apply(lambda x: x.str.lower().str.strip())
    data["Name"] = data["Name"].apply(lambda x: x.strip())

    return data

def make_ranking(data: pd.DataFrame, custom_filter: tuple = None):
    """
    Makes the ranking dataframe of the data. Each row will be given
    5 points for each top 1, 4 points for each top 2, and so on.

    Args:
        data (pd.DataFrame): Dataframe from google sheets csv.
        custom_filter (tuple): Contains the key-value for the filter.

    Returns:
        pd.DataFrame: The ranking in descending order.
    """

    # filter if there is one
    if custom_filter is not None:
        # unpack values
        column, parameter = custom_filter
        # get the rows where column equals parameter
        data = data[data[column] == parameter]

    last_five_cols = data.columns[-5:]
    all_animals = pd.concat([data[i] for i in last_five_cols])
    unique_animals = all_animals.unique()

    values_first = data["1st animal"].value_counts()
    values_second = data["2nd animal"].value_counts()
    values_third = data["3rd animal"].value_counts()
    values_fourth = data["4th animal"].value_counts()
    values_fifth = data["5th animal"].value_counts()

    ranking = pd.DataFrame(index = unique_animals)
    votes = all_animals.value_counts()
    ranking["votes"] = votes

    values = []
    for animal in unique_animals:
        value = 0
        if animal in values_first:
            value += 5 * values_first[animal]
        if animal in values_second:
            value += 4 * values_second[animal]
        if animal in values_third:
            value += 3 * values_third[animal]
        if animal in values_fourth:
            value += 2 * values_fourth[animal]
        if animal in values_fifth:
            value += 1 * values_fifth[animal]

        values.append(value)

    ranking["values"] = values
    ranking = ranking.sort_values(by = "values", ascending = False)

    return ranking


def get_distribution(data: pd.DataFrame, parameter: str):
    """
    Obtains the distribution of the values of the parameter
    which is a column of the dataframe.

    Args:
        data (pd.DataFrame): Data with columns
        parameter (str): Column to get the distribution

    Returns:
        pd.DataFrame: Parameter distribution
    """
    gender_data = data[parameter].value_counts()
    return gender_data
