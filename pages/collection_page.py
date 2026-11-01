import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class CollectionPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    __PRODUCT_LINK = "main a[href*='/products/']"
    __FIRST_PRODUCT = "main a[href*='/products/'] >> nth=0"

    @allure.step("Open the category {handle}")
    def open_category(self, handle):
        self.open("/collections/" + handle)

    @allure.step("Count the products on the page")
    def get_products_count(self):
        self.wait_for(self.__FIRST_PRODUCT)
        count = self.count(self.__PRODUCT_LINK)
        self.add_log("Product links found", count)
        return count

    @allure.step("Click the first product")
    def open_first_product(self):
        self.click(self.__FIRST_PRODUCT)
        self.page.wait_for_url("**/products/**")

    @allure.step("Collect the addresses of the products")
    def get_product_paths(self):
        self.wait_for(self.__FIRST_PRODUCT)
        paths = []
        for link in self.page.locator(self.__PRODUCT_LINK).all():
            path = link.get_attribute("href").split("?")[0]
            if path not in paths:
                paths.append(path)
        self.add_log("Product addresses", paths)
        return paths
