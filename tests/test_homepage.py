import allure
import pytest
from pages.home_page import HomePage


@allure.epic("Browse the store")
@allure.feature("Homepage")
class TestHomepage:

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Homepage opens")
    @allure.title("N-1: Homepage loads with the BrewDog title")
    @allure.description("Open the homepage and check it loads and the browser tab title contains BrewDog.")
    def test_homepage_loads_with_correct_title(self, page):
        home_page = HomePage(page)
        home_page.open_home()
        home_page.add_log("Page title", home_page.title)
        assert home_page.status_code == 200
        assert "BrewDog" in home_page.title

    @pytest.mark.regression
    @pytest.mark.xfail(reason="Known bug: the age gate is switched off on the live site")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Age gate")
    @allure.title("T267: Age gate is shown to a first-time visitor")
    @allure.description("A new visitor must confirm their age before browsing an alcohol retailer. Known bug: the gate is off.")
    def test_age_gate_is_shown_to_new_visitors(self, page):
        home_page = HomePage(page)
        home_page.open_home_without_age_check()
        assert home_page.is_age_gate_visible()
