from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv

DRIVER_PATH = r'/Users/jackson/chromedriver'

def initializeWebdriver(path: str):
    """
    Initializes the WebDriver with necessary options.
    """
    service = Service(executable_path=path)
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("detach", True)
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1280,800")
    browser = webdriver.Chrome(service=service, options=option)
    return browser

def ytScrape(browser):
    q = input("Enter a search query for youtube:")
    browser.get("https://www.youtube.com/results?search_query=" + q)
    video_titles = browser.find_elements(By.CSS_SELECTOR, "#video-title > yt-formatted-string")
    video_views = browser.find_elements(By.CSS_SELECTOR, "#metadata-line > span:nth-child(3)")
    videos = []
    for v in range(0,len(video_titles)):
            video = {
                'title': video_titles[v].text,
                'views': video_views[v].text
            }
            videos.append(video)
    with open('videos.csv', 'w') as csvfile:

        # Create CSV writer
        writer = csv.writer(csvfile)

        # Write column headers
        writer.writerow(['Title', 'Views'])
        
        # Write video data  
        for video in videos:
            writer.writerow([[video['title'], video['views']]])
    

ytScrape(initializeWebdriver(DRIVER_PATH))