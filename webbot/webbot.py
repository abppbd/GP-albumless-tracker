"""
Webbot designed to automatically add Google Photos (GP) images from a list of
urls to a selected album in GP.
Uses selenium webdriver to imitate user input on GP web browser UI.
"""

import functions as SeWd


def start():
    driver = SeWd.init_driver()
    # Find a way to keep the driver between function call
