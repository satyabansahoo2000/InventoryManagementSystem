import streamlit as st
import extra_streamlit_components as stx
import streamlit_pydantic as sp
import time 
import pandas as pd
from datetime import date

from models.models import User, Category, Supplier
from database.database import suppliers, products, categories, purchases, consumptions

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

def insert_category(db, data):
    return db.insert({
        "key": data.category
    })

def insert_purchase(db, data):
    Key = {"key": str(len(fetch_all(db))+1)}
    data.update(Key)
    return db.insert(data)

def insert_product(db, data):
    return db.insert({
        "key": str(len(fetch_all(db))+1),
        "Category": data['category'],
        "Product Name": data['name'],
        "Product Description": data['desc'],
        "UOM": data['uom'],
        "Supplier": data['supplierName']
    })

def update_data(db, data: dict, key: str):
    return db.put(data, key)

def delete_data(db, key: str):
    return db.delete(key)

def fetch_all(db):
    res = db.fetch()
    return res.items

def fetch_one(db, key):
    res = db.get(key)
    return res

if chosen_id == 1:
    pass
# ----------------------------------------------------------------
# Consumption / Outwards
# ----------------------------------------------------------------
elif chosen_id == 2:
    _, col2, _ = st.columns([1,2,1])
    col2.title("Consumption / Outwards")
# ----------------------------------------------------------------
# Purchases / Inwards
# ----------------------------------------------------------------
elif chosen_id == 3:
    _, col2, col3 = st.columns([1,2,1])
    col2.title("Purchases / Inwards")
    col2.markdown("---")
    
    db = products()
    db2 = purchases()
    data = fetch_all(db)
    df = pd.DataFrame(data)

    def clear_form():
        st.session_state['date'] = date.today()
        st.session_state['units'] = 1
        st.session_state['rate'] = 0.00

    with col3.expander("Add a purchase"):
        date_ = st.date_input("Date", key='date')
        
        pCat = set(df['Category'])
        category = st.selectbox("Product Category", pCat)
        
        pName = df.loc[df['Category'] == category, "Product Name"]
        name = st.selectbox("Product Name", pName)
        
        uom = df.loc[(df['Category'] == category) & (df['Product Name'] == name), "UOM"].item()
        desc = df.loc[(df['Category'] == category) & (df['Product Name'] == name), "Product Description"].item()
        uom = st.text_input("Unit of Measurement (UOM)", value=uom)    
        desc = st.text_area("Product Description", max_chars=200, value=desc)
        
        units = st.number_input("Units purchases", min_value=1, key="units")
        rate = st.number_input("Rate", min_value=0.00, key="rate")
        total = st.number_input("Total Price", value=round(units*rate, 2), disabled=True, key="total")
        data = {
            "Date": date_.isoformat(),
            "Category": category,
            "Product Name": name,
            "UOM": uom,
            "Description": desc,
            "Units Purchased": units,
            "Rate": rate,
            "Total Price": total
        }
        submitted = st.button("Submit", key="button-key", type="primary")
        if submitted:
            insert_purchase(db2, data)
            placeholder = st.empty()
            with placeholder:
                st.success(":tada: Purchase added successfully !!!")
                time.sleep(2)
            placeholder.empty()

    with col3.expander("Update a purchase"):
        pass

    data2 = fetch_all(db2)
    df2 = pd.DataFrame(data2)
    if df2.empty:
        col2.warning(":warning: Purchases are not available !!!")
    else:
        df2 = df2[['Date', 'Category', 'Product Name', 'Description', 'UOM', 'Units Purchased', 'Rate', 'Total Price']]
        col2.dataframe(df2, use_container_width=True)
# ----------------------------------------------------------------
# Inventory
# ----------------------------------------------------------------
elif chosen_id == 4:
    _, col2, col3 = st.columns([1,2,1])
    col2.title("Inventory")
    col2.markdown("---")


