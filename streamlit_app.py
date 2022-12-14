import streamlit
import pandas
from urllib.error import URLError
streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  

streamlit.header("Fruityvice Fruit Advice!")
import requests
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please Select a Fruit to get Information")
  else:
    func=get_fruitvice_data(fruit_choice)
    streamlit.dataframe(func)
    streamlit.write('The user entered ', fruit_choice)
except URLError as e:
  streamlit.error()
#streamlit.stop()

import snowflake.connector
streamlit.header("The fruit load list contains:")
def get_fruit_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Select * from fruit_load_list")
    return my_cur.fetchall()
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_list()
  streamlit.dataframe(my_data_rows)
  
def insert_row(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ( '"+new_fruit+"')")
    return "Thanks for adding "+new_fruit
streamlit.header("Quickly add your Favourites: ")  
add_fruit=streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = insert_row(add_fruit)
  streamlit.text(my_data_row)

streamlit.stop()
fruit_choice2 = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding ', fruit_choice2)



