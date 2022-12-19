from selenium.webdriver.common.by import By
from seleniumpagefactory import PageFactory

from WebElements import ProductInCartElement, ProductElement


class BasePage(PageFactory):
    def __init__(self, driver):
        self.driver = driver


locators = {
    "login_button": (By.ID, 'login2'),
    "form_login_button": (By.XPATH, "//button[@onclick='logIn()']"),
    "username_input": (By.ID, "loginusername"),
    "password_input": (By.ID, "loginpassword"),
    "welcome_user": (By.ID, 'nameofuser'),
    "monitors_menu": (By.XPATH, "//a[contains(@onclick,'monitor')]"),
    "products_list": (By.XPATH, "//*[@id='tbodyid']"),
    "logout_button": (By.ID, 'logout2')
}


class HomePage(BasePage):

    def get_list_of_products(self):
        return list(map(lambda x: ProductElement(x),
                        self.driver.find_elements(By.XPATH, "//*[@id='tbodyid']//div[contains(@class, 'card h-100')]")))


class ProductPage(BasePage):
    locators = {
        "pr_price": (By.XPATH, "//*[@class='price-container']"),
        "pr_name": (By.XPATH, "//*[@class='name']"),
        "cart_link": (By.XPATH, "//*[contains(@onclick, 'showcart') or @href='cart.html']"),
        "add_to_cart_button": (By.XPATH, "//a[contains(@onclick, 'addToCart')]")
    }


class CartPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def get_products(self):
        return list(map(lambda x: ProductInCartElement(x),
                        self.driver.find_element(By.ID, "tbodyid").find_elements(By.CLASS_NAME, "success")))
