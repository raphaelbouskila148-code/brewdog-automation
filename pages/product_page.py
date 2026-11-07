import allure
from playwright.sync_api import Page
from pages.brewdog_page import BrewDogPage
from pages.screen_marks import show_note


class ProductPage(BrewDogPage):
    def __init__(self, page: Page):
        super().__init__(page)

    __TITLE = ".product-details__title >> nth=0"
    __PRICE = ".product-swatches__price__value >> nth=0"
    __ADD_TO_BASKET_BTN = ".product__atc-button >> nth=0"
    __PLUS_BTN = "main button[aria-label='Increase quantity'] >> nth=0"

    @allure.step("Open the product {path}")
    def open_product(self, path):
        self.open(path)

    def get_title(self):
        return self.get_text(self.__TITLE)

    def get_price(self):
        return self.get_text(self.__PRICE)

    def get_add_to_basket_text(self):
        return self.get_text(self.__ADD_TO_BASKET_BTN)

    def is_add_to_basket_visible(self):
        return self.is_visible(self.__ADD_TO_BASKET_BTN)

    def is_add_to_basket_enabled(self):
        return self.is_enabled(self.__ADD_TO_BASKET_BTN)

    @allure.step("Check if this product can be bought")
    def can_be_bought(self):
        self.page.wait_for_timeout(2000)
        button = self.page.locator(self.__ADD_TO_BASKET_BTN)
        can_buy = button.is_visible() and button.is_enabled()
        if can_buy:
            show_note(self.page, "This product is in stock. The test will use it.")
        else:
            show_note(self.page, "This product is sold out. Trying the next one...")
        return can_buy

    @allure.step("Choose 1 item with the + button and click Add to basket")
    def add_to_basket(self):
        if self.page.locator(self.__PLUS_BTN).is_visible():
            self.click(self.__PLUS_BTN)
        self.click(self.__ADD_TO_BASKET_BTN)
