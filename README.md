# Glowmark Stock Management System 💄📊 (Mock Project)

This project is a mock stock management system for **Glowmark**, a fictional facial products business.  
It demonstrates how inventory can be tracked efficiently instead of handling everything manually.

## Business Problem

Glowmark currently manages all inventory manually.  
This leads to several challenges:

- Stock shortages or overstock due to human error  
- Difficulty tracking products and suppliers  
- Time-consuming record-keeping and reporting  
- Inconsistent data for decision-making  

The Stock Management System aims to streamline inventory tracking, improve accuracy, and save time, allowing Glowmark to focus on growing the business.

## Business Solution

The Stock Management System for Glowmark is a mock project designed to:

- Track all products and their quantities  
- Record supplier details and purchase information  
- Monitor stock levels and generate low-stock alerts  
- Produce basic inventory reports for decision-making  

This project demonstrates **requirements analysis, process mapping, and system documentation**, showing skills in information systems design and business analysis.

## Features


- Simulated data to show system functionality  
- Stock management (add/update/delete products)  
- Supplier management  
- Sales tracking  
- Stock alerts with color-coded highlights  
- Inventory reports with tables and graphs  
- CSV export for tables and reports

## System UI


## Structure / Tables
| Table Name           | Fields / Attributes                         | Description                                      |
|----------------------|--------------------------------------------|-------------------------------------------------|
| PRODUCTS             | ProductID, Name, Category, Price, Quantity | Stores all facial products available at Glowmark |
| SUPPLIERS            | SupplierID, Name, Contact, ProductsSupplied | Tracks supplier details and products supplied  |
| STOCK_TRANSACTIONS   | TransactionID, Date, ProductID, QuantityIn, QuantityOut, SupplierID | Records stock movement (in/out)                |
| REORDER_ALERTS       | ProductID, MinimumQuantity, AlertStatus     | Monitors low stock and triggers reorder alerts |
| SALES                | SaleID, ProductID, QuantitySold, TotalSale, DateSold | Tracks product sales |


## Technologies Used

- **Programming & UI:** Python, Tkinter  
- **Database:** SQLite  
- **Documentation & Diagrams:** Microsoft Word, Excel, Lucidchart/Draw.io/Canva  
- **Version Control:** GitHub

## How to Run 
