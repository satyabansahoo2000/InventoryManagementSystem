from deta import Deta
import streamlit as st

def init_connection():
    deta = Deta(st.secrets.deta.key)
    return deta

def suppliers():
    deta = init_connection()
    return deta.Base("Suppliers")

def categories():
    deta = init_connection()
    return deta.Base("Categories")

def products():
    deta = init_connection()
    return deta.Base("Products")