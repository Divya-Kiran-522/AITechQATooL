import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def chrome_driver():
    """
    Fixture that automatically configures and provides a Chrome WebDriver instance.
    Automatically downloads ChromeDriver if not present.
    """
    chrome_options = Options()
    
    # Optional: Uncomment to run headless (without visible browser window)
    # chrome_options.add_argument("--headless")
    
    # Additional Chrome options for better automation
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    
    # Set up Chrome with automatic driver management
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver
    
    # Cleanup after test
    driver.quit()


@pytest.fixture(scope="session")
def chrome_driver_headless():
    """
    Fixture for headless Chrome (no visible window).
    Useful for CI/CD pipelines.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver
    
    driver.quit()


def pytest_configure(config):
    """
    Print configuration info at test startup
    """
    print("\n" + "="*60)
    print("Chrome WebDriver Configuration Loaded")
    print("="*60)
    print("Browser: Google Chrome")
    print("Driver: Automatically managed by webdriver-manager")
    print("ChromeDriver will be auto-downloaded if needed")
    print("="*60 + "\n")
