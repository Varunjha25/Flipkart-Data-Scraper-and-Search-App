import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configure ChromeDriver path and user agent
chrome_driver_path = r"C:\Users\Ankit\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

db_name = "scraped_data.db" 
table_name = "scraped_links"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT
)
""")
conn.commit()

url = "https://www.flipkart.com/"  
try:
    driver.get(url)
    elements = driver.find_elements(By.CSS_SELECTOR, "a") 
    scraped_data = [{"title": e.text, "link": e.get_attribute("href")} for e in elements if e.text.strip()]

    
    for data in scraped_data:
        cursor.execute(f"""
        INSERT INTO {table_name} (title, link)
        VALUES (?, ?)
        """, (data['title'], data['link']))

    print("Data saved to database successfully!")

finally:
    driver.quit()
    conn.close()
    
conn = sqlite3.connect("scraped_data.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM scraped_links")
for row in cursor.fetchall():
    print(row)
conn.close()
