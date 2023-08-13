import dotenv
import os
import googleapiclient.discovery
import gspread
from oauth2client.service_account import ServiceAccountCredentials
dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')
SHEET_ID = os.getenv('SHEET_ID')

# Authorization for Google Sheets 
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1 

# YouTube API client
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

# Add input for search term 
search_term = input("Enter a search term: ")

# Set search parameters
params = {
    'part': 'snippet',
    'maxResults': 50,
    'q': search_term
} 

# Rest of script...

while True:
    # Make API request
    response = youtube.search().list(**params).execute()
    
    # Get data from response
    for item in response['items']:
        title = item['snippet']['title']
        description = item['snippet']['description']  

        # No viewCount or likeCount available here
        
        sheet.append_row([title, description])
        
    # Paginate
        token = response.get('nextPageToken')
        if token:
            params['pageToken'] = token
        else:
            break

print('Scraping for {} complete!'.format(search_term))