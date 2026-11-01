import allure
import pytest
from playwright.sync_api import Page
from pages.screen_marks import highlight, show_note, ORANGE, BLUE, GREEN

BASE_URL = "https://usa.brewdog.com"


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.status_code = 0

    __SEARCH_BOX = "input[name='q']:visible >> nth=0"
    __ROBOT_CHECK = "text=Verify you are human"
    __AGE_CONFIRM_BTN = "uwp-age-gate button:has-text('Confirm')"

    @property
    def url(self):
        return self.page.url

    @property
    def title(self):
        return self.page.title()

    @allure.step("Click on {locator}")
    def click(self, locator):
        highlight(self.page, locator, "CLICK", ORANGE)
        self.page.locator(locator).click()

    @allure.step("Type '{text}' in {locator}")
    def fill_text(self, locator, text):
        highlight(self.page, locator, "TYPE: '" + text + "'", BLUE)
        self.page.locator(locator).fill(text)

    @allure.step("Choose '{value}' in {locator}")
    def select_option(self, locator, value):
        highlight(self.page, locator, "CHOOSE: " + value, BLUE)
        self.page.locator(locator).select_option(value)

    @allure.step("Press Enter in {locator}")
    def press_enter(self, locator):
        highlight(self.page, locator, "PRESS: Enter", ORANGE)
        self.page.locator(locator).press("Enter")

    @allure.step("Read the text of {locator}")
    def get_text(self, locator):
        highlight(self.page, locator, "READ THE TEXT", GREEN)
        text = self.page.locator(locator).inner_text()
        self.add_log("Text found", text)
        return text

    @allure.step("Read all the texts of {locator}")
    def get_all_texts(self, locator):
        highlight(self.page, locator, "READ ALL THE TEXTS", GREEN, 30)
        texts = self.page.locator(locator).all_inner_texts()
        self.add_log("Texts found", texts)
        return texts

    @allure.step("Read the {name} of {locator}")
    def get_attribute(self, locator, name):
        highlight(self.page, locator, "READ: " + name, GREEN)
        value = self.page.locator(locator).get_attribute(name)
        self.add_log("Value of " + name, value)
        return value

    @allure.step("Read the chosen value of {locator}")
    def get_value(self, locator):
        highlight(self.page, locator, "READ THE CHOSEN VALUE", GREEN)
        value = self.page.locator(locator).input_value()
        self.add_log("Chosen value", value)
        return value

    @allure.step("Count the elements of {locator}")
    def count(self, locator):
        number = self.page.locator(locator).count()
        highlight(self.page, locator, "COUNT: " + str(number) + " FOUND", GREEN, 30)
        return number

    @allure.step("Check if {locator} is shown")
    def is_visible(self, locator):
        highlight(self.page, locator, "CHECK: IS IT SHOWN?", GREEN)
        return self.page.locator(locator).is_visible()

    @allure.step("Check if {locator} is enabled")
    def is_enabled(self, locator):
        highlight(self.page, locator, "CHECK: IS IT ENABLED?", GREEN)
        return self.page.locator(locator).is_enabled()

    @allure.step("Wait until {locator} is shown")
    def wait_for(self, locator):
        if not self.page.locator(locator).is_visible():
            show_note(self.page, "Waiting up to 15 seconds for the element to appear...", 15)
        self.page.locator(locator).wait_for(timeout=15000)

    def add_log(self, name, text):
        allure.attach(str(text), name=name, attachment_type=allure.attachment_type.TEXT)
        show_note(self.page, name + ": " + str(text))

    @allure.step("Check if the site is showing its robot check")
    def is_robot_check_shown(self):
        if not self.page.locator(self.__ROBOT_CHECK).is_visible():
            return False
        show_note(self.page, "The site is showing a robot check. Waiting 5 seconds...", 5)
        self.page.wait_for_timeout(5000)
        return self.page.locator(self.__ROBOT_CHECK).is_visible()

    def skip_if_robot_check(self):
        if self.is_robot_check_shown():
            self.add_log("Robot check", "The site asked to verify the visitor is human, so this test was skipped")
            pytest.skip("The site's robot check is blocking automated visits from this computer")

    @allure.step("Go to {path}")
    def open_without_age_check(self, path):
        show_note(self.page, "Opening " + BASE_URL + path + " ...", 8)
        response = self.page.goto(BASE_URL + path)
        self.status_code = response.status
        self.add_log("Opened page", BASE_URL + path + " (status code " + str(response.status) + ")")
        self.skip_if_robot_check()

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

    @allure.step("Make the browser window phone sized (390 x 680)")
    def set_phone_screen(self):
        self.page.set_viewport_size({"width": 390, "height": 680})
        show_note(self.page, "The window is now phone sized: 390 x 680")

    @allure.step("Check that the page is not wider than the screen")
    def fits_screen(self):
        show_note(self.page, "CHECK: is the page wider than the screen? (sideways scrolling)")
        page_width = self.page.evaluate("document.documentElement.scrollWidth")
        screen_width = self.page.evaluate("window.innerWidth")
        self.add_log("Page width and screen width", str(page_width) + " and " + str(screen_width))
        return page_width <= screen_width + 1
