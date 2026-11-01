import allure
import pytest
from pages.cart_page import CartPage


@allure.epic("Buy a product")
@allure.feature("Cart")
class TestCart:

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Empty cart")
    @allure.title("N-2: New visitor's cart is empty")
    @allure.description("Open the cart as a new visitor and check it has no items and shows the empty message.")
    def test_new_visitor_cart_is_empty(self, page):
        cart_page = CartPage(page)
        cart_page.open_cart()
        assert cart_page.get_item_count() == 0
        assert "empty" in cart_page.get_empty_message().lower()

    @pytest.mark.regression
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Add to cart")
    @allure.title("T164-3: Adding an in-stock product puts it in the cart")
    @allure.description("Open an in-stock product, click Add to basket and check the cart count goes up.")
    def test_add_product_to_cart(self, page, buyable_product):
        cart_page = CartPage(page)
        assert cart_page.get_item_count() == 0

        buyable_product.add_to_basket()
        assert cart_page.wait_for_item() >= 1

    @pytest.mark.regression
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Cart page")
    @allure.title("T164-4: Added product appears on the cart page")
    @allure.description("Add an in-stock product, open the cart page and check the product is listed by name.")
    def test_added_product_appears_on_cart_page(self, page, buyable_product):
        product_name = buyable_product.get_title()
        buyable_product.add_to_basket()

        cart_page = CartPage(page)
        cart_page.wait_for_item()
        cart_page.open_cart()
        assert product_name.lower() in cart_page.get_cart_text().lower()
