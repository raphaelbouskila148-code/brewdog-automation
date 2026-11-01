import allure
import pytest
from data_provider import get_data
from pages.region_selector import RegionSelector


@allure.epic("Store settings and locations")
@allure.feature("Region settings")
class TestRegion:

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Default region")
    @allure.title("T329-1: United States is the selected region")
    @allure.description("On the US store, check the footer country selector has US selected.")
    def test_united_states_is_selected(self, page, open_home):
        region_selector = RegionSelector(page)
        assert region_selector.get_selected_country() == "us"

    @pytest.mark.regression
    @pytest.mark.parametrize("test_id, country, store", get_data("countries"))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Change region")
    @allure.title("{test_id}: Choosing {country} opens the {store} store")
    @allure.description("Choose another country in the footer selector and check the matching BrewDog store opens.")
    def test_changing_region_opens_that_store(self, page, open_home, test_id, country, store):
        region_selector = RegionSelector(page)
        region_selector.choose_country(country)
        assert "usa.brewdog.com" not in region_selector.url
        assert store in region_selector.url
