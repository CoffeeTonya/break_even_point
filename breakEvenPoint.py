import datetime
from glob import glob
from altair.vegalite.v4.schema.core import DataFormat
import numpy as np
import pandas as pd
import streamlit as st

# sidebar \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

item_code = st.sidebar.text_input('商品コード')
item_name = st.sidebar.text_input('商品名')
item_cost = st.sidebar.number_input('税抜原価', 0, step=1)
item_price = st.sidebar.number_input('税込売価', 0, step=1)
tax = st.sidebar.selectbox(
    '税率区分',
    ('8%', '10%'))
if tax == '8%':
    tax_ = 1.08
else:
    tax_ = 1.10
valiable_cost = st.sidebar.number_input('変動費', 0, step=1)
purchases = st.sidebar.number_input('仕入数', 0, step=1)
case = st.sidebar.number_input('入数', 0, step=1)
st.sidebar.markdown(rf'''
<br>
''', unsafe_allow_html=True)
shipping = st.sidebar.checkbox('送料無料')

if shipping == True:
    shipping = '無料'
    shipping_cost = 550
else:
    shipping = '別'
    shipping_cost = 0

# body \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# title
st.title('損益計算ツール')
st.markdown(rf'''
<br>
''', unsafe_allow_html=True)
if item_code == '':
    st.write('サイドバーの入力項目を入力してください')

st.markdown(rf'''
<br>
''', unsafe_allow_html=True)

# item
st.write('商品情報')

st.markdown(rf'''
    <table>
        <tr>
            <th>商品CD</th><th>品名</th><th>原価</th><th>売価</th><th>送料</th><th>税率</th>
        </tr>
        <tr>
            <td>{item_code}</td><td>{item_name}</td><td>{"{:,}".format(item_cost)}</td><td>{"{:,}".format(item_price)}</td><td>{shipping}</td><td>{tax}</td>
        </tr>
    </table>
    ''', unsafe_allow_html=True)

st.markdown(rf'''
<br>
''', unsafe_allow_html=True)

# pl_
st.write('損益分岐表')

index1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

column1 = []
column2 = []
column3 = []
column4 = []

for row in index1:
    number_of_sales = row * case
    number_of_cost = round((item_cost * purchases) + (valiable_cost * number_of_sales) + (shipping_cost * number_of_sales))
    amount_of_sales = round(number_of_sales * (item_price / tax_))
    plofit = round(amount_of_sales - number_of_cost)
    column1.append("{:,}".format(number_of_sales))
    column2.append("{:,}".format(number_of_cost))
    column3.append("{:,}".format(amount_of_sales))
    column4.append("{:,}".format(plofit))

dict1={'売上数': column1, '仕入金額': column2, '売上金額': column3, '損益': column4}

st.table(pd.DataFrame(data=dict1))
