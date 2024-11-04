import pandas as pd


def mean_rating_recipes(interactions_df):
    # Calculate the mean rating and the number of reviews for each recipe
    # Input: RAW_interactions dataframe
    # Output: Dataframe with the columns
    # ["recipe_id","mean_rating","count_total"]
    mean_rating_df = interactions_df.groupby('recipe_id').agg(
        mean_rating=('rating', 'mean'),
        count=('rating', 'count')
    )
    sorted_mean_rating = mean_rating_df.sort_values(by="count",
                                                    ascending=False)\
        .rename(columns={"count": "count_total"}).reset_index()
    return sorted_mean_rating


def detailled_ratings_recipes(interactions_df, mean_rating_df):
    # Return the mean rating and the number of reviews for each recipe
    # alongside the number of vote for each rating
    # Inputs: - RAW_interactions dataframe
    #         - dataframe from mean_rating_recipes function
    # Output: Dataframe with the columns
    # ["recipe_id","mean_rating","count_total","rating","count by rating"]
    count_by_rating_df = interactions_df.groupby(by=["recipe_id", "rating"])\
        .size().reset_index(name="count_by_rating")
    detailled_ratings_df = pd.merge(mean_rating_df,
                                            count_by_rating_df,
                                            on="recipe_id",
                                            how="left")
    return detailled_ratings_df


def explicit_nutriments(recipes_df):
    recipes_df.sort_values(by="minutes",inplace=True,ascending=False)
    recipes_df = recipes_df[2:]
    recipes_df[['calories','total fat (%)','sugar (%)','sodium (%)','protein (%)','saturated fat (%)','carbohydrates (%)']] = recipes_df.nutrition.str.split(",",expand=True)
    recipes_df['calories'] = recipes_df['calories'].apply(lambda x: x.replace('[','')) 
    recipes_df['carbohydrates (%)']= recipes_df['carbohydrates (%)'].apply(lambda x: x.replace(']','')) 
    return recipes_df