from selenium.webdriver.common.by import By
from seleniumpagefactory import PageFactory


class WebElement(PageFactory):
    def __init__(self, element):
        self.driver = element

    def find_element(self, by, locator):
        return self.driver.find_element(by, locator)

    def click(self):
        return self.driver.click()


class ProductInCartElement(WebElement):
    locators = {
        "pr_name": (By.XPATH, "//td[2]"),
        "pr_price": (By.XPATH, "//td[3]"),
        "delete": (By.XPATH, "//*[contains(@onclick, 'deleteItem')]")
    }


class ProductElement(WebElement):
    locators = {
        "pr_price": (By.XPATH, "//h5"),
        "pr_name": (By.XPATH, "//h4")
    }