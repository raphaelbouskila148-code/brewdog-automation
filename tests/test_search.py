import allure
import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage


@allure.epic("Browse the store")
@allure.feature("Search")
class TestSearch:

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Search from the header")
    @allure.title("T297: Search box returns products for 'IPA'")
    @allure.description("Type IPA in the header search box, press Enter and check product results are shown.")
    def test_search_box_returns_products_for_ipa(self, page, open_home):
        home_page = HomePage(page)
        home_page.search("IPA")

        search_page = SearchPage(page)
        assert "ipa" in search_page.get_heading().lower()
        assert search_page.get_products_count() > 0

    @pytest.mark.regression
    @pytest.mark.xfail(reason="Known bug: a search with no matches shows unrelated products and no 'no results' message")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("No results message")
    @allure.title("T298: No-match search tells the user nothing was found")
    @allure.description("Search for a word that matches nothing and check a 'no results' message is shown. Known bug.")
    def test_search_with_no_matches_tells_user(self, page):
        search_page = SearchPage(page)
        search_page.open_search("zzqxnotarealbeer")
        search_page.add_log("Page address", search_page.url)
        assert "no results" in search_page.get_no_results_message().lower()
