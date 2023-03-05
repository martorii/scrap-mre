from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from typing import List
from bs4 import BeautifulSoup
from bs4.element import Comment
import re


def get_html_from_page_selenium(url: str, headless: bool = False) -> str:
    """
    Given an url, return its html.
    """    
    # Add headless option
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    
    # Start browser
    with webdriver.Chrome(chrome_options=chrome_options) as browser:
        # Connect to url
        browser.get(url)
        # Wait until it is loaded
        time.sleep(1)
        # Get html
        html = browser.page_source
    
    # Fetch html
    return html

def get_html_from_page(url: str) -> str:
    """
    Given an url, return its html.
    """
    from urllib.request import urlopen
    
    # Start browser
    with urlopen("https://www.munichre.com/en") as r:
        # Fetch html
        html = r.read()
    
    return html


def get_all_urls_from_html(html: str) -> List:
    """
    Search for all href in html.
    """
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True)]


def get_visible_text_from_html(html: str) -> str:
    """
    Get only the visible text from html.
    """
    # Get whole soup
    soup = BeautifulSoup(html, 'html.parser')
    # Look only at the main division
    main_div = soup.find("main", {"class": "main content"})
    # Get visible text
    text = main_div.get_text()
    # Remove multiple spaces
    text = re.sub(r'[ \n\r\t]+', ' ', text)
    text = re.sub(r'[ ]+', ' ', text)
    return text