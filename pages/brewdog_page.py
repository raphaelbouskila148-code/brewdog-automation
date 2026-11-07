import allure
import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.screen_marks import show_note

BASE_URL = "https://usa.brewdog.com"


class BrewDogPage(BasePage):
    """Everything that belongs to the BrewDog site itself: the address, the
    age popup, the header search box and the check for the site blocking us.

    It inherits all the plain Playwright commands from BasePage, and every
    page object in this project inherits from this class.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.status_code = 0

    __SEARCH_BOX = "input[name='q']:visible >> nth=0"
    __SITE_BLOCK = "iframe[src*='challenges.cloudflare.com'], body:has-text('needs to be verified'), body:has-text('check your connection')"
    __AGE_CONFIRM_BTN = "uwp-age-gate button:has-text('Confirm')"

    @allure.step("Check if the site is blocking this visit")
    def is_site_blocking_us(self):
        if self.page.locator(self.__SITE_BLOCK).count() == 0:
            return False
        show_note(self.page, "The site may be blocking this visit. Waiting 10 seconds...", 10)
        self.page.wait_for_timeout(10000)
        return self.page.locator(self.__SITE_BLOCK).count() > 0

    def skip_if_site_blocks_us(self):
        if self.is_site_blocking_us():
            self.add_log("Blocked by the site", "The site asked to verify the visitor is human, or refused the request, so this test was skipped")
            pytest.skip("The site is blocking automated visits from this computer")

    def wait_for(self, locator):
        """Same as BasePage.wait_for, but if the wait fails it first checks
        whether the site is blocking us, so the test is skipped instead of
        failing for a reason that is not a real defect."""
        try:
            super().wait_for(locator)
        except Exception:
            self.skip_if_site_blocks_us()
            raise

    @allure.step("Go to {path}")
    def open_without_age_check(self, path):
        response = self.go_to(BASE_URL + path)
        self.status_code = response.status
        self.add_log("Opened page", BASE_URL + path + " (status code " + str(response.status) + ")")
        self.skip_if_site_blocks_us()

    def open(self, path):
        self.open_without_age_check(path)
        self.confirm_age()

    @allure.step("Confirm the age if the age popup is shown")
    def confirm_age(self):
        if self.page.locator(self.__AGE_CONFIRM_BTN).is_visible():
            self.click(self.__AGE_CONFIRM_BTN)

    @allure.step("Check if the age popup is shown")
    def is_age_gate_visible(self):
        show_note(self.page, "Waiting 2 seconds to see if the age popup appears...", 2)
        self.page.wait_for_timeout(2000)
        return self.is_visible(self.__AGE_CONFIRM_BTN)

    @allure.step("Search for {text} in the header search box")
    def search(self, text):
        self.click(self.__SEARCH_BOX)
        self.fill_text(self.__SEARCH_BOX, text)
        self.press_enter(self.__SEARCH_BOX)
