# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

# Convert Snowpark DF to Pandas DF
pd_df = my_dataframe.to_pandas()

name_on_order = st.text_input("Name on Smoothie: ")
st.write('The name on your Smoothie will be: ', name_on_order)

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections=5
    )

if ingredient_list:

    ingredients_string = ''

    for fruit in ingredient_list:
        ingredients_string += fruit + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        st.write(f"{fruit}, {search_on}")

        st.subheader(fruit + ' Nutrition Information')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)


    # st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) 
            values (\'""" + ingredients_string + "\', \'"+ name_on_order + """')"""
    
    # st.write(my_insert_stmt)

    time_to_insert = st.button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(f"Your Smoothie is ordered!, {name_on_order}", icon="✅")

