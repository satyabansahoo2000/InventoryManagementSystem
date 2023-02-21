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
        "key": str(len(fetch_all(db))+1),
        "GSTIN": data.gstin,
        "Name": data.name,
        "Phone Number": data.phone,
        "Location": data.address.location,
        "District": data.address.district,
        "Pincode": data.address.pincode
    })

def update_supplier(db, data: dict, key: str):
    return db.put(data, key)

def fetch_all(db):
    res = db.fetch()
    return res.items

def fetch_one(db, key):
    res = db.get(key)
    return res

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

# ----------------------------------------------------------------
# Suppliers
# ----------------------------------------------------------------
elif chosen_id == 6:
    db = suppliers()
    _, col2, col3 = st.columns([1,2,1])
    col2.title("Suppliers List")
    col2.markdown("---")

    data = fetch_all(db)
    if not data:
        col2.subheader("No Suppliers avaiable !!! Please add suppliers.")
    else:
        df = pd.DataFrame(fetch_all(db))
        df = df[['key', 'Name', 'Phone Number', 'GSTIN', 'Location', 'District', 'Pincode']]
        col2.dataframe(df, use_container_width=True)
    
    with col3.expander("Add Supplier"):
        data = sp.pydantic_form(key="add-supplier", model=Supplier, ignore_empty_values=True, clear_on_submit=True)
        if data:
            insert_supplier(db, data)
            placeholder = st.empty()
            with placeholder:
                st.success(":tada: Supplier added successfully !!!")
                time.sleep(2)
            placeholder.empty()
    
    with col3.expander("Update Supplier"):
        key = st.text_input(label="", label_visibility="collapsed",placeholder="Enter the key of the Supplier")
        if key == "":
            st.error(":point_up_2: Please enter the key of the supplier")
            st.stop()
        else:
            data = fetch_one(db,key=key)
            if data is None:
                st.error("key is not available. Please enter a valid key of the supplier.")
                st.stop()
            with st.form(key="update-supplier", clear_on_submit=True):
                data["Name"] = st.text_input(label="Name of the supplier", value=data["Name"])
                data["Phone Number"] = st.text_input(label="Phone number", value=data["Phone Number"])
                data["GSTIN"] = st.text_input(label="GSTIN number", value=data["GSTIN"])
                data["Location"] = st.text_input(label="Location", value=data["Location"])
                data["District"] = st.text_input(label="District", value=data["District"])
                data["Pincode"] = st.text_input(label="Pincode", value=data["Pincode"])
                submitted2 = st.form_submit_button("Update", type="primary")
            if submitted2:
                update_supplier(db, data, key=key)
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier updated successfully !!!")
                    time.sleep(2)
                placeholder.empty()
# ----------------------------------------------------------------