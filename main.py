from youtube import YTDownloader

# Step 3: Using the Downloader
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=BS46C2z5lVE"
    downloaded_file_path = YTDownloader.download_video(url, "720p")
    print(f"Downloaded file: {downloaded_file_path}")
