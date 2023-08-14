import requests
import dotenv
import os
from bs4 import BeautifulSoup
import googleapiclient.discovery
import gspread
from oauth2client.service_account import ServiceAccountCredentials

dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')
SHEET_ID=os.getenv('SHEET_ID')

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# Prompt user for search term for YT Query
search_term = input("Enter in a search term: ")

# Format Search URL
search_url = f'https://www.youtube.com/results?search_query={search_term}'

# Use requests to load the search_url
response = requests.get(search_url)

soup = BeautifulSoup(response.text, 'html.parser')

videos = []

for video in soup.select('.yt-uix-tile-link'):
  
  # Get video ID
    video_id = video['href'].split('=')[1]

  # Request video page
    video_page = requests.get(f'https://www.youtube.com/watch?v={video_id}')

  # Parse video page
    soup = BeautifulSoup(video_page.text, 'html.parser')

    # Get title
    title = soup.select_one('#container > h1').text 

    # Get view and like count
    view_count = soup.select_one('#count > yt-view-count-renderer').text
    like_count = soup.select_one('#top-level-buttons > ytd-toggle-button-renderer:nth-child(1) > a').text

    # Create video dict
    video = {
    'id': video_id,
    'title': title,
    'view_count': int(view_count),
    'like_count': int(like_count) 
    }

    videos.append(video)

# Sort videos by view count
sorted_videos = sorted(videos, key=lambda x: x['view_count'], reverse=True)
for video in sorted_videos:
  try:
     row = [video['title'], video['view_count'], video['like_count'], video['id']]
     sheet.append_row(row)
  except Exception as e:
     print("Error appending row: ", e)



print('Scraping for {} complete!'.format(search_term))