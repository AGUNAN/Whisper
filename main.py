import os
from pytube import YouTube
import whisper
from fpdf import FPDF

def download_audio(youtube_url, output_path="audio"):
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    os.makedirs(output_path, exist_ok=True)
    file_path = stream.download(output_path=output_path)
    base, _ = os.path.splitext(file_path)
    mp3_path = base + ".mp3"
    os.rename(file_path, mp3_path)
    print(f"Audio downloaded to: {mp3_path}")
    return mp3_path

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    print("Transcribing audio...")
    result = model.transcribe(audio_path)
    return result["text"]

def save_text_to_pdf(text, output_file="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    lines = text.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)
    pdf.output(output_file)
    print(f"PDF saved as: {output_file}")

if __name__ == "__main__":
    link = input("Enter YouTube video URL: ")
    audio_file = download_audio(link)
    transcript = transcribe_audio(audio_file)
    save_text_to_pdf(transcript)
