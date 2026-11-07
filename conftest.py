import os
import platform
import pytest
from pages.brewdog_page import BASE_URL
from pages.collection_page import CollectionPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.screen_marks import show_test_banner, pause_after_test


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1366, "height": 680}, "locale": "en-US", "timezone_id": "America/New_York"}


@pytest.fixture(scope="session", autouse=True)
def write_environment_file(browser):
    run_on = "My computer"
    if os.getenv("CI") == "true":
        run_on = "GitHub Actions"
    file = open("allure-results/environment.properties", "w")
    file.write("Website=BrewDog USA\n")
    file.write("Start_URL=" + BASE_URL + "\n")
    file.write("Browser=" + browser.browser_type.name + "\n")
    file.write("Browser_version=" + browser.version + "\n")
    file.write("Python_version=" + platform.python_version() + "\n")
    file.write("Operating_system=" + platform.system() + "\n")
    file.write("Run_on=" + run_on + "\n")
    file.close()


@pytest.fixture(autouse=True)
def show_test_info(page, request):
    show_test_banner(page, request)
    yield
    pause_after_test(page)


@pytest.fixture
def open_home(page):
    home_page = HomePage(page)
    home_page.open_home()


@pytest.fixture
def buyable_product(page):
    collection_page = CollectionPage(page)
    collection_page.open_category("non-alcoholics")
    product_page = ProductPage(page)
    for path in collection_page.get_product_paths():
        product_page.open_product(path)
        if product_page.can_be_bought():
            return product_page
    pytest.fail("No product that can be bought was found in non-alcoholics")
