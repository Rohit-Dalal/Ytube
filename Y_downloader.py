from pytube import YouTube, Playlist
from os.path import isfile


def isurl(file_):
    if isinstance(file_, str):
        return True
    else:
        return False

def url_list(file):
    with open(file, 'r') as f:
        urls = [ line.replace("\n", "") for line in f.readlines() ]
        return urls

def downloader(link):
    if isurl(link):
        vid = YouTube(link)
        return vid.streams



print(downloader('https://www.youtube.com/watch?v=Wy6ec9YTO8g'))





