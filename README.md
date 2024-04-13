# YouTube Song Recognizer

YouTube Song Recognizer is a Python application that recognizes songs from YouTube videos using the Shazam API. It extracts the audio from a given YouTube video, transcribes the audio using Google Speech Recognition, and then uses the Shazam API to identify the song.

## Installation

1. Clone the repository:
   `git clone https://github.com/your_username/your_project.git`


2. Install the required dependencies:
   `pip install -r requirements.txt`


3. Set up your RapidAPI key:
   - Rename the `.env.example` file to `.env`.
   - Replace `YOUR_RAPIDAPI_KEY` in the `.env` file with your actual RapidAPI key.

## Usage

1. Run the `main.py` script:
   `python main.py`


2. Provide the YouTube video ID when prompted.

3. Specify the input and output file paths for the video and audio files.

4. The application will download the video, extract the audio, transcribe it, and then recognize the song using the Shazam API.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
