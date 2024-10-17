import tkinter as tk
from tkinter import messagebox

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

# Start the GUI event loop
root.mainloop()
