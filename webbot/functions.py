"""
Helper functions for the Google Photos (GP) webbot.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep, time


# Check if a given url is an album.
def is_album_url(url):
    if "https://photos.google.com/album/" not in url:
        raise UserWarning(f"The following url is not an GP album:\n{url}")

# Check if a given url is a photo.
def is_photo_url(url):
    if "https://photos.google.com/photo/" not in url:
        raise UserWarning(f"The following url is not an GP photo:\n{url}")

# --------------------------------------------------------------------------- #
# Open a chrome webdriver session.
def init_driver():

    # WebDriver options.
    options = webdriver.ChromeOptions()
    # Allow GP login.
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Remove superflous user interaction.
    options.add_argument("--disable-search-engine-choice-screen")
    print("Get correct argument for default english lang")
    options.add_argument("--default-lang=en-GB")

    # Start webdriver.
    driver = webdriver.Chrome(options=options)

    return driver

def close_driver(driver):
    driver.quit()

# --------------------------------------------------------------------------- #
# Load the GP's albums page.
def goto_albums(driver):
    driver.get("https://photos.google.com/albums")

# Get ID of selected album.
def get_selected_album(driver):

    url = driver.current_url

    if is_album_url(url):
        # Album url: "https://photos.google.com/album/AlbumIDHere/".
        album_id = url.replace("https://photos.google.com/album/", "")
        album_id = album_id.replace("/", "")
        return album_id
    else:
        # An album wasn't selected in the webdriver.
        return None

# Load the 
def goto_photo(driver, img_url):
    # Exit if url is not a GP photo.
    status = is_photo_url(img_url)

    driver.get(img_url)

    # Img with access forbiden.
    if "lh3.googleusercontent.com" in driver.current_url:
        raise UserWarning("You don't have access to the image:"
                          f"\n{img_url}\n"
                          "Are you connected with the right google account in the browser?")

# --------------------------------------------------------------------------- #
# Wait until an Xpath element is available of the timer runs out.
def wait_xpath(driver, xpath, timeout=5, poll_interval=0.5):
    # timeout in s, poll_interval in s.

    start = time()

    # Test element until timeout is reached.
    while time() - start < timeout:
        try:
            # Fetch element.
            element = driver.find_element(By.XPATH, xpath)
            if element.is_displayed() and element.is_enabled():
                return element
        # The element doesn't exists.
        except NoSuchElementException:
            pass
        sleep(poll_interval)

    # Xpath search timed out !
    raise UserWarning(f"After {timeout}s, the search was abandoned for the button at (XPaht):"
                      f"\n{xpaht}\n")


# Use GP web UI to add img an image to an album.
def add_to_album(driver, img_url, album_id):
    """
    On GP's web UI the current image can be put in an album by clicking:
    More options (3 dots) > Add to album (4th option) > select album in the popup
    """

    # Load image webpage.
    goto_photo(driver, img_url)

    # ActionChains for the move_to_element method.
    action = ActionChains(driver)

    # "More options" button.
    more_options_xpath = '//div[@aria-label="More options"][@__is_owner="true"]'#"/html/body/div[1]/div/c-wiz/div[4]/c-wiz/div[1]/div[2]/div[2]/span/div/div[10]/div"
    more_option_elem = wait_xpath(driver, more_options_xpath, 5, 0.5)
    # Find and click the button.
    action.move_to_element(more_option_elem).click().perform()
    # Wait for animation to finish.
    sleep(0.4)

    # "Add to album" button.
    add_to_album_xpath = '//div[@aria-label="More options"][@__is_owner="true"]'#"/html/body/div[1]/div/c-wiz/div[4]/c-wiz/div[1]/div[2]/div[2]/span/div/div[10]/div"
    add_to_album_elem = wait_xpath(driver, add_to_album_xpath, 5, 0.5)
    # Find and click the button.
    action.move_to_element(add_to_album_elem).click().perform()
    # Wait for animation to finish.
    sleep(0.4)

    # Select album in the popup list.
    album_xpath = f'//li[@data-id="{album_id}"]'
    album_elem = wait_xpath(driver, album_xpath, 5, 0.5)
    # Find and click the album.
    action.move_to_element(album_elem).click().perform()
    # Wait for animation to finish.
    sleep(0.4)
