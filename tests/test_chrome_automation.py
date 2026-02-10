import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_chrome_browser_automation_example(chrome_driver):
    """
    Example test demonstrating Chrome browser automation with Selenium.
    This test opens Google and verifies the page loaded successfully.
    """
    # Navigate to Google
    chrome_driver.get("https://www.google.com")
    
    # Wait for the page to load and verify title
    assert "Google" in chrome_driver.title
    
    # Verify the search box is present
    search_box = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    assert search_box is not None
    print("✓ Google homepage loaded successfully in Chrome")


def test_chrome_browser_navigation(chrome_driver):
    """
    Example test demonstrating navigation and page interaction in Chrome.
    """
    # Navigate to a website
    chrome_driver.get("https://www.example.com")
    
    # Wait for the page title
    WebDriverWait(chrome_driver, 10).until(
        EC.title_contains("Example")
    )
    
    # Verify page content
    page_source = chrome_driver.page_source
    assert "example.com" in page_source.lower() or "Example Domain" in page_source
    print("✓ Successfully navigated to example.com and verified content")


@pytest.mark.skip(reason="Demonstration - uncomment to run")
def test_chrome_form_interaction_example(chrome_driver):
    """
    Example test for form interaction in Chrome.
    Skipped by default - uncomment to test with your own website.
    """
    chrome_driver.get("https://your-test-website.com")
    
    # Example: Find and fill a text input
    # input_field = chrome_driver.find_element(By.ID, "input_id")
    # input_field.send_keys("test value")
    
    # Example: Click a button
    # button = chrome_driver.find_element(By.XPATH, "//button[@id='submit']")
    # button.click()
    
    print("✓ Form interaction test completed in Chrome")
