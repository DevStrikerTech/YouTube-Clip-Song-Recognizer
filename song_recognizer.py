import youtube_dl
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import requests
import os
from dotenv import load_dotenv
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SongRecognizer:
    """
    A class for recognizing songs from YouTube videos using the Shazam API.
    
    Attributes:
        api_key (str): The API key for accessing the Shazam API.
        shazam_api_url (str): The URL of the Shazam API endpoint.
    """
    
    def __init__(self, api_key: str) -> None:
        """
        Initializes the SongRecognizer object with the Shazam API key.
        
        Args:
            api_key (str): The API key for accessing the Shazam API.
        """
        self.api_key = api_key
        self.shazam_api_url = "https://shazam.p.rapidapi.com/songs/detect"
    
    def fetch_video_metadata(self, video_id: str) -> Optional[str]:
        """
        Fetches metadata for a YouTube video.
        
        Args:
            video_id (str): The ID of the YouTube video.
        
        Returns:
            str: The title of the YouTube video, or None if metadata cannot be retrieved.
        """
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {'quiet': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
        return info_dict.get('title')
    
    def download_video(self, video_id: str, output_path: str) -> None:
        """
        Downloads a YouTube video.
        
        Args:
            video_id (str): The ID of the YouTube video.
            output_path (str): The path to save the downloaded video.
        """
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    
    def extract_audio(self, video_path: str, output_path: str) -> None:
        """
        Extracts audio from a video file.
        
        Args:
            video_path (str): The path to the video file.
            output_path (str): The path to save the extracted audio file.
        """
        video_filename = os.path.basename(video_path)
        audio_filename = os.path.splitext(video_filename)[0] + ".mp3"
        output_audio_path = os.path.join(output_path, audio_filename)
        
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_audio_path)
        video_clip.close()
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribes audio from an audio file using Google Speech Recognition.
        
        Args:
            audio_path (str): The path to the audio file.
        
        Returns:
            str: The transcribed text.
        """
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"
    
    def recognize_song(self, audio_data: str) -> Optional[dict]:
        """
        Recognizes the song from audio data using the Shazam API.
        
        Args:
            audio_data (str): The audio data to be recognized.
        
        Returns:
            dict: A dictionary containing information about the recognized song,
                  or None if no song is recognized.
        """
        headers = {
            "x-rapidapi-host": "shazam.p.rapidapi.com",
            "x-rapidapi-key": self.api_key,
            "content-type": "application/json",
        }
        params = {"content": audio_data}
        response = requests.post(self.shazam_api_url, headers=headers, json=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger.error("Error occurred while recognizing the song: %s", response.status_code)
            return None

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variables
api_key = os.getenv('RAPIDAPI_KEY')

# Example usage
video_id = "VIDEO_ID"  # Replace VIDEO_ID with the ID of the YouTube video
input_video_path = "path/to/input.mp4"  # Replace with input video file path
output_audio_path = "path/to/output.mp3"  # Replace with output audio file path

recognizer = SongRecognizer(api_key)
video_title = recognizer.fetch_video_metadata(video_id)
logger.info("Video Title: %s", video_title)

recognizer.download_video(video_id, input_video_path)
recognizer.extract_audio(input_video_path, output_audio_path)

transcription = recognizer.transcribe_audio(output_audio_path)
logger.info("Transcription: %s", transcription)

result = recognizer.recognize_song(transcription)
logger.info("Recognized Song: %s", result)
