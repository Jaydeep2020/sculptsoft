from itertools import product

import requests
import streamlit as st
import pandas as pd

from db.database import get_session
from services.inventory_manager import InventoryManager
from services.inventory import Inventory
from services.generic import Generic

from models.inventory_model import InventoryModel
from models.product_model import ProductModel
from models.enums import CategoryType

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Add Inventory",
        "View Inventories",
        "Add Product",
        "View Products",
        "Search Product",
        "Update Product Stock",
        "Delete Product From Inventory",
        "Transfer Stock",
        "Total Stock Across Inventories"
    ]
)

# ---------------------------------------------------
# ADD INVENTORY
# ---------------------------------------------------

if menu == "Add Inventory":
    st.header("Add Inventory")

    inventory_name = st.text_input("Inventory Name")
    location = st.text_input("Location")

    if st.button("Add Inventory"):

        payload = {
            "name": inventory_name,
            location: location
        }

        response = requests.post(
            f"{BASE_URL}/inventory-manager/add_inventory",
            json=payload
        )

        st.write(response.json())

# ---------------------------------------------------
# VIEW INVENTORIES
# ---------------------------------------------------

elif menu == "View Inventories":

    st.header("View Inventories")

    with get_session() as session:

        inventories = InventoryManager.view_inventories(session)

        data = []

        for inv in inventories:
            data.append({
                "ID": inv.id,
                "Name": inv.name,
                "Location": inv.location
            })

        st.dataframe(pd.DataFrame(data))


# ---------------------------------------------------
# ADD PRODUCT
# ---------------------------------------------------

# ---------------------------------------------------
# ADD PRODUCT
# ---------------------------------------------------

elif menu == "Add Product":

    st.header("Add Product")

    # Inventory Details
    inventory_name = st.text_input("Inventory Name")
    location = st.text_input("Location")

    # Product Details
    product_name = st.text_input("Product Name")

    category = st.selectbox(
        "Category",
        [c.value for c in CategoryType]
    )

    price = st.number_input(
        "Price",
        min_value=1.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1
    )

    # Optional Fields
    warranty = None
    expiry_date = None

    if category == CategoryType.ELECTRICAL.value:

        warranty = st.number_input(
            "Warranty Months",
            min_value=0
        )

    elif category == CategoryType.GROCERY.value:

        expiry_date = st.date_input(
            "Expiry Date"
        )

    # Add Product Button
    if st.button("Add Product"):

        try:

            with get_session() as session:

                # Check Inventory Exists
                inventory_id = Generic.get_inventory_id(
                    session,
                    inventory_name,
                    location
                )

                if inventory_id is None:
                    raise Exception(
                        f"Inventory '{inventory_name}' "
                        f"with location '{location}' does not exist"
                    )

                # Create Product Object
                product = ProductModel(
                    name=product_name,
                    category=category,
                    price=price,
                    warranty_month=warranty,
                    expiry_date=expiry_date
                )

                # Add Product To Inventory
                Inventory.add_product(
                    session,
                    product,
                    inventory_id,
                    quantity
                )

            st.success("Product added successfully")

        except Exception as e:
            st.error(str(e))

# ---------------------------------------------------
# VIEW PRODUCTS
# ---------------------------------------------------

elif menu == "View Products":

    st.header("View Products")

    inventory_name = st.text_input("Inventory Name")
    location = st.text_input("Location")

    if st.button("View Products"):
        try:
            with get_session() as session:

                inventory_id = Generic.get_inventory_id(session, inventory_name, location)

                products = Inventory.view_products(session, inventory_id)

                data = []

                for p in products:
                    data.append({
                        "Name": p.name,
                        "Category": p.category,
                        "Price": p.price,
                        "Quantity": p.quantity,
                        "Warranty": p.warranty_month,
                        "Expiry Date": p.expiry_date
                    })

                st.dataframe(pd.DataFrame(data))

        except Exception as e:
            st.error(str(e))

