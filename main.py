import streamlit as st
import extra_streamlit_components as stx
import streamlit_pydantic as sp
import time

from models.models import User, Category, Supplier, Product

st.set_page_config(
    layout = "wide",
)

chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="🏘️ Home", description="Dashboard & Store Balance Sheet"),
    stx.TabBarItemData(id=2, title="Consumption / Outwards", description="Consumption of products"),
    stx.TabBarItemData(id=3, title="Purchases / Inwards", description="Purchases of products"),
    stx.TabBarItemData(id=4, title="Inventory", description="Inventory of products available"),
    stx.TabBarItemData(id=5, title="Category", description="Categories of different products"),
    stx.TabBarItemData(id=6, title="Suppliers", description="Suppliers of different products"),
    stx.TabBarItemData(id=7, title="Add / Update", description="Add and Update Suppliers and Categories of products")
], default=1, return_type=int)

if chosen_id == 1:
    pass
elif chosen_id == 2:
    pass
elif chosen_id == 3:
    pass
elif chosen_id == 4:
    pass
elif chosen_id == 5:
    pass
elif chosen_id == 6:
    pass
elif chosen_id == 7:
    _, col2, _ = st.columns([1,1.5,1])
    with col2:
        with st.expander("Add a supplier"):
            data = sp.pydantic_form(key="add-supplier-form", model=Supplier, ignore_empty_values=True, clear_on_submit=True)
            if data:
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier added successfully !!!")
                    time.sleep(1)
                placeholder.empty()

        with st.expander("Update a supplier"):
            data = sp.pydantic_form(key="update-supplier-form", model=Supplier, ignore_empty_values=True, clear_on_submit=True)
            if data:
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier added successfully !!!")
                    time.sleep(1)
                placeholder.empty()

        with st.expander("Add a category"):
            data = sp.pydantic_form(key="add-category-form", model=Category, ignore_empty_values=True, clear_on_submit=True)
            if data:
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier added successfully !!!")
                    time.sleep(1)
                placeholder.empty()

        with st.expander("Update a category"):
            data = sp.pydantic_form(key="update-category-form", model=Category, ignore_empty_values=True, clear_on_submit=True)
            if data:
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier added successfully !!!")
                    time.sleep(1)
                placeholder.empty()

        with st.expander("Add a product"):
            data = sp.pydantic_form(key="add-product-form", model=Product, ignore_empty_values=True, clear_on_submit=True)
            if data:
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier added successfully !!!")
                    time.sleep(1)
                placeholder.empty()

        with st.expander("Update a product"):
            data = sp.pydantic_form(key="update-product-form", model=Product, ignore_empty_values=True, clear_on_submit=True)
            if data:
                placeholder = st.empty()
                with placeholder:
                    st.success(":tada: Supplier added successfully !!!")
                    time.sleep(1)
                placeholder.empty()