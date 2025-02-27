"""
Main module of the project
"""
from data_treatment import import_data, make_ranking, get_distribution
from plots import plot_ranking, plot_gender, plot_age, plot_country

def main():
    """
    Main function of the project
    """
    # get google sheets database
    sheet_name = 'top-5-animals'
    sheet_id = '1XLO-q3zrwgsAbITzBbIgICT9X61GZ8c4LX_ubsE2JCo'
    first_url = "https://docs.google.com/spreadsheets/d/"
    second_url = "/gviz/tq?tqx=out:csv&sheet="
    url = f"{first_url}{sheet_id}{second_url}{sheet_name}"

    # import data
    data = import_data(url)
    

    # filter dataframe
    filters = {"Gender": list(data.loc[:,"Gender"].unique()),
               "Country": list(data.loc[:, "Country"].unique()),
               "Age": list(data.loc[:, "Age"].unique())}

    # make dataframe
    ranking = make_ranking(data, custom_filter = None)
    gender_distribution = get_distribution(data, "Gender")
    country_distribution = get_distribution(data, "Country")
    age_distribution = get_distribution(data, "Age")

    # get first 15 animals
    ranking = ranking.iloc[0:15]

    # plots
    plot_ranking(ranking)
    plot_gender(gender_distribution)
    plot_country(country_distribution)
    plot_age(age_distribution)

if __name__ == "__main__":
    main()