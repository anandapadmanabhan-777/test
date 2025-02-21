import streamlit as st
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Retrieve Hugging Face API key from Streamlit secrets
hf_api_key = st.secrets["HF_API_KEY"]
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {"Authorization": f"Bearer {hf_api_key}"}

def get_transcript(video_id):
    transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join(segment["text"] for segment in transcript_data)

def summarize_text(text):
    payload = {
        "inputs": text,
        "parameters": {"max_length": 130, "min_length": 30, "do_sample": False}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()[0]["summary_text"]

def main():
    st.title("YouTube Video Summarizer")
    video_url = st.text_input("Enter YouTube video URL")
    if video_url:
        # Extract video ID from URL
        match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url)
        if match:
            video_id = match.group(1)
            try:
                transcript = get_transcript(video_id)
                st.write("Transcript fetched. Generating summary...")
                summary = summarize_text(transcript)
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Invalid YouTube URL.")

if __name__ == "__main__":
    main()
