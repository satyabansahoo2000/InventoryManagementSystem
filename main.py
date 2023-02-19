import streamlit as st
import extra_streamlit_components as stx
import streamlit_pydantic as sp
import time
import pandas as pd

from models.models import User, Category, Supplier, Product
from database.database import suppliers, products

st.set_page_config(
    layout = "wide",
    page_icon=":ledger:",
    page_title="Inventory Management"
)

chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="🏘️ Home", description="Dashboard & Store Balance Sheet"),
    stx.TabBarItemData(id=2, title="Consumption / Outwards", description="Consumption of products"),
    stx.TabBarItemData(id=3, title="Purchases / Inwards", description="Purchases of products"),
    stx.TabBarItemData(id=4, title="Inventory", description="Inventory of products available"),
    stx.TabBarItemData(id=5, title="Category / Products", description="Categories of products"),
    stx.TabBarItemData(id=6, title="Suppliers", description="Suppliers of products")
], default=1, return_type=int)

def insert_supplier(db, data):
    return db.insert({
        "key": data.gstin,
        "Name": data.name,
        "Phone": data.phone,
        "Location": data.address.location,
        "District": data.address.district,
        "Pincode": data.address.pincode
    })

def fetch_all(db):
    res = db.fetch()
    return res.items

if chosen_id == 1:
    pass
elif chosen_id == 2:
    _, col2, _ = st.columns([1,2,1])
    col2.title("Consumption / Outwards")
elif chosen_id == 3:
    _, col2, _ = st.columns([1,2,1])
    col2.title("Purchases / Inwards")
elif chosen_id == 4:
    _, col2, col3 = st.columns([1,2,1])
    col2.title("Inventory")
    with col3.expander("Add Product"):
        data = sp.pydantic_form(key="add-product", model=Product, ignore_empty_values=True)#, clear_on_submit=True)
        if data:
            placeholder = st.empty()
            with placeholder:
                st.success(":tada: Product added successfully !!!")
                time.sleep(2)
            placeholder.empty()
elif chosen_id == 5:
    _, col2, col3 = st.columns([1,2,1])
    col2.title("Category & Product List")
    with col3.expander("Add Category"):
        data = sp.pydantic_form(key="add-category", model=Category, ignore_empty_values=True, clear_on_submit=True)
        if data:
            placeholder = st.empty()
            with placeholder:
                st.success(":tada: Category added successfully !!!")
                time.sleep(2)
            placeholder.empty()
elif chosen_id == 6:
    db = suppliers()
    _, col2, col3 = st.columns([1,2,1])
    col2.title("Suppliers List")
    col2.markdown("---")
    with col3.expander("Add Supplier"):
        data = sp.pydantic_form(key="add-supplier", model=Supplier, ignore_empty_values=True, clear_on_submit=True)
        if data:
            insert_supplier(db, data)
            placeholder = st.empty()
            with placeholder:
                st.success(":tada: Supplier added successfully !!!")
                time.sleep(2)
            placeholder.empty()
    data = fetch_all(db)
    if not data:
        col2.subheader("No Suppliers avaiable !!! Please add suppliers.")
    else:
        df = pd.DataFrame(fetch_all(db))
        col2.dataframe(df, use_container_width=True)