import os
import whisper
import warnings
import openai
from datetime import datetime
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to the console
    ]
)

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning,
                        message="You are using `torch.load` with `weights_only=False`")

# Set up your API key and other configurations as needed
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OpenAI API key is not set.")
    exit(1)  # Exit the program if the API key is not set

# Set OpenAI API key
openai.api_key = api_key  # Ensure API key is set after importing openai


class FileWriter:
    """Class to handle writing text to files."""

    def __init__(self, directory: str):
        """Initialize with a directory path."""
        self.directory = directory
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        """Ensure that the directory exists."""
        os.makedirs(self.directory, exist_ok=True)

    def write_to_file(self, filename: str, content: str):
        """Write content to a file."""
        file_path = os.path.join(self.directory, filename)
        with open(file_path, "w") as f:
            f.write(content)
        logging.info(f"Content saved to {file_path}")


class AudioProcessor:
    """Class to process audio files for transcription and summarization."""

    def __init__(self):
        """Initialize the Whisper model."""
        logging.info("Loading Whisper model...")
        self.model = whisper.load_model("base")
        logging.info("Whisper model loaded.")

    def transcribe_audio(self, file_path: str) -> str:
        """Transcribe the audio file to text using Whisper model."""
        try:
            result = self.model.transcribe(file_path)
            return result['text']
        except Exception as e:
            logging.error(f"Error transcribing audio: {e}")
            return ""

    def summarize_text(self, text: str) -> str:
        """Summarize the text using OpenAI's GPT model."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant that summarizes texts."},
                    {"role": "user", "content": f"Summarize the following text: {text}"}
                ],
                max_tokens=800
            )
            # Correctly access the message content
            summary = response['choices'][0]['message']['content'].strip()
            return summary
        except Exception as e:
            logging.error(f"Error summarizing text: {e}")
            return ""


def generate_output_filename(base_name: str, suffix: str, extension: str) -> str:
    """Generate a unique output filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{suffix}_{timestamp}.{extension}"


def is_supported_format(file_path: str) -> bool:
    """Check if the file format is supported."""
    supported_formats = ('.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm')
    return file_path.lower().endswith(supported_formats)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Transcribe and summarize audio files.")
    parser.add_argument("file_path", type=str, help="Path to the audio file")
    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = parse_arguments()
    file_path = args.file_path

    # Ensure the path is valid on your local system
    if not os.path.exists(file_path):
        logging.error("The specified file does not exist.")
        return

    # Validate file format
    if not is_supported_format(file_path):
        logging.error(
            "Unsupported file format. Supported formats are: mp3, mp4, mpeg, mpga, m4a, wav, webm")
        return

    # Extract the base name of the input file
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Initialize the audio processor
    audio_processor = AudioProcessor()

    # Transcribe the audio
    logging.info("Transcription in progress...")
    text = audio_processor.transcribe_audio(file_path)
    logging.info("Transcription complete. Text:")
    logging.debug(text)

    # Save the transcription to a file
    transcription_writer = FileWriter("audio_transcription")
    transcription_filename = generate_output_filename(
        base_name, "transcription", "txt")
    transcription_writer.write_to_file(transcription_filename, text)

    # Summarize the transcription
    logging.info("Summarization in progress...")
    summary = audio_processor.summarize_text(text)
    logging.info("Summarization complete. Summary:")
    logging.debug(summary)

    # Save the summary to a file
    summary_writer = FileWriter("audio_summarize")
    summary_filename = generate_output_filename(base_name, "summary", "txt")
    summary_writer.write_to_file(summary_filename, summary)


if __name__ == "__main__":
    main()
