# This script will prepare additional dataframes using the ones 
# directly availalbe in the project. It aims to improve the application 
# processing time by executing some calculations beforehand (mean calclulations, 
# merge dataframes, data cleaning and preparation,...). 
# This script should be executed one time during the setup of the app.

import pandas as pd
from best_recipes import mean_rating_recipes, detailled_ratings_recipes, explicit_nutriments


def main():
    RAW_interactions_df = pd.read_csv("data/RAW_interactions.csv")
    RAW_recipes_df = pd.read_csv("data/RAW_recipes.csv")

    mean_ratings_df = mean_rating_recipes(RAW_interactions_df)

    #detailled_ratings_df = detailled_ratings_recipes(RAW_interactions_df, mean_ratings_df)

    explicit_nutriments_df = explicit_nutriments(RAW_recipes_df)

    mean_ratings_df.to_csv("data/mean_ratings.csv", index=False)
    #detailled_ratings_df.to_csv("data/detailled_ratings.csv", index=False)
    explicit_nutriments_df["submitted"] = pd.to_datetime(explicit_nutriments_df["submitted"])
    print(explicit_nutriments_df["submitted"])
    explicit_nutriments_df.to_csv("data/recipes_explicit_nutriments.csv", index=False)

if __name__ == "__main__":
    main()