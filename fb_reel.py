import streamlit as st
import yt_dlp
import re
from datetime import datetime
import tempfile
import os
import shutil  # For more robust file operations

# App title and description
st.set_page_config(page_title="Facebook Reel Downloader", page_icon="📽️")
st.title("📽️ Facebook Reel Downloader")
st.markdown("Download any Facebook Reel video by entering its URL below.")

# Helper functions
def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    filename = filename.encode('ascii', 'ignore').decode('ascii')
    return filename.strip()[:100]

def is_valid_facebook_reel_url(url):
    """Check if URL is valid Facebook Reel URL"""
    facebook_reel_pattern = r'(https?:\/\/(?:www\.|m\.)?facebook\.com\/reel\/\S+)'
    return re.match(facebook_reel_pattern, url) is not None

def fetch_reel_data(reel_url):
    """Download Facebook reel data into bytes and return filename"""
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': '%(title)s_%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(reel_url, download=False)
            title = sanitize_filename(info_dict.get('title', 'facebook_reel'))
            video_id = info_dict.get('id')
            ext = info_dict.get('ext', 'mp4')
            filename = f"{title}_{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"

            # Create a temporary directory within the current working directory
            app_temp_dir = os.path.join(os.getcwd(), "app_temp")
            os.makedirs(app_temp_dir, exist_ok=True)
            temp_file_path = os.path.join(app_temp_dir, "temp_reel.mp4")

            ydl_opts_download = {
                'format': 'best[ext=mp4]',
                'outtmpl': temp_file_path,
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_dl:
                ydl_dl.download([reel_url])
                with open(temp_file_path, 'rb') as f:
                    video_bytes = f.read()

            # Clean up the temporary file and directory
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists(app_temp_dir) and not os.listdir(app_temp_dir):
                os.rmdir(app_temp_dir)

            return {
                'status': 'success',
                'data': video_bytes,
                'filename': filename,
                'title': title
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

# Main app interface
url = st.text_input("Enter Facebook Reel URL:", placeholder="https://www.facebook.com/reel/...")

if st.button("Download Video"):
    if not url:
        st.warning("Please enter a URL.")
    elif not is_valid_facebook_reel_url(url):
        st.error("Invalid Facebook Reel URL. Please check the format.")
    else:
        with st.spinner("Fetching and preparing video..."):
            result = fetch_reel_data(url)

            if result['status'] == 'success':
                st.success("✅ Download ready!")

                st.download_button(
                    label="⬇️ Click to Download",
                    data=result['data'],
                    file_name=result['filename'],
                    mime="video/mp4",
                    key=f"download_button_{result['filename']}"
                )

                st.info(
                    "📱 The download should start automatically. Check your browser's Downloads folder."
                )
            else:
                st.error(f"❌ Download failed: {result['message']}")
