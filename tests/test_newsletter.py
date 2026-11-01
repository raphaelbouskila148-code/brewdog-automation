import allure
import pytest
from pages.newsletter_form import NewsletterForm


@allure.epic("Customer account")
@allure.feature("Newsletter form")
class TestNewsletter:

    @pytest.mark.smoke
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Form fields")
    @allure.title("T331-1: Newsletter form shows First Name, Email and Join button")
    @allure.description("Check the homepage newsletter form has a First Name field, an Email field and a Join Free Now button.")
    def test_newsletter_form_has_fields(self, page, open_home):
        newsletter_form = NewsletterForm(page)
        assert newsletter_form.is_first_name_visible()
        assert newsletter_form.is_email_visible()
        assert newsletter_form.is_join_button_visible()

    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Form validation")
    @allure.title("T331-2: Invalid email is not accepted")
    @allure.description("Fill a name and an email without '@', click Join and check the form is not sent.")
    def test_invalid_email_is_not_accepted(self, page, open_home):
        newsletter_form = NewsletterForm(page)
        newsletter_form.fill_form("Raphael", "notanemail")
        assert newsletter_form.get_email_message() != ""
        assert "/contact" not in newsletter_form.url

    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Form validation")
    @allure.title("T331-3: Empty required fields are not accepted")
    @allure.description("Click Join with both fields empty and check the form is not sent.")
    def test_empty_fields_are_not_accepted(self, page, open_home):
        newsletter_form = NewsletterForm(page)
        newsletter_form.fill_form("", "")
        assert newsletter_form.get_first_name_message() != ""
        assert newsletter_form.get_email_message() != ""
        assert "/contact" not in newsletter_form.url
