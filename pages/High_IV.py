from openbb_terminal.sdk import openbb as obb
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="High IV Scanner",)
data = obb.stocks.options.screen.screener_output(preset='high_IV.ini')[0]
high_iv = data.iloc[:,1:10]
high_iv