# ---------------------------------------------------
# SEARCH PRODUCT
# ---------------------------------------------------

elif menu == "Search Product":

    st.header("Search Product")

    inventory_name = st.text_input("Inventory Name")
    location = st.text_input("Location")

    product_name = st.text_input("Product Name")

    if st.button("Search"):

        try:
            with get_session() as session:

                inventory_id = Generic.get_inventory_id(session, inventory_name, location)

                product = Inventory.search_product(session, product_name, inventory_id)

                if product is None:
                    st.warning("Product not found in the specified inventory")
                else:
                    st.success(f"Product found: {product.name} | Category: {product.category} | Price: {product.price} | Quantity: {product.quantity}")

        except Exception as e:
            st.error(str(e))

# ---------------------------------------------------
# UPDATE PRODUCT STOCK
# ---------------------------------------------------

elif menu == "Update Product Stock":

    st.header("Update Product Stock")

    inventory_name = st.text_input("Inventory Name")
    location = st.text_input("Location")
    product_name = st.text_input("Product Name")
    quantity = st.number_input(
        "Add Quantity",
        min_value=-1000,
        step=1,
        value=0
    )

    if st.button("Update Stock"):

        try:
            with get_session() as session:
                inventory_id = Generic.get_inventory_id(session, inventory_name, location)
                Inventory.update_product(session=session, product_name=product_name, inventory_id=inventory_id, quantity=quantity)
            st.success("Stock updated successfully")

        except Exception as e:
            st.error(str(e))

# ---------------------------------------------------
# DELETE PRODUCT
# ---------------------------------------------------

elif menu == "Delete Product From Inventory":

    st.header("Delete Product From Inventory")

    inventory_name = st.text_input("Inventory Name")
    location = st.text_input("Location")
    product_name = st.text_input("Product Name")

    if st.button("Delete Product"):

        try:
            with get_session() as session:

                inventory_id = Generic.get_inventory_id(session, inventory_name, location)

                Inventory.delete_product_from_inventory(session=session, product_name=product_name, inventory_id=inventory_id)

            st.success("Product deleted successfully")

        except Exception as e:
            st.error(str(e))

# ---------------------------------------------------
# TRANSFER STOCK
# ---------------------------------------------------

elif menu == "Transfer Stock":

    st.header("Transfer Stock")

    source_inventory_name = st.text_input("Source Inventory Name")
    source_inventory_location = st.text_input("Source Inventory Location")
    destination_inventory_name = st.text_input("Destination Inventory Name")
    destination_inventory_location = st.text_input("Destination Inventory Location")
    product_name = st.text_input("Product Name")
    quantity = st.number_input(
        "Add Quantity",
        min_value=-1000,
        step=1,
        value=0
    )

    if st.button("Transfer"):

        try:
            with get_session() as session:
                source_inventory_id = Generic.get_inventory_id(session, source_inventory_name, source_inventory_location)
                destination_inventory_id = Generic.get_inventory_id(session, destination_inventory_name, destination_inventory_location)

                InventoryManager.transfer_stock(
                    session,
                    product_name,
                    source_inventory_id,
                    destination_inventory_id,
                    quantity
                )

            st.success("Stock transferred successfully")

        except Exception as e:
            st.error(str(e))

# ---------------------------------------------------
# TOTAL STOCK
# ---------------------------------------------------

elif menu == "Total Stock Across Inventories":

    st.header("Total Stock Across Inventories")

    product_name = st.text_input("Product Name")

    if st.button("Get Total Stock"):

        try:
            with get_session() as session:

                product = (
                    InventoryManager.get_total_stock_across_inventories(
                        session,
                        product_name
                    )
                )

                if product:

                    st.write({
                        "Product": product.name,
                        "Category": product.category,
                        "Total Stock": product.total_stocks
                    })

                else:
                    st.warning("Product not found")

        except Exception as e:
            st.error(str(e))