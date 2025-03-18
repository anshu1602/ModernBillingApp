# Elegant Billing System

A modern billing application with a graphical user interface (GUI) built using PySide6, designed to manage customer transactions and generate bills. The application connects to a MySQL database to store customer and billing information.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Database Setup](#database-setup)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- Add new customer transactions with details (name, phone, item, quantity, price, payment method).
- View and refresh a table of recent transactions with calculated totals.
- Calculate total revenue and transaction count dynamically.
- Modern UI with a customizable color scheme.
- Persistent data storage using MySQL.
- Error handling for invalid inputs and database issues.

## Prerequisites
Before running the application, ensure you have the following installed:
- **Python 3.7 or higher**
- **MySQL Server** (e.g., MySQL Community Server)
- Required Python packages:
  - `PySide6` (for GUI)
  - `mysql-connector-python` (for MySQL connectivity)

You can install the dependencies using pip:
```bash
pip install PySide6 mysql-connector-python
