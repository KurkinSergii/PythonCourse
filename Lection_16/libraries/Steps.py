import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Pages import HomePage, ProductPage, CartPage


class MySteps:
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    DATA_CASH = {}

    url = 'https://www.demoblaze.com/'

    def __init__(self):
        self.wait = None
        self.chromedriver = None
        self.home_page = None
        self.product_page = None
        self.cart_page = None

    def start_webdriver(self):
        self.chromedriver = webdriver.Chrome()
        self.chromedriver.fullscreen_window()
        self.wait = WebDriverWait(self.chromedriver, 10)
        self.home_page = HomePage(self.chromedriver)
        self.product_page = ProductPage(self.chromedriver)
        self.cart_page = CartPage(self.chromedriver)

        self.chromedriver.get(self.url)

    def close_webdriver(self):
        self.chromedriver.close()

    def click_login_button(self):
        self.home_page.login_button.click()

    def login_button_is_presented(self):
        return self.wait.until(expected_conditions.visibility_of(self.home_page.form_login_button))

    def set_up_login_and_password(self, login, password):
        self.home_page.username_input.send_keys(login)
        self.home_page.password_input.send_keys(password)
        self.click_form_login_button()

    def log_out_button_is_presented(self):
        return self.wait.until(expected_conditions.visibility_of(self.home_page.logout_button))

    def welcome_message_is_presented(self, username):
        return username in self.home_page.welcome_user.text

    def click_form_login_button(self):
        self.home_page.form_login_button.click()

    def click_on_monitors_category(self):
        self.home_page.monitors_menu.click()

    def click_on_the_product_with_the_highest_price_on_the_page(self):
        self.wait.until(expected_conditions.visibility_of(self.home_page.get_list_of_products))
        products = self.home_page.get_list_of_products()
        products_prices = {}
        list(map(lambda x:
                 products_prices.setdefault(x,
                                            list(map(int, re.findall(r'\d+', x.find_element(By.TAG_NAME, "h5").text)))[
                                                0])
                 , products))
        highest_price_product = max(products_prices, key=products_prices.get)

        self.DATA_CASH.setdefault("PRODUCT_PRICE", products_prices[highest_price_product])
        self.DATA_CASH.setdefault("PRODUCT_NAME", highest_price_product.find_element(By.CLASS_NAME, 'card-title').text)

        highest_price_product.click()

    def get_highest_price_product_name(self):
        return self.DATA_CASH["PRODUCT_NAME"]

    def get_highest_price_product_price(self):
        return self.DATA_CASH["PRODUCT_PRICE"]

    def products_page_with_is_open(self, name, price):
        return self.product_page.pr_name.is_displayed() and \
               self.product_page.pr_price.is_displayed() and \
               self.product_page.pr_name.text == name and \
               list(map(int, re.findall(r'\d+', self.product_page.pr_price.text)))[0] == price

    def click_on_add_to_cart_button(self):
        self.product_page.add_to_cart_button.click()
        self.wait.until(expected_conditions.alert_is_present())
        self.chromedriver.switch_to.alert.accept()

    def click_on_cart_button(self):
        self.product_page.cart_link.click()

    def product_is_successfully_added_to_cart(self):
        self.wait.until(expected_conditions.visibility_of(self.cart_page.get_products))
        return len(self.cart_page.get_products()) > 0

    def get_product_name_text(self):
        return self.cart_page.get_products()[0].pr_name.text

    def get_product_price_text(self):
        return int(self.cart_page.get_products()[0].pr_price.text)

    def clean_cart(self):
        self.click_on_cart_button()
        self.wait.until(expected_conditions.element_to_be_selected(self.cart_page.get_products))
        self.cart_page.get_products()[0].delete.click()
        self.wait.until(expected_conditions.element_to_be_selected(self.cart_page.get_products))
