"""
Unit tests for the SongRecognizer class.
"""

import unittest
from unittest.mock import patch
from song_recognizer import SongRecognizer

class TestSongRecognizer(unittest.TestCase):
    
    @patch('builtins.input', return_value='VIDEO_ID')
    @patch('song_recognizer.SongRecognizer.fetch_video_metadata', return_value='Video Title')
    @patch('song_recognizer.SongRecognizer.download_video')
    @patch('song_recognizer.SongRecognizer.extract_audio')
    @patch('song_recognizer.SongRecognizer.transcribe_audio', return_value='Transcribed Text')
    @patch('song_recognizer.SongRecognizer.recognize_song', return_value={'song': 'details'})
    def test_song_recognizer_workflow(self, mock_recognize_song, mock_transcribe_audio, mock_extract_audio, mock_download_video, mock_fetch_video_metadata, mock_input):
        """
        Test the workflow of the SongRecognizer class.
        """
        # Create an instance of SongRecognizer
        recognizer = SongRecognizer(api_key='TEST_API_KEY')
        
        # Call the method being tested
        recognizer.run()
        
        # Assertions
        mock_input.assert_called_once_with('Enter the YouTube video ID: ')
        mock_fetch_video_metadata.assert_called_once_with('VIDEO_ID')
        mock_download_video.assert_called_once_with('VIDEO_ID', 'video.mp4')
        mock_extract_audio.assert_called_once_with('video.mp4', 'video.mp3')
        mock_transcribe_audio.assert_called_once_with('video.mp3')
        mock_recognize_song.assert_called_once_with('Transcribed Text')

if __name__ == '__main__':
    unittest.main()
