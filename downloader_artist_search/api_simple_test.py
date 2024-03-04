

"""
Doesn't work yet 
from pytube import Channel
"""

from pytube import Channel

c = Channel('https://www.youtube.com/c/ToopetVideos')

print("channel name  :", c.channel_name)
for url in c.video_urls:
    print(url)