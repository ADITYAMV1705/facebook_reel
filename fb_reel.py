import streamlit as st
import os
import yt_dlp
import instaloader
import uuid
import streamlit.components.v1 as components

# App Title
st.set_page_config(page_title="📥 Reel/Video Downloader", page_icon="🎬", layout="centered")
st.title("📥 Facebook & Instagram Reel/Video Downloader")
st.write("Easily download **public** reels/videos from Facebook or Instagram! 🚀")

# Tabs for Facebook and Instagram
tab1, tab2 = st.tabs(["📘 Facebook", "📸 Instagram"])

# --- Instagram Reel Downloader ---
with tab2:

    import requests

    # Inside your Instagram tab:
    st.header("Instagram Reel Downloader")

    reel_url = st.text_input("🔗 Enter Instagram Reel URL:")

    if st.button("Check & Preview Reel", key="insta_btn"):
        if reel_url:
            try:
                st.info("Processing your request... ⏳")

                # Extract shortcode
                shortcode = reel_url.strip().split("/")[-2]

                # Setup Instaloader
                loader = instaloader.Instaloader()

                # Load the post
                post = instaloader.Post.from_shortcode(loader.context, shortcode)

                # Check privacy
                if post.owner_profile.is_private:
                    st.warning("⚠️ This reel is from a **private account**. Cannot preview or download it.")
                else:
                    st.success("✅ This reel is from a public account. Preview below:")

                    # Download the video using requests
                    download_id = str(uuid.uuid4())
                    output_dir = f"downloads/{download_id}"
                    os.makedirs(output_dir, exist_ok=True)

                    video_path = os.path.join(output_dir, "reel.mp4")
                    response = requests.get(post.video_url)
                    with open(video_path, "wb") as f:
                        f.write(response.content)

                    # 🎥 Centered video preview
                    with open(video_path, "rb") as file:
                        video_data = file.read()
                        st.markdown(
                            "<div style='display: flex; justify-content: center;'>",
                            unsafe_allow_html=True
                        )
                        st.video(video_data)
                        st.markdown("</div>", unsafe_allow_html=True)

                    # 🎬 Proper download button
                    with open(video_path, "rb") as file:
                        st.markdown(
                            "<div style='display: flex; justify-content: center; margin-top: 20px;'>",
                            unsafe_allow_html=True
                        )
                        st.download_button(
                            label="⬇️ Download Reel Video",
                            data=file,
                            file_name="reel.mp4",
                            mime="video/mp4",
                        )
                        st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"😣 Oops! Something went wrong: {e}")
        else:
            st.warning("⚠️ Please enter a valid Instagram Reel URL.")

# --- Facebook Video Downloader ---
with tab1:
    st.header("Facebook Reel/Video Downloader")

    fb_url = st.text_input("🔗 Enter Facebook Video URL:")

    if st.button("Fetch & Preview", key="fb_btn"):
        if fb_url:
            try:
                st.info("Fetching the Facebook video... ⏳")

                # Create a unique download folder
                download_id = str(uuid.uuid4())
                output_dir = f"downloads/{download_id}"
                os.makedirs(output_dir, exist_ok=True)

                # Setup yt_dlp options
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': f'{output_dir}/video.%(ext)s',
                    'quiet': True,
                }

                # Download with yt_dlp
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(fb_url, download=True)
                    video_title = info.get("title", "Facebook Video")
                    video_file = ydl.prepare_filename(info)

                # ✅ Video fetched successfully
                st.success("✅ Video fetched successfully!")

                # 🎥 Centered video preview
                with open(video_file, "rb") as file:
                    video_data = file.read()
                    st.markdown(
                        "<div style='display: flex; justify-content: center;'>",
                        unsafe_allow_html=True
                    )
                    st.video(video_data)
                    st.markdown("</div>", unsafe_allow_html=True)

                # 🎬 Centered download button
                with open(video_file, "rb") as file:
                    st.markdown(
                        "<div style='display: flex; justify-content: center; margin-top: 20px;'>",
                        unsafe_allow_html=True
                    )
                    st.download_button(
                        label="⬇️ Download Video",
                        data=file,
                        file_name=os.path.basename(video_file),
                        mime="video/mp4",
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"😢 Failed to download video: {e}")
        else:
            st.warning("⚠️ Please enter a valid Facebook video URL.")
