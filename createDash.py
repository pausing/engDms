from dash import Dash,html,dcc,Input,Output
import streamlit as st
import date
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Super',page_icon=':bar_chart:',layout='wide')
st.title(' :bar_chart: SampleSuperStore EDA')
st.markdown('<style>div.block-container{padding-top:1000rem;}<?style>',unsafe_allow_html=True)