import streamlit as st
import pandas as pd
from functools import reduce

# Dummy user credentials (in a real application, you'd use a database)
USER_CREDENTIALS = {
    "admin": {"password": "password123", "role": "admin"},
    "customer": {"password": "buy123", "role": "customer"}
}

# Global product dictionary to store product information
if 'products' not in st.session_state:
    st.session_state.products = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None

# Function to handle product input
def input_products(product_name, price, quantity):
    if product_name and price > 0 and quantity > 0:
        st.session_state.products[product_name] = {'price': price, 'quantity': quantity}
        st.success(f"Product '{product_name}' added successfully!")
        update_product_list()
    else:
        st.error("Please fill all fields with valid data.")

# Function to update the product list displayed in the GUI
def update_product_list():
    if st.session_state.products:
        st.write("**Product List:**")
        for product, info in st.session_state.products.items():
            st.write(f"{product}: Price = {info['price']}, Quantity = {info['quantity']}")
    else:
        st.write("No products available.")

# Function to handle product selection and purchase
def select_product(selected_product):
    if selected_product and st.session_state.products[selected_product]['quantity'] > 0:
        st.session_state.products[selected_product]['quantity'] -= 1
        st.success(f"Thank you for purchasing {selected_product}.")
        update_product_list()
    elif selected_product:
        st.error(f"{selected_product} is out of stock.")
    else:
        st.error("Please select a product.")

# Function to apply a discount to all products
def apply_discount(discount_percentage):
    if 0 <= discount_percentage <= 100:
        discount_factor = 1 - discount_percentage / 100
        for product in st.session_state.products.keys():
            st.session_state.products[product]['price'] = round(st.session_state.products[product]['price'] * discount_factor, 2)
        st.success(f"Discount of {discount_percentage}% applied to all products.")
        update_product_list()
    else:
        st.error("Please enter a valid discount percentage (0-100).")

# Function to calculate total stock value
def calculate_total_stock_value():
    total_value = reduce(lambda acc, product: acc + (product['price'] * product['quantity']), st.session_state.products.values(), 0)
    st.info(f"Total stock value: ${total_value:.2f}")

# Function to filter out-of-stock products
def filter_out_of_stock():
    out_of_stock_products = [p for p in st.session_state.products if st.session_state.products[p]['quantity'] == 0]
    if out_of_stock_products:
        st.info(f"Out of stock products: {', '.join(out_of_stock_products)}")
    else:
        st.info("All products are in stock.")

# Function to save products to a CSV file
def save_to_csv():
    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products).T  # Convert to DataFrame and transpose for proper format
        df.to_csv("products.csv")
        st.success("Products saved to 'products.csv'.")
    else:
        st.error("No products to save.")

# Function to load products from a CSV file
def load_from_csv():
    try:
        df = pd.read_csv("products.csv", index_col=0)
        st.session_state.products = df.T.to_dict()  # Convert DataFrame back to dictionary
        st.success("Products loaded from 'products.csv'.")
        update_product_list()
    except FileNotFoundError:
        st.error("'products.csv' not found.")

# Login function
def login(username, password, role):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password and USER_CREDENTIALS[username]["role"] == role:
        st.session_state.logged_in = True
        st.session_state.role = role
        st.success(f"Login successful! Role: {st.session_state.role.capitalize()}")
    else:
        st.error("Invalid username, password, or role.")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.success("You have been logged out.")

# Main Application
st.title("Product Management System")

# Navigation
if not st.session_state.logged_in:
    # Login Section
    st.header("Login")

    # Role Selection
    role = st.radio("Who are you?", ["Customer", "Admin"])

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        login_button = st.form_submit_button("Login")

    if login_button:
        # Convert role to lowercase for consistency with USER_CREDENTIALS
        login(username, password, role.lower())

else:
    # Sidebar with logout button
    with st.sidebar:
        st.sidebar.header(f"Logged in as {st.session_state.role.capitalize()}")
        if st.button("Logout"):
            logout()

    # Page selection for logged-in users based on role
    if st.session_state.role == "admin":
        page = st.sidebar.selectbox("Select Page", ["Add Products", "Reports"])

        if page == "Add Products":
            # Product Input Section
            st.header("Add New Product")
            with st.form("product_form"):
                product_name = st.text_input("Product Name")
                product_price = st.number_input("Price", min_value=0.0, step=0.01)
                product_quantity = st.number_input("Quantity", min_value=0, step=1)
                submitted = st.form_submit_button("Add Product")

            if submitted:
                input_products(product_name, product_price, product_quantity)

        elif page == "Reports":
            # Discount Section
            st.header("Apply Discount")
            discount_percentage = st.number_input("Discount Percentage", min_value=0, max_value=100, step=1)
            if st.button("Apply Discount"):
                apply_discount(discount_percentage)

            # Stock Value Calculation Section
            if st.button("Calculate Total Stock Value"):
                calculate_total_stock_value()

            # Filter Out of Stock Section
            if st.button("Filter Out of Stock Products"):
                filter_out_of_stock()

            # Save/Load Section
            st.header("Save/Load Products")
            if st.button("Save to CSV"):
                save_to_csv()
            if st.button("Load from CSV"):
                load_from_csv()

    elif st.session_state.role == "customer":
        page = st.sidebar.selectbox("Select Page", ["Purchase Products", "Reports"])

        if page == "Purchase Products":
            # Product Purchase Section
            st.header("Purchase Product")
            if st.session_state.products:
                selected_product = st.selectbox("Select a Product to Purchase", list(st.session_state.products.keys()))
                if st.button("Purchase"):
                    select_product(selected_product)
            else:
                st.warning("No products available for purchase.")

        elif page == "Reports":
            # Stock Value Calculation Section
            if st.button("Calculate Total Stock Value"):
                calculate_total_stock_value()

            # Filter Out of Stock Section
            if st.button("Filter Out of Stock Products"):
                filter_out_of_stock()

    # Product List Section
    st.header("Product List")
    update_product_list()
