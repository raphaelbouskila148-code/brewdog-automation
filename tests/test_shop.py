import allure
import pytest
from data_provider import get_data
from pages.collection_page import CollectionPage
from pages.product_page import ProductPage


@allure.epic("Browse the store")
@allure.feature("Shop categories")
class TestShop:

    @pytest.mark.smoke
    @pytest.mark.parametrize("test_id, handle", get_data("categories"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Category lists products")
    @allure.title("{test_id}: Category '{handle}' lists products")
    @allure.description("Open a shop category and check it loads and shows at least one product.")
    def test_collection_page_lists_products(self, page, test_id, handle):
        collection_page = CollectionPage(page)
        collection_page.open_category(handle)
        assert collection_page.status_code == 200
        assert collection_page.get_products_count() > 0

    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Open a product")
    @allure.title("T163: Clicking a product opens its product page")
    @allure.description("Open the Beer category, click the first product and check its page opens.")
    def test_clicking_a_product_opens_its_page(self, page):
        collection_page = CollectionPage(page)
        collection_page.open_category("beer")
        collection_page.open_first_product()

        product_page = ProductPage(page)
        assert product_page.get_title() != ""
        assert "/products/" in product_page.url
        product_page.add_log("Product page address", product_page.url)
