import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestWebsite(unittest.TestCase):
    def test_website(self):
        # Set up the Chrome browser
        driver = webdriver.Chrome()
        login_url = "http://127.0.0.1:5000/login"
        driver.get(login_url)

        # Log in
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password_hash")
        login_button = driver.find_element(By.CSS_SELECTOR, "input.submit-field")

        email_input.send_keys("test@gmail.com")
        password_input.send_keys("Test2023!")
        login_button.click()
        print("Clicked login button")

        print("Waiting for 'homepage' element...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "homepage"))
        )
        print("Found 'homepage' element")
        driver.get("http://127.0.0.1:5000/properties")

        header = driver.find_element(By.TAG_NAME, "h1")
        assert header.text == "OMH"

        properties = driver.find_elements(By.CSS_SELECTOR, "#props table tr")
        assert len(properties) > 1

        # Apply Price filter
        price_filter = driver.find_element(By.ID, "price-filter")
        price_filter.send_keys("250001-500000")

        # Apply Bedrooms filter (3 bedrooms)
        bedrooms_filter = driver.find_element(By.ID, "bedrooms-filter")
        bedrooms_filter.send_keys("3")

        # Apply Bathrooms filter (2 bathrooms)
        bathrooms_filter = driver.find_element(By.ID, "bathrooms-filter")
        bathrooms_filter.send_keys("2")

        apply_filters = driver.find_element(By.ID, "apply-filters")
        apply_filters.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#props table tr"))
        )

        filtered_properties = driver.find_elements(By.CSS_SELECTOR, "#props table tr")
        assert len(filtered_properties) <= len(properties)

        # Reset filters
        reset_filters = driver.find_element(By.ID, "reset-filters")
        reset_filters.click()

        # Apply Bedrooms filter (5 bedrooms)
        bathrooms_filter.send_keys("5")

        apply_filters.click()

        # Check for "Sorry, no properties meet your choices" message
        no_properties_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#no-properties-message"))
        )
        assert no_properties_message.text == "Sorry, no properties meet your choices."

        driver.quit()

if __name__ == "__main__":
    unittest.main()
