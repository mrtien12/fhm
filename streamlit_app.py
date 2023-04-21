import streamlit as st
import pandas as pd
import time
import fhm
st.markdown("# Customer app")
st.set_page_config(page_title='quanproject')
st.sidebar.markdown(
    """ Program to solve FHM problem*
"""
)


data_customer = st.file_uploader("Customer Data Input",type = ['csv'])
if data_customer is not None:
    df = pd.read_csv(data_customer)
    st.write(df.head(5))

    transactions = df.groupby('no').apply(lambda x: [(p,q) for p,q in zip(x['product'],x['quantity'])]).reset_index().values.tolist()
    st.write(transactions)
else:
    st.write("Please upload a customer data file.")

product_data = st.file_uploader("Product Data Input",type =['csv'])
if product_data is not None:
    df1 = pd.read_csv(product_data)
    st.write(df1.head(5))

    price = dict(zip(df1['product'],df1['price']))
    st.write(price)
else:
    st.write("Please upload a product data file.")

check = st.selectbox(
    "Select mode of threshold(Percent or not):",("True","False")
)
if check == 'True':
    mode = True
elif check == "False":
    mode = False

if mode :
    percent = st.slider("Percentage:",min_value = 0.0,max_value = 1.0,value = 0.1,step = 0.1)
    fhm1 = fhm.FHM(transactions,price,percent,minutil_pc=mode)
else :
    num = st.number_input("Number:")
    fhm1 = fhm.FHM(transactions,price,num,minutil_pc= mode)
start = time.perf_counter()
k = fhm1.run_FHM()
end = time.perf_counter()
st.write("Execution time :" + str(end-start))
st.write(k)
