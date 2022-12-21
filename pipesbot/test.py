import urllib.request

# Get the URL of the TikTok video
url = 'https://www.tiktok.com/@lpsn12/video/7178332420536683822?is_from_webapp=1&sender_device=pc'

# Download the video
urllib.request.urlretrieve(url, r'C:\Users\pipee\OneDrive\Desktop\discord-bot\video.mp4')