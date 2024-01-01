# Vision-Prompt-Recorder
This app allows users to interact with the AI model by providing text or image-based prompts. The application supports both text and image-based prompts and can handle multiple file types for image prompts, including JPEG, PNG, and PDF.

## Features
1. Interact with Google's Gemini Pro AI using text or image prompts.
2. Automatically logs and stores all interactions and responses in a SQLite database.
3. Supports multiple file types for image prompts, including JPEG, PNG, and PDF.

## Installation & Setup

1. Clone the repository to your local machine.
```bash
git clone <repository_url>
```

2. Navigate to the project directory.
```bash
cd <project_directory>
```
3. Install the necessary packages listed in the requirements.txt file. It's recommended to do this in a virtual environment to avoid conflicts with your other Python projects.
```pip install -r requirements.txt```

5. Set up your GOOGLE_API_KEY in your `.env` file. This is required to interact with Google's Gemini Pro AI.

## Running the Application

1. Run the Gemini.py script using Streamlit.
```streamlit run Gemini.py```
2. Open your web browser and navigate to localhost:8501 (or the URL provided in your terminal after running the script) to interact with the app.

3. Choose a tab ("Gemini Pro" for text prompts, "Gemini Pro Vision" for image prompts), input your prompt, and click "SEND" or "GET RESPONSE" to interact with the AI and store the response in the database.

## Requirements
* Python 3.x
* Streamlit
* Google's Generative AI Python Client
* dotenv
* Pillow
* pdf2image
* SQLite3
* pandas
