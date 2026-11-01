import allure
import pytest
from pages.collection_page import CollectionPage
from pages.home_page import HomePage


@allure.epic("Browse the store")
@allure.feature("Mobile")
class TestMobile:

    @pytest.mark.mobile
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Fits the phone screen")
    @allure.title("N-3: Homepage fits a mobile screen")
    @allure.description("On a phone-sized screen (390 x 680), check the homepage has no sideways scrolling.")
    def test_homepage_fits_mobile_screen(self, page):
        home_page = HomePage(page)
        home_page.set_phone_screen()
        home_page.open_home()
        assert home_page.fits_screen()

    @pytest.mark.mobile
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Fits the phone screen")
    @allure.title("N-4: Category page works on mobile")
    @allure.description("On a phone-sized screen (390 x 680), check the Beer category lists products and fits the screen.")
    def test_collection_page_works_on_mobile(self, page):
        collection_page = CollectionPage(page)
        collection_page.set_phone_screen()
        collection_page.open_category("beer")
        assert collection_page.get_products_count() > 0
        assert collection_page.fits_screen()
