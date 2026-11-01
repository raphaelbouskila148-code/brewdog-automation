import allure
import pytest
from data_provider import get_data
from pages.login_page import LoginPage


@allure.epic("Customer account")
@allure.feature("Login")
class TestLogin:

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Sign-in page")
    @allure.title("T304-1: Login page opens with an email field and Continue button")
    @allure.description("Open the account page and check the sign-in form shows an Email field and a Continue button.")
    def test_login_page_opens(self, page):
        login_page = LoginPage(page)
        login_page.open_login()
        assert login_page.is_email_field_visible()
        assert login_page.is_continue_button_visible()

    @pytest.mark.regression
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Email validation")
    @allure.title("T304-2: Empty email shows an error")
    @allure.description("Click Continue without an email and check the 'Enter a valid email address' error is shown.")
    def test_empty_email_shows_error(self, page):
        login_page = LoginPage(page)
        login_page.open_login()
        login_page.submit_email("")
        assert "Enter a valid email address" in login_page.get_error()

    @pytest.mark.regression
    @pytest.mark.parametrize("test_id, email", get_data("invalid_emails"))
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Email validation")
    @allure.title("{test_id}: Invalid email '{email}' is rejected")
    @allure.description("Enter a badly formatted email, click Continue and check an error is shown.")
    def test_invalid_email_is_rejected(self, page, test_id, email):
        login_page = LoginPage(page)
        login_page.open_login()
        login_page.submit_email(email)
        assert "Enter a valid email address" in login_page.get_error()
