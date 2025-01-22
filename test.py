import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests

# Initialize the WebDriver (using Chrome here)
driver = webdriver.Chrome()

def check_https(url):
    """ Check if the website is using HTTPS """
    if url.startswith('https://'):
        print("[+] HTTPS is enabled.")
    else:
        print("[!] HTTPS is not enabled.")

def test_login_vulnerabilities(url, username_field_id, password_field_id, login_button_xpath, username, password):
    """ Test basic login vulnerabilities like weak credentials handling """
    driver.get(url)
    time.sleep(2)
    
    # Attempting to login with a weak password or common credentials
    username_input = driver.find_element(By.ID, username_field_id)
    password_input = driver.find_element(By.ID, password_field_id)
    login_button = driver.find_element(By.XPATH, login_button_xpath)
    
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()
    time.sleep(3)
    
    # Check for failure message or login success indicator
    page_source = driver.page_source
    if "incorrect" in page_source.lower() or "error" in page_source.lower():
        print("[+] Login failed as expected for weak credentials.")
    else:
        print("[!] Vulnerability: Weak credentials did not fail.")

def test_sensitive_data_exposure(url):
    """ Check if any sensitive data is exposed in the page source """
    driver.get(url)
    time.sleep(2)
    
    page_source = driver.page_source
    if "password" in page_source or "token" in page_source:
        print("[!] Sensitive data (e.g., password or token) exposed in page source.")
    else:
        print("[+] No sensitive data found in page source.")

def check_headers(url):
    """ Check for some important HTTP headers like CSP and HSTS """
    response = requests.get(url)
    headers = response.headers
    
    if 'Strict-Transport-Security' in headers:
        print("[+] Strict-Transport-Security header is present.")
    else:
        print("[!] Missing Strict-Transport-Security header.")
    
    if 'Content-Security-Policy' in headers:
        print("[+] Content-Security-Policy header is present.")
    else:
        print("[!] Missing Content-Security-Policy header.")
    
    if 'X-Content-Type-Options' in headers:
        print("[+] X-Content-Type-Options header is present.")
    else:
        print("[!] Missing X-Content-Type-Options header.")

def main():
    # URL for testing
    url = 'https://dronacharyatech.netlify.app/'  # Replace with the target URL
    username_field_id = 'learner1@synoize.com'  # Replace with actual username field ID
    password_field_id = 'qwerty'  # Replace with actual password field ID
    login_button_xpath = '//*[contains(text(),′Login′)]'  # Replace with actual login button XPath
    username = 'admin@synoize.com'  # Replace with a common username
    password = 'qwerty'  # Replace with a weak password
    
    # Creating threads for each test
    threads = []
    
    # Check HTTPS (runs in its own thread)
    thread_https = threading.Thread(target=check_https, args=(url,))
    threads.append(thread_https)
    
    # Test login vulnerabilities (runs in its own thread)
    # thread_login = threading.Thread(target=test_login_vulnerabilities, args=(url, username_field_id, password_field_id, login_button_xpath, username, password))
    # threads.append(thread_login)
    
    # Test sensitive data exposure (runs in its own thread)
    thread_sensitive_data = threading.Thread(target=test_sensitive_data_exposure, args=(url,))
    threads.append(thread_sensitive_data)
    
    # Check HTTP headers (runs in its own thread)
    thread_headers = threading.Thread(target=check_headers, args=(url,))
    threads.append(thread_headers)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Quit the WebDriver session
    # driver.quit()
    time.sleep(60)
if __name__ == "__main__":
    main()
