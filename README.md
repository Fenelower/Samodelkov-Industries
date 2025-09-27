# Samodelkov Industries Analytics

## About the Company
**Samodelkov Industries** is a data analytics company.  
This project focuses on analyzing the customer database to understand **customer distribution by regions, popular cities, and unique clients**.

---

## About the Project
This project performs **basic analytics** on the customers of Samodelkov Industries using **SQL queries** and a **Python automation script**.  

Key functionalities include:
- Counting customers by **state, city, ZIP code**.
- Identifying **unique customers**.
- Checking for **duplicates** in the database.
- Automating query execution and saving results to **CSV files** using Python.

---

## Repository Structure
<img width="470" height="193" alt="image" src="https://github.com/user-attachments/assets/b49201f2-a79f-494f-93b5-30e279bd8d15" />


---


## ER-diagram
<img width="1040" height="839" alt="image" src="https://github.com/user-attachments/assets/23915964-8897-4a9e-bca1-2729c23abd00" />



---


## How to Run the Project

### 1. Create Table and Import CSV
1. Make sure **PostgreSQL** is installed and the database is created.
2. Open **psql** or **pgAdmin**.
3. Run the setup script:
   ```sql
   \i 'C:\Users\Пользователь\Desktop\DATAVISUALISATION/customers_setup.sql'

✅ This will create the customers table and import the CSV data.

## 2. Run SQL Analytics Queries

Open queries.sql in psql or pgAdmin.

Execute all 10 queries.

Results can be viewed in the terminal or in pgAdmin.

## 3. Run Python Script

### Install required Python libraries:
```pip install psycopg2-binary pandas```

### Open main.py and configure your database connection:
```
DB_HOST = 'localhost
DB_NAME = 'MAXIMVISUAL'
DB_USER = 'postgres'
DB_PASS = 'maxim22s2'
DB_PORT = 5433
```

## Run the script:
```python main.py```
The script will display results in the terminal and save CSV files in the project folder.

### Tools and Resources
-PostgreSQL
-psql / pgAdmin
-Python 3.x
-Python libraries: psycopg2-binary, pandas
-Git & GitHub
-Customer CSV file
-VS Code / Notepad++ (for editing scripts)

### License

This project is licensed under the MIT License.

