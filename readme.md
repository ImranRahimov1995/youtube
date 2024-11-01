# YouTube Downloader

A Python script that allows you to download videos and audio from YouTube using the `yt-dlp` library. This downloader supports quality selection and can handle both single videos and playlists.

## Features

- Download videos in various quality settings (e.g., 4K, 1080p, 720p, etc.)
- Download audio in MP3 format
- Supports both single video downloads and playlists
- Configurable download directory

## Requirements

- Python 3.7 or higher
- `yt-dlp`
- `ffmpeg` (for audio extraction)

## Installation

1. **Clone the repository** or download the script:

    ```bash
    git clone https://github.com/yourusername/youtube-downloader.git
    cd youtube-downloader
    ```

2. **Install dependencies** using pip:

    ```bash
    pip install yt-dlp
    ```

3. **Install FFmpeg**:
   - On Windows, you can download it from [FFmpeg's official site](https://ffmpeg.org/download.html).
   - On macOS, you can install it using Homebrew:

     ```bash
     brew install ffmpeg
     ```

   - On Linux, use your package manager (e.g., `apt`, `yum`, etc.):

     ```bash
     sudo apt install ffmpeg
     ```

## Usage

You can use this script directly to download videos or audio. Here's how to do it:

### Download Video

To download a video, specify the URL and the desired quality:

```python
from yt_downloader import YTDownloader

url = "https://www.youtube.com/watch?v=BS46C2z5lVE"
downloaded_file_path = YTDownloader.download_video(url, "360p")
print(f"Downloaded file: {downloaded_file_path}")
```

### Download Audio

To download audio from a video, use the following method:

```python

from yt_downloader import YTDownloader

url = "https://www.youtube.com/watch?v=BS46C2z5lVE"
downloaded_audio_path = YTDownloader.download_audio(url)
print(f"Downloaded audio: {downloaded_audio_path}")

```

### Example of Downloading a Playlist

To download an entire playlist, you can set the is_playlist parameter to True when calling the download method.

```python

url = "https://www.youtube.com/watch?v=QDnBsg6SHiI"
downloaded_playlist_files = YTDownloader.download_video(url, "720p", is_playlist=True)
print(f"Downloaded files: {downloaded_playlist_files}")

```

### Notes
The downloaded files will be saved in the ./downloads directory, which is created automatically.
Ensure that your network connection is stable for successful downloads.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgments
This project uses the yt-dlp library for downloading videos and extracting audio.
Special thanks to the FFmpeg project for audio processing.



### Key Sections Explained

1. **Overview**: Provides a brief introduction to the script and its capabilities.
2. **Features**: Lists the main functionalities of the downloader.
3. **Requirements**: Specifies what is needed to run the script.
4. **Installation**: Detailed steps on how to set up the environment and install necessary packages.
5. **Usage**: Includes code snippets demonstrating how to use the downloader for various tasks, such as downloading video and audio.
6. **Quality Options**: Lists the quality settings that can be used when downloading videos.
7. **Example of Downloading a Playlist**: Shows how to download an entire playlist if desired.
8. **Notes**: Provides additional information about where the files are saved and the need for a stable internet connection.
9. **License and Acknowledgments**: Gives credit for libraries and projects used.

Feel free to adjust any sections to better suit your project or preferences!
