import allure
from playwright.sync_api import Page
from pages.screen_marks import highlight, show_note, ORANGE, BLUE, GREEN


class BasePage:
    """Plain Playwright commands.

    Nothing in this file knows which website is being tested, so the whole
    file can be copied into another project and used as it is.
    Everything that belongs to the BrewDog site lives in brewdog_page.py,
    which inherits from this class.
    """

    def __init__(self, page: Page):
        self.page = page

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

    @allure.step("Go to {address}")
    def go_to(self, address):
        show_note(self.page, "Opening " + address + " ...", 8)
        return self.page.goto(address)

    def add_log(self, name, text):
        allure.attach(str(text), name=name, attachment_type=allure.attachment_type.TEXT)
        show_note(self.page, name + ": " + str(text))

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
