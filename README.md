# Python-Project

# 🛒 Product Management System (with Streamlit + MongoDB)  

A **Product Management System** built with **Streamlit** and **MongoDB Atlas**.  
This system supports **two types of users**:  

- **Admin**: Add/manage products, apply discounts, generate reports, save/load products.  
- **Customer**: Register/login, view and purchase products, check reports.  

All **user authentication** is handled via MongoDB (customers) and **predefined admin credentials**. Products can also be exported/imported via CSV.  

---

## 🚀 Features  

### 🔑 Authentication  
- Secure login with **hashed passwords (SHA-256)**.  
- **Admins** have predefined credentials.  
- **Customers** can self-register (stored in MongoDB).
- <img width="977" height="770" alt="image" src="https://github.com/user-attachments/assets/da7b2a99-4732-4422-aa16-f960328fde90" />


### 👨‍💼 Admin Features  
- Add new products with name, price, and quantity.  
- Apply percentage discounts across all products.  
- Calculate total stock value.  
- Filter and list out-of-stock products.  
- Save product list to CSV or load products from CSV.  

### 👩‍💻 Customer Features  
- Browse available products.  
- Purchase products (stock decreases automatically).  
- View reports (total stock value & out-of-stock items).  

### 💾 Storage  
- Users are stored in **MongoDB Atlas**.  
- Products are stored in **Streamlit session state** (with optional CSV persistence).  

---

## 🛠️ Requirements  

Install dependencies:  

```bash
pip install streamlit pymongo pandas
