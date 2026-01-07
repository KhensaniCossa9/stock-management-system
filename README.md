# Glowmark Stock Management System 💄📊 (Mock Project)

The **Glowmark Stock Management System** is a mock desktop application developed for a fictional facial-product business. The project demonstrates how small businesses can move from manual stock tracking to a structured, digital inventory system.

This project was created to showcase **information systems analysis, business logic, and system design skills**.

## Business Problem

Glowmark currently manages all inventory manually.  
This leads to several challenges:

- Inaccurate stock counts
- Stock shortages or overstocking
- Difficulty tracking suppliers for restocking and sales
- No clear visibility of low stock items
- Time-consuming reporting

The Stock Management System aims to streamline inventory tracking, improve accuracy, and save time, allowing Glowmark to focus on growing the business.

## Business Solution

The Stock Management System for Glowmark provides a structured solution that:

- Tracks products and their quantities  
- Records sales transactions
- Manages supplier information
- Monitors stock levels and flags low stock
- Generates clear inventory reports

## Key Features

-**Welcome Dashboard**
 - Displays total products, total sales, and low-stock count

- **Stock Management**
  - Add, update, and view products
  - Automatic quantity calculations

- **Sales Management**
  - Record product sales
  - Automatically updates stock levels

- **Supplier Management**
  - Store supplier names and contact details
  - Supports restocking workflows

- **Stock Alerts**
  - Color-coded stock levels:
    - 🔴 Critical (below 15)
    - 🟡 Low (15–29)
    - 🟢 Healthy (30+)
  - Filter by stock status
  - Reorder shortcut to suppliers

-**Reports**
 - Stock level report with table and bar graph
 - Export stock data to CSV for analysis
 - Sorted to highlight low-stock items first

## Screenshots (UI overview)


## Conceptual Database Design

| Table Name             | Fields / Attributes                                                                | Description                                                |
| ---------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **PRODUCTS**           | ProductID (PK), Name, Category, Price, Quantity                                    | Stores all facial products sold by Glowmark                |
| **SUPPLIERS**          | SupplierID (PK), Name, Phone, Email, ProductType                                   | Stores supplier contact details and supplied product types |
| **STOCK_TRANSACTIONS** | TransactionID (PK), Date, ProductID (FK), QuantityIn, QuantityOut, SupplierID (FK) | Records all stock movement (purchases and sales)           |
| **REORDER_ALERTS**     | AlertID (PK), ProductID (FK), MinimumQuantity, AlertStatus                         | Monitors low stock levels and triggers reorder alerts      |
| **SALES**              | SaleID (PK), ProductID (FK), QuantitySold, TotalSale, DateSold                     | Tracks all product sales for reporting                     |


## Technologies Used

- **Programming & Language:** Python
- **User Interface:** Tkinter  
- **Database:** SQLite  
- **Version Control & Portfolio:** GitHub

## How to Run the Project

1. Download or clone the repository
2. Open the project folder
3. Run the main Python file:
   ```bash
   python glowmark.py
4. The application opens as a desktop window

## Project Type
This is a mock project created for learning, portfolio. and demonstration purposes.
It is not a live commercial system

## Author
Created by Khensani Cossa
(Bcom Information Systems Graduate)
