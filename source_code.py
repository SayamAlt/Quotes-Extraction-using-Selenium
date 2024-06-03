import time, pickle, os, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def login(driver,username,password):
    website = "http://quotes.toscrape.com//"
    # Open the website
    driver.get(website)
    
    # Click the login button to access the login page
    login_button = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/p/a")
    login_button.click()
    time.sleep(5)
    
    try:
        # Find the username field and enter the username
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys(username)
        # Find the password field and enter the password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        # Find the login button and click it
        login_button = driver.find_element(By.XPATH, "/html/body/div/form/input[2]")
        login_button.click()
        time.sleep(5) # Wait for login to complete
    except:
        raise Exception("Login failed!")

def scrape_data(driver):
    # Scrape all the quotes of the first page
    quotes = driver.find_elements(By.CLASS_NAME, "quote")

    # Initialize a variable to store all the quotes
    data = []

    # Extract various available attributes within each quote
    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text
        tags = quote.find_element(By.CLASS_NAME, "tags").text
        text = str(text).removeprefix('“').removesuffix('”')
        data.append([text,author,tags]) 

    # Find the next button and click it
    next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")

    # Loop until the next button doesn't exist on the webpage i.e. it is the last webpage containing quotes
    while next_button:
        next_button.click() # Click the next button
        # Scrap all quotes present within the page
        quotes = driver.find_elements(By.CLASS_NAME, "quote")

        for quote in quotes:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            tags = quote.find_element(By.CLASS_NAME, "tags").text
            text = str(text).removeprefix('“').removesuffix('”')
            data.append([text,author,tags])
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.next a") # Find the next button at each iteration
        except:
            break # Terminate the loop if the next button doesn't appear
        
    return data

def main():
    try:
        # Load the .env file
        load_dotenv('login_credentials.env')
        # Get the login credentials from the .env file
        username = str(os.getenv("username")).lower()
        password = str(os.getenv("password")).lower()
        # Set path to Chrome driver
        webdriver_service = Service('../../chromedriver.exe') 
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(service=webdriver_service,options=chrome_options)
        login(driver,username,password)
        data = scrape_data(driver)
        
        # Save data to a CSV file
        with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Text","Author","Tags"])
            writer.writerows(data)
    finally:
        driver.close() # Close the web driver

if __name__ == '__main__':
    main()