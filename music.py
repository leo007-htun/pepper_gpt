from youtubesearchpython import VideosSearch
import json

# Read the contents of the JSON file
with open('/home/cmpuser1/pepper_gpt/pepper_text.json', 'r') as file:
    search_query = file.read().strip()

# Perform the YouTube search with the search query
videosSearch = VideosSearch(search_query, limit=1)
result = videosSearch.result()
#print(result)

video_link = result['result'][0]['link']
print(video_link)

# Save the video_link to a .txt file
with open('/home/cmpuser1/pepper_gpt/link.txt', 'w') as file:
    file.write(video_link)