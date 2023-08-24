import requests
from bs4 import BeautifulSoup
import urllib.parse

def download_reddit_video(reddit_video_url):
    # URL to the main website
    main_url = "https://rapidsave.com/info?url="

    # Extract the unique identifier for the filename
    unique_identifier = reddit_video_url.split('/')[-2] + "_" + reddit_video_url.split('/')[-1]

    # Construct the complete URL
    complete_url = main_url + urllib.parse.quote(reddit_video_url, safe='')

    # Send a GET request to the complete URL
    response = requests.get(complete_url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the download button link
    download_button = soup.find('a', class_='downloadbutton', href=lambda href: href and href.startswith("https://sd.rapidsave.com/download.php"))

    if download_button:
        download_link = download_button['href']

        # Download the video
        video_response = requests.get(download_link)

        # Create a filename using the title and unique identifier
        filename = f"downloads/{unique_identifier}.mp4"

        with open(filename, 'wb') as video_file:
            video_file.write(video_response.content)
            return "success", filename
    else:
        return "error"
