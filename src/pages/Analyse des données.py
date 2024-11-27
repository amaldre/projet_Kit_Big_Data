import streamlit as st
import statsmodels.api as sm
from src.utils.dbapi import DBapi


st.title("Analyse des data")


def tracer_graphes():
    client_DB = DBapi()

    # nombre de recettes par années
    nb_recette_par_annee_df = client_DB.find_two_by("recipe_id", 'submitted')
    print(nb_recette_par_annee_df.head())
    nb_recette_par_annee_df = nb_recette_par_annee_df.groupby('recipe_id').agg(
        mean_rating=('rating', 'mean'),
        count=('rating', 'count')
    )
    nb_recette_par_annee_df['year'] = nb_recette_par_annee_df['submitted'].dt.year
    nb_recette_par_annee_df['month'] = nb_recette_par_annee_df['submitted'].dt.month
    nb_recette_par_annee_df['submitted_by_month']=nb_recette_par_annee_df['submitted'].dt.to_period('M').dt.to_timestamp()
    submissions_groupmonth = nb_recette_par_annee_df['submitted_by_month'].value_counts().sort_index()
    decomposition = sm.tsa.seasonal_decompose(submissions_groupmonth, model='additive', period=12)

    nb_recette_par_annee_df["trend"] = decomposition.trend
    nb_recette_par_annee_df["seasonal"] = decomposition.seasonal

    print(nb_recette_par_annee_df.head())


def main():
    st.markdown("")
    tracer_graphes()
    

if __name__ == "__main__":
    main()