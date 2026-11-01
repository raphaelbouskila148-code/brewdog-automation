import allure
import pytest


@allure.epic("Browse the store")
@allure.feature("Product page")
class TestProduct:

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Product details")
    @allure.title("T164-1: Product page shows the product name")
    @allure.description("Open an in-stock product and check its name is shown.")
    def test_product_page_shows_name(self, buyable_product):
        assert buyable_product.get_title() != ""

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Product details")
    @allure.title("T226: Product page shows a price in USD")
    @allure.description("Open an in-stock product and check a price in US dollars is shown.")
    def test_product_page_shows_price_in_dollars(self, buyable_product):
        assert "$" in buyable_product.get_price()

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Add to basket button")
    @allure.title("T164-2: In-stock product has an enabled Add to basket button")
    @allure.description("Open an in-stock product and check the Add to basket button is visible and enabled.")
    def test_product_page_has_add_to_basket_button(self, buyable_product):
        assert buyable_product.is_add_to_basket_visible()
        assert buyable_product.is_add_to_basket_enabled()
        assert "Add to basket" in buyable_product.get_add_to_basket_text()
