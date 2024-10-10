import pytest

# enables proper handling of async functions, ensuring that they run in an event loop
# event loop is responsible for executing asynchronous code, coordinating the execution of multiple tasks, and managing the overall flow of an application

# open landing page and assure it is opened
@pytest.mark.asyncio 
async def test_open_start_page(setup_page):  # as an input it uses 'setup_page' fixture, which in its turn uses 'browser' fixture
    page = setup_page                        # get object from fixture
    assert page.url == 'https://symonstorozhenko.wixsite.com/website-1'  # compare if actual result  == expected. So, the landing page is opened

# do click on 'Contact Us' link
@pytest.mark.asyncio
async def contact_us_verification(setup_page):
    page = setup_page  
    locator = page.get_by_text(text_contact_us)  
    text_content = await locator.text_content()
    assert text_content == validate_text_contact_us, f"Text did not match: {text_content}"

# fill in parameters, click 'Submit' button and check request was submitted (UI level)
@pytest.mark.asyncio
async def test_submit_form(submit_contact_us_form):
    page = submit_contact_us_form

    # Wait for the confirmation message to appear after submitting the form
    try:
        confirmation_message_locator = await page.wait_for_selector("div#comp-kqx72xe4", timeout=5000, state='visible')
        assert await confirmation_message_locator.is_visible(), "Confirmation message not visible"

        # Get the text and validate it
        confirmation_text = await confirmation_message_locator.inner_text()
        assert "Thanks for submitting!" in confirmation_text, "Confirmation message not as expected"
        print("Form submission message detected.")
        
    except TimeoutError:
        print("Confirmation message not found after CAPTCHA solving.")
        raise AssertionError("Confirmation message not visible after CAPTCHA was solved")