import allure
from playwright.sync_api import Page
from pages.base_page import BasePage, BASE_URL


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    __EMPTY_MESSAGE = ".main-cart__empty-message"
    __CART_CONTENT = "main"

    @allure.step("Open the cart page")
    def open_cart(self):
        self.open("/cart")

    @allure.step("Ask the shop how many items are in the cart")
    def get_item_count(self):
        response = self.page.request.get(BASE_URL + "/cart.js")
        count = response.json()["item_count"]
        self.add_log("Items in cart", count)
        return count

    @allure.step("Wait until the cart has an item (up to 10 seconds)")
    def wait_for_item(self):
        count = self.get_item_count()
        for i in range(10):
            if count == 0:
                self.page.wait_for_timeout(1000)
                count = self.get_item_count()
        return count

    def get_empty_message(self):
        return self.get_text(self.__EMPTY_MESSAGE)

    def get_cart_text(self):
        return self.get_text(self.__CART_CONTENT)
