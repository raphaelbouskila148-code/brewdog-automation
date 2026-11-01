import allure
import pytest
from data_provider import get_data
from pages.home_page import HomePage


@allure.epic("Browse the store")
@allure.feature("Footer")
class TestFooter:

    @pytest.mark.smoke
    @pytest.mark.parametrize("test_id, link_text, expected_path", get_data("footer_links"))
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Footer links")
    @allure.title("{test_id}: Footer link '{link_text}' points to the right page")
    @allure.description("Find a footer link and check its address points to the right page.")
    def test_footer_link_points_to_correct_page(self, page, open_home, test_id, link_text, expected_path):
        home_page = HomePage(page)
        assert expected_path in home_page.get_footer_link_address(link_text)
