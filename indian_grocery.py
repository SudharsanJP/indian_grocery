import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px

#)title
st.title(':orange[💮Indian groceries price in Sydney data🌳]')
st.error("area: DATA VISUALIZATION")

#) reading dataset
df = pd.read_csv(r"D:\Sudharsan\Guvi_Data science\DS101_Sudharsan\Mainboot camp\capstone project\indian_groceries_sydney\indian_store.csv")

#) checkbox with df
st.subheader("\n:green[1. dataset🌝]\n")
if (st.checkbox("original data")):
    #)showing original dataframe
    st.markdown("\n#### :red[1.1 original dataframe]\n")
    data = df.head(5)
    st.dataframe(data.style.applymap(lambda x: 'color:purple'))

#) to get only the string in the given list of elements
import re
quantity_list = df['Quantity'].tolist()
units_list = []

for string in quantity_list:
    pattern = r'[0-9]'
    new_string = re.sub(pattern, '', string)
    units_list.append(new_string)
#units_list

#) converting list into column
df['units'] = units_list
#df

#) to get only the string in the given list of elements
import re
quantity_list = df['Quantity'].tolist()
num_quantity_list1 = []
for string in quantity_list:
    pattern =  r'[a-z]'
    new_string = re.sub(pattern, '', string)
    num_quantity_list1.append(new_string)
#num_quantity_list1

num_quantity_list2 = []
for string in num_quantity_list1:
    pattern =  r'[A-Z]'
    new_string = re.sub(pattern, '', string)
    num_quantity_list2.append(new_string)
#num_quantity_list2

int_quantity_list = []

for num in num_quantity_list2:
    num = int (num)
    int_quantity_list.append(num)
#int_quantity_list

#) converting list into column
df['num_quantity'] = int_quantity_list
#df

#) to get only the string in the given list of elements
import re

#) removing $ symbol from price column
list_price = df['Product Price'].tolist() #) converting item_date column into list
price_string = map(str, list_price)
list_price_string = list(price_string)

new_price_list = []
for num in list_price:
       price = re.findall(r'\d+\.\d+', num)
       converted = float(price[0])
       new_price_list.append(converted)
#new_price_list

float_quantity_list = []

for num_price in new_price_list:
    num_price = float (num_price)
    float_quantity_list.append(num_price)
#float_quantity_list

#) converting list into column
df['price_usd'] = float_quantity_list
#df
#) dropping unncessary columns
df.drop(['Product Price','Quantity'],axis=1,inplace=True)

df1 = df[df['units'] == 'g']
#df1

df2 = df[df['units'] == 'kg']
#df2

df2['num_quantity'] = df2['num_quantity'].mul(1000)
#df2

#) dropping unncessary columns
df2.drop(['units'],axis=1,inplace=True)
#df2

#) dropping unncessary columns
df1.drop(['units'],axis=1,inplace=True)
#df1

#)concatenation of dataframes(1-2)
df = pd.concat([df1, df2], axis=0, ignore_index=True)
#df

#) to rename the columns
df.rename(columns={'Product Name':'product_name',
                   "num_quantity": "num_quantity_grams",
                   'Product Category':'product_category',
                   'Product Price (INR)':'price_inr'
                  }, inplace=True)

#) adding a column with price:gram ratio
df['inr_per_gram'] = df['price_inr']/df['num_quantity_grams']
#df
#) checkbox with df
if (st.checkbox("data post processing")):
    #)showing original dataframe
    st.markdown("#### :red[1.2 data post processing]")
    data = df.head(5)
    st.dataframe(data.style.applymap(lambda x: 'color:green'))
#df['product_category'].unique()

#) converting df to list
list_product_category =df['product_category'].tolist()
list_price_inr = df['price_inr'].tolist()
list_quantity_grams = df['num_quantity_grams'].tolist()

#) converting list to np
np_product_category = np.array(list_product_category)
np_price_inr = np.array(list_price_inr)
np_quantity_grams = np.array(list_quantity_grams)


#df['inr_per_gram']

#) lowest price
df_inr1 = df[df['price_inr'] < 75]

#) highest price
df_inr2 = df[df['price_inr'] > 3000]

#) biscuits
df_pc1 = df[df['product_category'] == 'Biscuits']

#) sweets
df_pc2 = df[(df['product_category'] == 'Sweets') & (df["price_inr"]>500)]

#)fruits and vegetables
df_pc3 = df[(df['product_category'] == 'Fruits & Vegetables') & (df["price_inr"]>500)]
st.subheader("\n:green[2. data analysis🌹]")
selectBox=st.selectbox("data analysis: ", ['scatterplot 1',
                                           'scatterplot 2',
                                           'scatterplot 3',
                                           'scatterplot 4',
                                           'scatterplot 5'])

if selectBox == 'scatterplot 1':
    st.markdown("\n#### :red[2.1 the product less than 35]\n")
    #)scatter plot
    fig = px.scatter(
    df_inr1,
    x='num_quantity_grams',
    y='price_inr',
    color="product_category",
    hover_name="product_name",
    log_x=True,
    size_max=60,
)
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig, theme=None, use_container_width=True)

elif selectBox == 'scatterplot 2':
    st.markdown("\n#### :violet[2.2 the product more than 6800]\n")
    #)scatter plot
    fig = px.scatter(
    df_inr2,
    x='num_quantity_grams',
    y='price_inr',
    color="product_category",
    hover_name="product_name",
    log_x=True,
    size_max=60,
)
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig, theme=None, use_container_width=True)

elif selectBox == 'scatterplot 3':
    st.markdown("\n#### :blue[2.3 Biscuits]\n")
    fig = px.scatter(
    df_pc1,
    x='num_quantity_grams',
    y='price_inr',
    color="product_name",
    #hover_name="product_name",
    log_x=True,
    size_max=60,
)
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig, theme=None, use_container_width=True)

elif selectBox == 'scatterplot 4':
    st.markdown("\n#### :violet[2.4 sweets]\n")
    fig = px.scatter(
    df_pc2,
    x='num_quantity_grams',
    y='price_inr',
    color="product_name",
    #hover_name="product_name",
    log_x=True,
    size_max=60,
)
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig, theme=None, use_container_width=True)

elif selectBox == 'scatterplot 5':
    st.markdown("\n#### :red[5. veg and fruits]\n")
    fig = px.scatter(
    df_pc3,
    x='num_quantity_grams',
    y='price_inr',
    color="product_name",
    #hover_name="product_name",
    log_x=True,
    size_max=60,
)
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig, theme=None, use_container_width=True)  

