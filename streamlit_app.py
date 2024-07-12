import streamlit as st
import os

key = os.getenv('API_KEY')
st.title("Alpha Scout, comparing bookmaker odds to find arbitrage opportunities.")
st.write(key)
