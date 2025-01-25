"# distributor_dashboard" 
Installation and Setup

To get started with the distributor dashboard project, follow these steps:
# Distributor Dashboard

This is a Django web application that allows distributors to view their earnings, trends, and other key metrics based on transaction data.

## Features

* **User Authentication:** Distributors can log in with their unique ID and password to access their data.
* **Dashboard:**
    * Daily earnings summary.
    * Weekly earnings trends (visualized with charts).
    * Product category-wise earnings breakdown (visualized with charts).
* **Filters:** Date range filter to customize the data displayed.
* **Data Loading:** Easy data loading from a CSV file.

## Tech Stack

* **Backend:** Python, Django Framework
* **Frontend:** HTML, CSS, JavaScript, Chart.js (for visualizations)
* **Database:** MySql(can be easily switched to other RDBMS supported by Django)

## Installation

1. **Clone the repository:**
   ```bash
   git clone ["this repo's url "]
2. **Activating the enviroment **
   python3 -m venv .venv
   source .venv/bin/activate
4. **Set up the database:**
    python manage.py makemigrations
    python manage.py migrate
5. ** Load data from command **
   python manage.py importdata ./data/transaction_data.csv
6. ** Run the server **
   python manage.py runserver


   For login use distributor details such as Distributor_name for username and Distributor_id for password which will be retrieved from MySql.
   

   This README provides a comprehensive overview of the project, including features, installation instructions, data format, usage guidelines.
