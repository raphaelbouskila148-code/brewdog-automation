# BrewDog USA – Test Automation Framework

![BrewDog Tests](https://github.com/raphaelbouskila148-code/brewdog-automation/actions/workflows/tests.yml/badge.svg)

Automated UI tests for the [BrewDog USA](https://usa.brewdog.com) e-commerce site, written in **Python** with **Playwright** and **pytest**, using the **Page Object Model**, with **Allure** reports and **GitHub Actions** CI.

This project continues my manual testing of the same site: I executed 246 test cases in TestRail and reported 72 bugs in the [BrewDog STR report](https://raphaelbouskila148-code.github.io/raphael-QA-HTML1/brewdog-str.pdf). The automated scenarios are documented in the STD (`docs/BrewDog_STD.xlsx`) before being automated.

---

## Test plan (STD)

`docs/BrewDog_STD.xlsx` lists all 37 test cases with preconditions, steps, expected result, test data, priority, the test function that runs each one and the exact command to run it.

Test IDs are the case numbers of my TestRail run R14 (the STR report): for example `T113` is the manual case "Click on the Beer option and verify it sends me to all the beers", and the test automates it. A suffix (`T304-1`, `T304-2`) means several automated tests cover one manual case, and `N-1` to `N-5` are new tests that have no manual case. The column "STR case" in the STD shows the matching TestRail number.

## What is tested

37 tests in 11 test classes. DDT (`@pytest.mark.parametrize`) runs the same test with different data, and the data comes from a data provider (`data_provider.py` reads `data/test_data.json`).

| Class | File | Tests | What is checked |
|---|---|---|---|
| `TestHomepage` | `test_homepage.py` | 2 | Page loads; age-confirmation popup is shown to a first-time visitor |
| `TestShop` | `test_shop.py` | 7 | Each of 6 shop categories lists products (DDT); clicking a product opens it |
| `TestProduct` | `test_product.py` | 3 | In-stock product shows name, USD price and an enabled "Add to basket" |
| `TestSearch` | `test_search.py` | 2 | Search box returns products; no-match message |
| `TestCart` | `test_cart.py` | 3 | New cart is empty; adding a product updates the cart and cart page |
| `TestFooter` | `test_footer.py` | 4 | Shipping, Contact, Terms and Privacy links (DDT) |
| `TestMobile` | `test_mobile.py` | 2 | Homepage and category fit a phone-sized screen (390 x 680) |
| `TestLogin` | `test_login.py` | 5 | Sign-in page opens; empty and invalid emails are rejected (DDT) |
| `TestNewsletter` | `test_newsletter.py` | 3 | Signup form fields; invalid and empty input is not accepted |
| `TestRegion` | `test_region.py` | 3 | US is selected; choosing another country opens that store (DDT) |
| `TestBars` | `test_bars.py` | 3 | Bar search finds bars by city (DDT); no-match message |

Tests are also tagged by type: `smoke`, `regression`, `mobile`.

> The tests never place an order, never send a real email and never subscribe anyone to the newsletter.

## What the Allure report shows

- **Behaviors tab:** tests grouped as epic > feature > story (`@allure.epic`, `@allure.feature`, `@allure.story`). Four epics: Browse the store, Buy a product, Customer account, Store settings and locations.
- **Severity:** every test has `@allure.severity` (critical, normal or minor). It follows the Priority column in the STD: High = critical, Medium = normal, Low = minor.
- **Steps:** every action and every read in the page objects is a step (`@allure.step`), so each test shows what the browser did, in order.
- **Logs:** important values are attached as text (`allure.attach`, wrapped in `add_log` in `base_page.py`), for example the page title, a product name and price, a link address, the cart count or the browser's validation message.
- **Environment:** the dashboard lists the website, start URL, browser and its version, Python version, operating system and where the run happened. `conftest.py` writes it to `allure-results/environment.properties` at the start of every run.

## What you see in the browser

When the tests run with a visible browser window (the default, `--headed`), the page marks what the test is doing, so someone watching, or a screen recording, can follow without reading any code:

- **A coloured box with a label** around the element the test uses: orange for clicks and key presses, blue for typing and choosing, green for reading and checking (`CLICK`, `TYPE: 'IPA'`, `READ THE TEXT`, `COUNT: 3 FOUND`, `CHECK: IS IT SHOWN?`).
- **A bar at the bottom** with the test name and what it checks (taken from `@allure.title` and `@allure.description`).
- **Small notes** with what the test found, the same values that go to the Allure logs.

It is drawn by `pages/screen_marks.py` and called from `base_page.py` and `conftest.py`. It is switched off in headless runs and on GitHub Actions.

## Known issues found by the automation

Tests for known site bugs are marked **xfail** (expected to fail): they show as known issues in every report without turning the pipeline red, and will show as **XPASS** once BrewDog fixes them.

| Issue | Test |
|---|---|
| A search with no matches shows unrelated products and no "no results" message | T298 |
| The age-confirmation gate is switched off, so visitors are never asked their age | T267 |

## Project structure

```
brewdog-automation/
├── .github/workflows/tests.yml   # CI: runs all browsers, publishes the Allure report
├── docs/BrewDog_STD.xlsx         # Test plan (STD)
├── data/test_data.json           # Test data for the DDT tests (one list per line)
├── pages/                        # Page objects (POM) and screen_marks.py (the boxes and labels shown in the browser)
├── tests/                        # Test classes, one file per area
├── conftest.py                   # Shared fixtures (browser settings, open home, product to buy) and the Allure environment file
├── data_provider.py              # Reads the test data file for the DDT tests
├── pytest.ini                    # Test settings, markers, report options
└── requirements.txt
```

## Running the tests

```bash
pip install -r requirements.txt
playwright install

pytest                         # all tests, Chromium window you can watch (slow motion, set in pytest.ini)
pytest -m smoke                # quick smoke tests only
pytest tests/test_login.py     # one test file
pytest --browser firefox       # another browser
pytest -o addopts="--alluredir=allure-results"   # no browser window, faster (this is what GitHub does)
```

Each run saves an HTML report in `reports/report.html` and Allure results in `allure-results/`.
On failure, a screenshot, video and Playwright trace are saved in `test-results/`.

### Allure report

```bash
allure serve allure-results
```

On Windows, `allure_report.bat` (temporary report) and `allure_save_report.bat` (saved as `allure-report/index.html`) do the same using a local Java + Allure copy.

## CI (GitHub Actions)

Runs on every push, every pull request, weekly, and on demand, in Chromium, Firefox and WebKit in parallel. The Allure report from the Chromium run is published to GitHub Pages.
