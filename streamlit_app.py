# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

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

    # st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) 
            values (\'""" + ingredients_string + "\', \'"+ name_on_order + """')"""
    
    # st.write(my_insert_stmt)

    time_to_insert = st.button('submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(f"Your Smoothie is ordered!, {name_on_order}", icon="✅")
