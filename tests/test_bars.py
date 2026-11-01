import allure
import pytest
from data_provider import get_data
from pages.bar_locator_page import BarLocatorPage


@allure.epic("Store settings and locations")
@allure.feature("Bar locator")
class TestBars:

    @pytest.mark.regression
    @pytest.mark.parametrize("test_id, city", get_data("cities"))
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Bar search")
    @allure.title("{test_id}: Searching '{city}' lists that city's bar")
    @allure.description("Type a city in the bar search and check that city's bar is in the results.")
    def test_bar_search_lists_bars(self, page, test_id, city):
        bar_locator_page = BarLocatorPage(page)
        bar_locator_page.open_bar_locator()
        bar_locator_page.search(city)
        assert bar_locator_page.has_bar_in_city(city)

    @pytest.mark.regression
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("No bars message")
    @allure.title("N-5: Searching a city with no bar shows a message")
    @allure.description("Type a place with no BrewDog bar and check the 'No bars found' message is shown.")
    def test_bar_search_with_no_match_shows_message(self, page):
        bar_locator_page = BarLocatorPage(page)
        bar_locator_page.open_bar_locator()
        bar_locator_page.search("zzqxnowhere")
        assert "No bars found" in bar_locator_page.get_empty_message()
