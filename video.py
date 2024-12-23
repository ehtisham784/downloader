import streamlit as st
import yt_dlp
import os
import re

# Set page configuration for a simple and mobile-responsive UI layout
st.set_page_config(page_title="🎥 YouTube Video Downloader", layout="centered")

# Add custom CSS for simplicity and responsiveness
st.markdown("""
    <style>
        .title {
            font-size: 28px;
            color: #FF6347;
            font-weight: bold;
            text-align: center;
        }
        .description {
            font-size: 16px;
            color: #4682B4;
            text-align: center;
        }
        .container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: auto;
        }
        input, select, button {
            width: 100%;
            margin-bottom: 15px;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #999;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title">🎥 YouTube Video Downloader</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Enter a YouTube video link below to download it as an MP4 file.</div>', unsafe_allow_html=True)

# Input for the YouTube URL
youtube_url = st.text_input("YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=example")

# Dropdown for selecting video resolution
resolution = st.selectbox("Select Video Resolution", ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"], index=5)

# Define a function to sanitize the filename
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|#]', "_", filename)

# Define the download function
def download_video(youtube_url, resolution):
    try:
        # Define the download options
        output_directory = "downloads"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Define format filter based on the resolution selected
        resolution_dict = {
            "144p": "160",
            "240p": "133",
            "360p": "134",
            "480p": "135",
            "720p": "136",
            "1080p": "137",
            "1440p": "264",
            "2160p": "266"
        }

        # Format based on the selected resolution
        format_code = resolution_dict[resolution]
        ydl_opts = {
            'format': f'{format_code}+bestaudio/best',
            'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
            'quiet': True,
            'ffmpeg_location': r'C:\Users\hpvic\OneDrive\Desktop\ffmpeg\bin\ffmpeg.exe',  # Adjust this path to your ffmpeg location
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            sanitized_filename = sanitize_filename(f"{info['title']}.mp4")
            file_path = os.path.join(output_directory, sanitized_filename)
            return info['title'], file_path
    except Exception as e:
        return None, str(e)

# Streamlit UI for the download button
if st.button("Download Video"):
    if youtube_url:
        st.spinner("🚀 Hang tight! Downloading your video...")
        title, file_name = download_video(youtube_url, resolution)
        if title:
            st.success(f"'{title}' has been downloaded successfully!")
            if os.path.exists(file_name):
                with open(file_name, "rb") as file:
                    st.download_button(
                        label="Download MP4 File",
                        data=file,
                        file_name=file_name,
                        mime="video/mp4"
                    )
                os.remove(file_name)
            else:
                st.error(f"File not found: {file_name}")
        else:
            st.error(f"An error occurred: {file_name}")
    else:
        st.warning("Please enter a valid YouTube URL.")

# Footer information
st.markdown('<div class="footer">Built with ❤️ using Streamlit and yt-dlp.</div>', unsafe_allow_html=True)
