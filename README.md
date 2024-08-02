
# Audio Transcription and Summarization

This project is designed to transcribe and summarize audio files using OpenAI's Whisper and GPT models. The application processes audio files, transcribes them into text, and generates a summary of the transcribed text with an audio file. This guide will walk you through setting up and running the program using Docker.

## Prerequisites

Before running the program, ensure that you have the following installed on your system:

- [Docker](https://www.docker.com/get-started) (version 20.10 or later)
- [Git](https://git-scm.com/) (to clone the repository, if necessary)

## Setup

### 1. Clone the Repository

If you haven't already cloned the repository, you can do so with the following command:

```bash
git clone https://github.com/Goutcho/Audio-Summary.git
```

Navigate into the project directory:

```bash
cd Audio-Summary
```

### 2. Build the Docker Image

To build the Docker image for the application, use the following command:

```bash
docker build -t audio-summary .
```

This command will create a Docker image named `audio-summary`.

## Usage

### Run the Application

To run the application using Docker and use a file locally, put it in the files folder and use the following command while in the main application folder :

```bash
docker run --rm -v $(pwd):/app -e OPENAI_API_KEY=your_api_key_here audio-summary app/files/<name_of_the_file>
```

- Ensure that the `OPENAI_API_KEY` environment variable is set correctly.

### Example

If your audio file is named `example.mp3` and is located in the current directory, you can run:

```bash
docker run --rm -v $(pwd):/app -e OPENAI_API_KEY=your_api_key_here audio-summary app/example.mp3
```

### Output

The program will generate two output files in the working directory:

1. **Transcription Text**: Contains the transcribed text from the audio file.
2. **Summary Text**: Contains the summarized text of the transcription.
1. **Summary Audio**: Contains the summarized audio of the transcription.

The filenames will follow the format: `<base_name>_transcription_<timestamp>.txt` and `<base_name>_summary_<timestamp>.txt`.

## Notes

- Ensure the audio file format is supported (`.mp3`, `.mp4`, `.mpeg`, `.mpga`, `.m4a`, `.wav`, `.webm`).
- If you encounter any issues, check the logs for more information.


