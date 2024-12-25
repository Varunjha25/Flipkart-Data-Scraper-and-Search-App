# Flipkart-Data-Scraper-and-Search-App
![image](https://github.com/user-attachments/assets/64cf3ff9-478f-4015-9297-e57fbcbd54aa)
import sqlite3
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
### Imports:
### sqlite3 is for interacting with the SQLite database.
### selenium modules are used for web scraping by automating a browser (in this case, Chrome).

## Chrome Setup
---  Set ChromeDriver path and User-Agent
chrome_driver_path = r"C:\path\to\chromedriver.exe"
user_agent = "Mozilla/5.0 ..."

### ChromeDriver Path: Specifies the location of the ChromeDriver on your system to allow Selenium to control Chrome.

### User-Agent: A string representing the browser and system details to mimic a real user browsing the web.

-- Configure Chrome options
chrome_options = Options()

chrome_options.add_argument(f"user-agent={user_agent}")

chrome_options.add_argument("--headless")

chrome_options.add_argument("--disable-gpu")

### Chrome Options: Sets Chrome to run in "headless" mode (no UI), use the custom user agent, and disable GPU hardware acceleration (for smoother performance in headless mode).

-- Initialize WebDriver
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

### WebDriver Setup: Initializes the Chrome browser with the specified options and the path to the ChromeDriver.

## SQLite Database Setup
---et up SQLite database and create table
db_name = "scraped_data.db"

table_name = "scraped_links"

conn = sqlite3.connect(db_name)

cursor = conn.cursor()

cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (

                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    
                    title TEXT, 
                    
                    link TEXT)""")

conn.commit()

### Database Connection: Connects to the SQLite database (scraped_data.db).

### Table Creation: Creates the scraped_links table if it doesn’t exist. This table has three columns: id (primary key), title, and link.

## Web Scraping
--- Scrape links from a webpage
url = "https://www.flipkart.com/"

try:
    driver.get(url)

    elements = driver.find_elements(By.CSS_SELECTOR, "a")
    
    scraped_data = [{"title": e.text, "link": e.get_attribute("href")} for e in elements if e.text.strip()]

### URL: The URL of the page to scrape.
### driver.get(url): Opens the specified URL in the Chrome browser.
### driver.find_elements: Finds all anchor (<a>) elements on the page.
### Scraping Data: Creates a list of dictionaries, each containing the title (text) and link (href attribute) of the anchor tags, filtering out empty links (where e.text.strip() is not empty).

--- Save scraped data into database
for data in scraped_data:
    cursor.execute(f"""INSERT INTO {table_name} (title, link) VALUES (?, ?)""", 
                   (data['title'], data['link']))
print("Data saved to database!")

### Insert into Database: For each scraped link, inserts its title and link into the scraped_links table.
### Confirmation: Prints a message indicating that the data has been saved.
finally:

    driver.quit()
    
    conn.close()
### Cleanup: Ensures the browser and database connection are closed even if there’s an error.

## Display Data from Database

# Display data from database
conn = sqlite3.connect(db_name)

cursor = conn.cursor()

cursor.execute("SELECT * FROM scraped_links")

for row in cursor.fetchall():

    print(row)

conn.close()
### Reopen Database Connection: Connects to the database again.
### Retrieve and Print Data: Executes a query to fetch all data from the scraped_links table and prints each row.

## Streamlit Interface for Searching
# Streamlit interface to search data
import streamlit as st

import pandas as pd


st.title("Customer Search Box")

customer_code = st.text_input("Enter Customer Code or Keyword to Search:", "")

## Streamlit Setup: Initializes a Streamlit app where users can input a keyword (customer_code) to search.
# Function to load data from SQLite database
def load_data(query):

    conn = sqlite3.connect(db_path)
    
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    
    return df
### load_data Function: Executes an SQL query, loads the result into a pandas DataFrame, and returns it.
# Query the database if customer_code

if customer_code:

    query = f"""SELECT * FROM scraped_links WHERE title LIKE '%{customer_code}%'"""
    
    df = load_data(query)
    
    st.write(df)
### Search Query: If the user enters a keyword, an SQL query is constructed to find rows where either the title or link contains the customer_code.
### Display Results: Displays the results as a table in the Streamlit app.

