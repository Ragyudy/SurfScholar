# CPSC 183 Final Project

Noah Dee, Lauren Lee, Grady Yu

## Summary 

Considering the reported success and its ability to reshape TikTok, we wanted to investigate whether we can harness this tool for educational purposes. Our goal is to create software such that given a PDF textbook, it can create a Subway Surfers "brain rot" video containing the summarized information. For example, instead of reading through the textbook in preparation for exams, students could simply attach their (digital) textbook, and an AI will summarize and return the information in the form of a shorter, more appealing video. 

## Setup

0. Install python - https://www.python.org/downloads/
1. Clone this repository to your local computer (git clone git@github.com:Ragyudy/SurfScholar.git)
2. Setup a virtual environment and install dependencies:
   1. `python -m venv .venv`
   2. `source .venv/bin/activate`
   3. `pip install -r requirements.txt`
3. Generate Gemeni API Key (it's free!) – https://ai.google.dev/gemini-api/docs/api-key
4. Create a .env file (reference `.env.example`) and enter your Gemeni API Key
5. `python main.py`
6. OPTIONAL: upload your own textbook notes and "brain rot" video (make sure to name the textbook notes file `notes.pdf` and the video file `input.mp4`)

Note: The audio does not work on QuickTime Player if your app is on default settings. The audio should work if the video is open in VSCode.
