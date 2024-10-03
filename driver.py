import pytest
from selenium import webdriver


options = webdriver.ChromeOptions()
options.set_capability("selenoid:options", {
    "enableVNC": True,
    "screenResolution": "1280x1024x24",
    "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru", "LC_ALL=ru_RU.UTF-8"]
})

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Remote(command_executor="http://185.93.109.120:4444/wd/hub", options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
