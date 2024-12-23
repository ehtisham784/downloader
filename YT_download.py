import streamlit as st
import yt_dlp
import os
import re

# Set page configuration
st.set_page_config(page_title="YouTube Video Downloader", layout="centered")

st.title("🎥 YouTube Video Downloader")
st.write("Enter a YouTube video link below to download it as an MP4 file.")

youtube_url = st.text_input("YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=example")

# Define a function to sanitize the filename
def sanitize_filename(filename):
    # Replace invalid characters and '#' with '_'
    return re.sub(r'[\\/*?:"<>|#]', "_", filename)

# Define the download function
def download_video(youtube_url):
    try:
        # Define the download options
        output_directory = "downloads"  # Define the folder where videos will be saved
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)  # Create the folder if it doesn't exist

        # Sanitize the filename to avoid issues with special characters
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),  # Save file in the output directory
            'quiet': True,
            'ffmpeg_location': r'C:\Users\hpvic\OneDrive\Desktop\ffmpeg\bin\ffmpeg.exe',  # Adjust this path to your ffmpeg location
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            # Sanitize the filename before returning
            sanitized_filename = sanitize_filename(f"{info['title']}.mp4")
            return info['title'], os.path.join(output_directory, sanitized_filename)
    except Exception as e:
        return None, str(e)

# Streamlit UI and functionality
if st.button("Download Video"):
    if youtube_url:
        with st.spinner("Downloading video..."):
            title, file_name = download_video(youtube_url)
            if title:
                st.success(f"'{title}' has been downloaded successfully!")
                if os.path.exists(file_name):  # Ensure the file exists before opening
                    with open(file_name, "rb") as file:
                        st.download_button(
                            label="Download MP4 File",
                            data=file,
                            file_name=file_name,
                            mime="video/mp4"
                        )
                    os.remove(file_name)  # Remove the file after the download button is used
                else:
                    st.error(f"File not found: {file_name}")
            else:
                st.error(f"An error occurred: {file_name}")
    else:
        st.warning("Please enter a valid YouTube URL.")

st.write("---")
st.write("Built with ❤️ using Streamlit and yt-dlp.")
