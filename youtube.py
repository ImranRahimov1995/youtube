import os
import yt_dlp

from uuid import uuid4
from abc import ABC, abstractmethod
from typing import Literal, Optional


MEDIA_ROOT = "./downloads"

Quality = Literal[
    "best",
    "worst",
    "4k",
    "2k",
    "1080p",
    "720p",
    "480p",
    "360p"
]

class MediaDownloader(ABC):
    """Interface for media downloading."""

    @abstractmethod
    def download(self, url: str, is_playlist: bool = False) -> None:
        raise NotImplementedError


class QualitySelectable(ABC):
    """Interface for specifying media quality."""

    @abstractmethod
    def set_quality(self, quality: Quality) -> None:
        """Set the desired quality for download."""
        raise NotImplementedError


class FileOperations(ABC):
    """Interface for file operations."""

    @abstractmethod
    def get_full_path(self, quality: Quality) -> None:
        """Get the full path of the downloaded file."""
        raise NotImplementedError

    @abstractmethod
    def delete_by_path(self, path: str) -> None:
        """Delete the file at the specified path."""
        raise NotImplementedError


class FileHandler(FileOperations):
    """Class for handling file operations."""

    def __init__(self, download_dir: Optional[str] = MEDIA_ROOT) -> None:
        """Initialize the file handler."""
        self._id = uuid4().hex
        self.download_dir = download_dir
        self.output_dir = self._create_output_dir()
        self.full_path = None

    def _create_output_dir(self) -> str:
        """Ensure the output directory exists."""
        _dir = os.path.join(self.download_dir, self._id)
        os.makedirs(_dir, exist_ok=True)
        print(f"Created directory: {_dir}")
        return _dir

    def _get_first_file(self) -> Optional[str]:
        """Get the first file in the specified directory."""
        try:
            files = [
                f for f in os.listdir(self.output_dir)
                if os.path.isfile(os.path.join(self.output_dir, f))
            ]
            if files:
                return files[0]  # Retrieve the first file
            else:
                print("No files found in the directory.")
                return None
        except Exception as e:
            print(f"Error accessing directory: {e}")
            return None

    def get_full_path(self) -> Optional[str]:
        """Get the full path of the first downloaded file."""
        filename = self._get_first_file()
        if filename:
            self.full_path = os.path.join(self.output_dir, filename)
            return self.full_path
        return None

    def delete_by_path(self) -> None:
        """Delete the file at the full path."""
        if self.full_path and os.path.exists(self.full_path):
            os.remove(self.full_path)
            print(f"Deleted file at path: {self.full_path}")
        else:
            print(f"File not found at path: {self.full_path}")


class YTDownloader(MediaDownloader, QualitySelectable):
    """YouTube media downloader with quality selection."""

    def __init__(self, download_type: Literal["video", "audio"]) -> None:
        """Initialize the downloader."""
        self.download_type = download_type
        self.quality = "best"  # Default quality
        self.file = FileHandler(MEDIA_ROOT)

    def set_quality(self, quality: Quality) -> None:
        """Set the desired quality for the download."""
        self.quality = quality

    def download(self, url: str, is_playlist: bool = False) -> None:
        """Download media from a URL with the specified quality."""
        ydl_opts = {
            "format": self._get_format(),
            "outtmpl": f"{self.file.output_dir}/%(title)s.%(ext)s",
            "quiet": True,
            "noplaylist": not is_playlist,  # Download playlist if true
        }

        if self.download_type == "audio":
            ydl_opts.update({
                "format": "bestaudio",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        else:
            ydl_opts["format"] = self._get_format()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Starting download: {url} at quality {self.quality}")
            ydl.download([url])

    def _get_format(self) -> str:
        """Get the download format based on type and quality."""
        if self.download_type == "audio":
            return "bestaudio"
        return (f"bestvideo[height<={self._map_quality_to_height()}][ext=mp4]"
                "+bestaudio[ext=m4a]/mp4")

    def _map_quality_to_height(self) -> int:
        """Map quality label to approximate video height."""
        quality_map = {
            "best": 2160,
            "worst": 144,
            "4k": 2160,
            "2k": 1440,
            "1080p": 1080,
            "720p": 720,
            "480p": 480,
            "360p": 360,
        }
        return quality_map.get(self.quality, 1080)

    @classmethod
    def download_audio(cls, url: str) -> Optional[str]:
        """Download audio from a specified URL."""
        audio_downloader = cls(download_type="audio")
        audio_downloader.set_quality("best")
        audio_downloader.download(url, is_playlist=False)
        return audio_downloader.file.get_full_path()

    @classmethod
    def download_video(cls, url: str, quality: Quality = '1080p') -> Optional[str]:
        """Download video from a specified URL."""
        video_downloader = cls(download_type="video")
        video_downloader.set_quality(quality)
        video_downloader.download(url, is_playlist=False)
        return video_downloader.file.get_full_path()