elif chosen_id == 5:
    db = categories()
    _, col2, col3 = st.columns([1,2,1])
    col2.title("Products List")
    col2.markdown("---")

    data = fetch_all(db)
    res = [f['key'] for f in data]
    if not data:
        pass
    else:
        category_key = col2.selectbox("Category", res)
    
    with col3.expander("Add Category"):
        data = sp.pydantic_form(key="add-category", model=Category, ignore_empty_values=True, clear_on_submit=True)
        if data:
            insert_category(db, data)
            placeholder = st.empty()
            with placeholder:
                st.success(":tada: Category added successfully !!!")
                time.sleep(2)
            placeholder.empty()
    
    with col3.expander("Update Category"):
        key = st.text_input(label="", label_visibility="collapsed",placeholder="Enter the key of the Category")
        if key == "":
            st.error(":point_up_2: Please enter the key of the category")
        else:
            data = fetch_one(db,key=key)
            if data is None:
                st.error("key is not available. Please enter a valid key of the supplier.")
            with st.form(key="update-supplier", clear_on_submit=True):
                data["key"] = st.text_input(label="Name of the category", value=data["key"])
                submitted2 = st.form_submit_button("Update", type="primary")
            if submitted2:
                update_data(db, data, key=key)
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Category updated successfully !!!")
                    time.sleep(2)
                placeholder.empty()

    with col3.expander("Delete Category"):
        key = st.text_input(label="", label_visibility="collapsed",placeholder="Enter the key of the Category", key="delete-category-key")
        if key == "":
            st.error(":point_up_2: Please enter the key of the category")
        else:
            if key in res:
                delete_data(db, key)
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Category deleted successfully !!!")
                    time.sleep(2)
                placeholder.empty()
            else:
                st.error(":warning: Category not found !!!")
    
    col3.markdown("---")
    db1 = suppliers()
    data1 = fetch_all(db1)
    res1 = [f['Name'] for f in data1]
    res2 = [f['key'] for f in data1]

    db2 = products()

    with col3.expander("Add Product"):
        with st.form("add-product-form", clear_on_submit=True):
            category = st.selectbox("Product Category", res)
            name = st.text_input("Product Name")
            uom = st.text_input("Unit of Measurement (UOM)")
            desc = st.text_area("Product Description", max_chars=200)
            supplierName = st.selectbox("Supplier Name", res1)

            submitted = st.form_submit_button("Submit", type="primary")
            if submitted:
                data2 = {
                    "category": category,
                    "name": name,
                    "desc": desc,
                    "uom": uom,
                    "supplierName": supplierName
                }
                insert_product(db2, data2)
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Product Added successfully !!!")
                    time.sleep(2)
                placeholder.empty()

    with col3.expander("Update Product"):
        key = st.text_input(label="", label_visibility="collapsed",placeholder="Enter the key of the Category", key="update-product-key")
        if key == "":
            st.error(":point_up_2: Please enter the key of the product")
        else:
            data = fetch_one(db2, key=key)
            if data is None:
                st.error("key is not available. Please enter a valid key of the supplier.")
            else:
                with st.form(key="update-product", clear_on_submit=True):
                    data["Category"] = st.selectbox("Product Category", res, index=res.index(data["Category"]))
                    data["Product Name"] = st.text_input(label="Name of the Product", value=data["Product Name"])
                    data["Product Description"] = st.text_input(label="Description of Product", value=data["Product Description"])
                    data["UOM"] = st.text_input(label="Unit of measurement", value=data["UOM"])
                    data["Supplier"] = st.selectbox("Supplier Name", res1, index=res1.index(data["Supplier"]))
                    submitted2 = st.form_submit_button("Update", type="primary")
                if submitted2:
                    update_data(db2, data, key=key)
                    placeholder = st.empty()
                    with placeholder:
                        st.success(":tada: Category updated successfully !!!")
                        time.sleep(2)
                    placeholder.empty()

    with col3.expander("Delete Product"):
        key = st.text_input(label="", label_visibility="collapsed",placeholder="Enter the key of the Porduct", key="delete-product-key")
        if key == "":
            st.error(":point_up_2: Please enter the key of the product")
        else:
            if key in res2:
                delete_data(db2, key)
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Product deleted successfully !!!")
                    time.sleep(2)
                placeholder.empty()
            else:
                st.error(":warning: Product not found !!!")

    with col2:
        data = fetch_all(db2)
        if not data:
            st.error("No Products available !!! Please add products.")
        else:
            data = pd.DataFrame(data)
            data = data[data['Category'] == category_key]
            data = data[['key', 'Product Name', 'UOM', 'Product Description', 'Supplier']]
            if data.empty:
                st.error(f"Products in {category_key} category not found. Please add products to {category_key} category.")
            else:
                st.dataframe(data, use_container_width=True)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Suppliers
# ----------------------------------------------------------------
elif chosen_id == 6:
    db = suppliers()
    data = fetch_all(db)
    res = [f['key'] for f in data]
    
    _, col2, col3 = st.columns([1,2,1])
    col2.title("Suppliers List")
    col2.markdown("---")

    if not data:
        col2.subheader("No Suppliers available !!! Please add suppliers.")
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
        key = st.text_input(label="", label_visibility="collapsed",placeholder="Enter the key of the Supplier", key="update-supplier-key")
        if key == "":
            st.error(":point_up_2: Please enter the key of the supplier")
        else:
            data = fetch_one(db,key=key)
            if data is None:
                st.error("key is not available. Please enter a valid key of the supplier.")
            with st.form(key="update-supplier", clear_on_submit=True):
                data["Name"] = st.text_input(label="Name of the supplier", value=data["Name"])
                data["Phone Number"] = st.text_input(label="Phone number", value=data["Phone Number"])
                data["GSTIN"] = st.text_input(label="GSTIN number", value=data["GSTIN"])
                data["Location"] = st.text_input(label="Location", value=data["Location"])
                data["District"] = st.text_input(label="District", value=data["District"])
                data["Pincode"] = st.text_input(label="Pincode", value=data["Pincode"])
                submitted2 = st.form_submit_button("Update", type="primary")
            if submitted2:
                update_data(db, data, key=key)
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier updated successfully !!!")
                    time.sleep(2)
                placeholder.empty()

    with col3.expander("Delete Supplier"):
        key = st.text_input(label="", label_visibility="collapsed",placeholder="Enter the key of the Supplier", key="delete-supplier-key")
        if key == "":
            st.error(":point_up_2: Please enter the key of the supplier")
        else:
            if key in res:
                delete_data(db, key)
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier deleted successfully !!!")
                    time.sleep(2)
                placeholder.empty()
            else:
                st.error(":warning: Supplier not found !!!")
# ----------------------------------------------------------------