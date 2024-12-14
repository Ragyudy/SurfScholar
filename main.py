import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import subprocess
from PyPDF2 import PdfReader
import google.generativeai as genai
from gtts import gTTS
import tempfile
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
API_KEY = os.getenv('GEMENI_API_KEY')

os.environ["MOVIEPY_USE_IMAGEMAGICK"] = "False"

def pdf_to_text(pdf_path):
   pdf_text = ""
   reader = PdfReader(pdf_path)
   # Loop through all pages to extract text
   for page in reader.pages:
       pdf_text += page.extract_text()
   return pdf_text

def summarize(text):
    # PUT UR API KEY HERE
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Summarize the following into a paragraph or two, "
        f"ensuring correct format and punctuation: {text}"
    )
    response = model.generate_content(prompt)
    final_response = ''
    for char in response.text:
        if char != '`':
            final_response += char
    print(final_response)
    return final_response

def format_chunks(text, chunk_size=5):
  words = text.split()
  return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def format_lines(chunk, line_length=3):
  words = chunk.split()
  lines = [' '.join(words[i:i + line_length]) for i in range(0, len(words), line_length)]
  return '\n'.join(lines)

def generate_voiceover(text):
  with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
      tts = gTTS(text)
      tts.save(temp_file.name)
      return temp_file.name

def modify_video(video_file, data):
    text_chunks = format_chunks(data, chunk_size=5)
    formatted_chunks = [format_lines(chunk, line_length=2) for chunk in text_chunks]
    video = VideoFileClip(video_file)

    # Generate voiceover and get the duration of each chunk
    voiceover_file = generate_voiceover(data)
    voiceover = AudioFileClip(voiceover_file)

    duration = voiceover.duration / len(formatted_chunks)

    text_clips = []
    for i, chunk in enumerate(formatted_chunks):
        shadow = TextClip(text=chunk, font_size=30, color='black', font="Arial") \
            .with_duration(duration) \
            .with_position(('center', 'center'))

        txt_clip = TextClip(text=chunk, font_size=30, color='white', font="Arial") \
            .with_duration(duration) \
            .with_position(('center', 'center'))

        # Set the start time for each clip, accumulate durations up to current chunk
        txt_clip = txt_clip.with_start(i * duration)
        shadow = shadow.with_start(i * duration)
        text_clips.append(shadow)
        text_clips.append(txt_clip)

    final_clip = CompositeVideoClip([video] + text_clips)
    final_clip = final_clip.with_audio(voiceover)
    final_clip.write_videofile("output_video_with_voice.mp4", fps=video.fps)

    os.remove
    os.remove(voiceover_file)

def speed_up_video(input_file, output_file, speed_factor):
    audio_filter = f"atempo={speed_factor}"
    video_filter = f"setpts={1/speed_factor}*PTS"

    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter:v", video_filter,
        "-filter:a", audio_filter,
        "-acodec", "libmp3lame",
        output_file
    ]

    subprocess.run(command)

if __name__ == "__main__":
    text = pdf_to_text("notes.pdf")
    summary = summarize(text)
    # Modify video with the response text and add voiceover
    video_file = "input.mp4"
    modify_video(video_file=video_file, data=summary)

    speed_up_video("output_video_with_voice.mp4", "2x_speed_output_video_with_voice.mp4", 1.5)