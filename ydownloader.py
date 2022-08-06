import os
import argparse
from pytube import YouTube
from concurrent.futures import ThreadPoolExecutor


class YoutubeDownloader:
    def __init__(self):
        self.cwd = os.getcwd()
        self.file_path = None
        self.urls = None

    def get_url_list_file(self):
        file = argparse.ArgumentParser(
            description="File which contains Urls list eg: urls.txt"
        )
        file.add_argument("FileName", metavar="file name", type=str)
        args = file.parse_args()
        input_file_name = args.FileName
        self.file_path = os.path.join(self.cwd, input_file_name)

    def read_urls_from_file(self):
        try:
            with open(self.file_path) as f:
                self.urls = f.readlines()
                if not self.urls:
                    print("file should not be empty. minimum one video url required.")
        except FileNotFoundError:
            print("File not Found. Please check file name")
            exit()

    def video_downloader(self, video_url):
        yt_video = YouTube(video_url)
        stream = yt_video.streams.filter(file_extension="mp4")
        video = stream.get_highest_resolution()
        print(f"\r {yt_video.title} - download starting...")
        print("\r downloading...")
        video.download()
        print(f"\r {yt_video.title} - download completed.")

    def download_video(self):
        with ThreadPoolExecutor() as executor:
            executor.map(self.video_downloader, self.urls)


if __name__ == "__main__":
    ydownload = YoutubeDownloader()
    ydownload.get_url_list_file()
    ydownload.read_urls_from_file()
    ydownload.download_video()
