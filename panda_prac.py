import tkinter as tk
from tkinter import messagebox
from functools import reduce
import pandas as pd

# Global product dictionary to store product information
products = {}

# Function to handle product input
def input_products():
    product_name = product_name_entry.get().strip()
    try:
        price = float(product_price_entry.get())
        quantity = int(product_quantity_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid price and quantity values.")
        return

    if product_name and price > 0 and quantity > 0:
        products[product_name] = {'price': price, 'quantity': quantity}
        update_product_list()
        clear_entries()
    else:
        messagebox.showerror("Input Error", "Please fill all fields with valid data.")

# Function to clear input fields after adding a product
def clear_entries():
    product_name_entry.delete(0, tk.END)
    product_price_entry.delete(0, tk.END)
    product_quantity_entry.delete(0, tk.END)

# Function to update the product list displayed in the GUI
def update_product_list():
    product_listbox.delete(0, tk.END)
    for product, info in products.items():
        product_listbox.insert(tk.END, f"{product}: Price = {info['price']}, Quantity = {info['quantity']}")

# Function to handle product selection and purchase
def select_product():
    selected = product_listbox.curselection()
    if not selected:
        messagebox.showerror("Selection Error", "Please select a product.")
        return

    product_name = product_listbox.get(selected).split(':')[0]
    if products[product_name]['quantity'] > 0:
        products[product_name]['quantity'] -= 1
        messagebox.showinfo("Purchase Successful", f"Thank you for purchasing {product_name}.")
        update_product_list()
    else:
        messagebox.showerror("Out of Stock", f"{product_name} is out of stock.")

# Function to apply a discount to all products using map and lambda
def apply_discount():
    try:
        discount_percentage = float(discount_entry.get())
        if 0 <= discount_percentage <= 100:
            discount_factor = 1 - discount_percentage / 100
            for product in products.keys():
                products[product]['price'] = round(products[product]['price'] * discount_factor, 2)
            update_product_list()
            messagebox.showinfo("Discount Applied", f"Discount of {discount_percentage}% applied to all products.")
        else:
            messagebox.showerror("Input Error", "Please enter a valid discount percentage (0-100).")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the discount percentage.")

# Function to calculate total stock value using reduce and lambda
def calculate_total_stock_value():
    total_value = reduce(lambda acc, product: acc + (product['price'] * product['quantity']), products.values(), 0)
    messagebox.showinfo("Total Stock Value", f"Total stock value: ${total_value:.2f}")

# Function to filter out-of-stock products using filter and lambda
def filter_out_of_stock():
    out_of_stock_products = list(filter(lambda p: products[p]['quantity'] == 0, products.keys()))
    if out_of_stock_products:
        messagebox.showinfo("Out of Stock", f"Out of stock products: {', '.join(out_of_stock_products)}")
    else:
        messagebox.showinfo("All in Stock", "All products are in stock.")

# Function to save products to a CSV file using pandas
def save_to_csv():
    if not products:
        messagebox.showerror("Save Error", "No products to save.")
        return

    df = pd.DataFrame(products).T  # Convert to DataFrame and transpose for proper format
    df.to_csv("products.csv")
    messagebox.showinfo("Save Successful", "Products saved to 'products.csv'.")

# Function to load products from a CSV file using pandas
def load_from_csv():
    try:
        df = pd.read_csv("products.csv", index_col=0)
        global products
        products = df.T.to_dict()  # Convert DataFrame back to dictionary
        update_product_list()
        messagebox.showinfo("Load Successful", "Products loaded from 'products.csv'.")
    except FileNotFoundError:
        messagebox.showerror("Load Error", "'products.csv' not found.")

# Main window setup
root = tk.Tk()
root.title("Product Management System")

# Product Input Section
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

tk.Label(input_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
product_name_entry = tk.Entry(input_frame)
product_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
product_price_entry = tk.Entry(input_frame)
product_price_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
product_quantity_entry = tk.Entry(input_frame)
product_quantity_entry.grid(row=2, column=1, padx=5, pady=5)

add_product_button = tk.Button(input_frame, text="Add Product", command=input_products)
add_product_button.grid(row=3, column=0, columnspan=2, pady=10)

# Product List Section
product_list_frame = tk.Frame(root)
product_list_frame.pack(padx=10, pady=10)

product_listbox = tk.Listbox(product_list_frame, width=50, height=10)
product_listbox.pack()

select_product_button = tk.Button(product_list_frame, text="Select Product", command=select_product)
select_product_button.pack(pady=10)

# Discount Section
discount_frame = tk.Frame(root)
discount_frame.pack(padx=10, pady=10)

tk.Label(discount_frame, text="Apply Discount (%):").grid(row=0, column=0, padx=5, pady=5)
discount_entry = tk.Entry(discount_frame)
discount_entry.grid(row=0, column=1, padx=5, pady=5)

discount_button = tk.Button(discount_frame, text="Apply Discount", command=apply_discount)
discount_button.grid(row=1, column=0, columnspan=2, pady=10)

# Stock Value and Filter Section
stock_frame = tk.Frame(root)
stock_frame.pack(padx=10, pady=10)

stock_value_button = tk.Button(stock_frame, text="Calculate Total Stock Value", command=calculate_total_stock_value)
stock_value_button.grid(row=0, column=0, padx=5, pady=5)

filter_button = tk.Button(stock_frame, text="Filter Out of Stock", command=filter_out_of_stock)
filter_button.grid(row=0, column=1, padx=5, pady=5)

# Save/Load Section
save_load_frame = tk.Frame(root)
save_load_frame.pack(padx=10, pady=10)

save_button = tk.Button(save_load_frame, text="Save to CSV", command=save_to_csv)
save_button.grid(row=0, column=0, padx=5, pady=5)

load_button = tk.Button(save_load_frame, text="Load from CSV", command=load_from_csv)
load_button.grid(row=0, column=1, padx=5, pady=5)

# Start the GUI event loop
root.mainloop()
