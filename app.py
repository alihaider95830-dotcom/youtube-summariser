"""
YouTube Video Summarizer - Streamlit Application
A user-friendly interface for summarizing YouTube videos using AI.
"""

import streamlit as st
import os
from summarizer import process_youtube_video
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF0000;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .summary-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF0000;
        margin-top: 1rem;
    }
    .error-box {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff4444;
        margin-top: 1rem;
    }
    .info-box {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4444ff;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application function."""

    # Header
    st.markdown('<p class="main-header">🎥 YouTube Video Summarizer</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Get AI-powered summaries of YouTube videos instantly</p>',
        unsafe_allow_html=True
    )

    # Check if API key is configured
    if not os.getenv("GOOGLE_API_KEY"):
        st.markdown(
            '<div class="error-box">⚠️ <strong>Google API Key not found!</strong><br>'
            'Please create a <code>.env</code> file with your <code>GOOGLE_API_KEY</code>.</div>',
            unsafe_allow_html=True
        )
        st.stop()

    # Sidebar with settings
    with st.sidebar:
        st.header("⚙️ Settings")

        # Model selection
        model_choice = st.selectbox(
            "Select Gemini Model",
            options=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
            index=0,
            help="Choose the AI model for summarization. gemini-1.5-flash is faster and cheaper."
        )

        st.markdown("---")

        # Information
        st.markdown("### ℹ️ How it works")
        st.markdown("""
        1. Paste a YouTube video URL
        2. Click 'Summarize Video'
        3. Get an AI-generated summary

        **Features:**
        - ✅ Handles long videos (20+ minutes)
        - ✅ Uses Map-Reduce strategy
        - ✅ Automatic transcript extraction
        - ✅ Error handling
        """)

        st.markdown("---")
        st.markdown("### 📝 Supported URLs")
        st.code("https://www.youtube.com/watch?v=...")
        st.code("https://youtu.be/...")

    # Main content area
    st.markdown("### 🔗 Enter YouTube URL")

    # Input field for YouTube URL
    youtube_url = st.text_input(
        label="YouTube URL",
        placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        label_visibility="collapsed"
    )

    # Example URLs (expandable)
    with st.expander("📌 Need an example? Try these:"):
        st.markdown("""
        - [Python Tutorial (Beginner)](https://www.youtube.com/watch?v=_uQrJ0TkZlc)
        - [AI Explained (Medium)](https://www.youtube.com/watch?v=kCc8FmEb1nY)
        - [Tech Talk (Advanced)](https://www.youtube.com/watch?v=aircAruvnKk)
        """)

    # Summarize button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        summarize_button = st.button(
            "🚀 Summarize Video",
            use_container_width=True,
            type="primary"
        )

    # Process the video when button is clicked
    if summarize_button:
        if not youtube_url:
            st.markdown(
                '<div class="error-box">❌ Please enter a YouTube URL first.</div>',
                unsafe_allow_html=True
            )
        else:
            # Show processing status
            with st.spinner("🔄 Processing video... This may take a minute for long videos."):
                # Create status placeholders
                status_placeholder = st.empty()

                # Step 1: Validation
                status_placeholder.info("🔍 Validating URL...")

                # Step 2: Process the video
                status_placeholder.info("📥 Extracting transcript...")

                # Step 3: Summarize
                status_placeholder.info("🤖 Generating summary with AI...")

                # Call the main processing function
                summary, error = process_youtube_video(youtube_url, model_name=model_choice)

                # Clear the status
                status_placeholder.empty()

                # Display results
                if error:
                    # Show error message
                    st.markdown(
                        f'<div class="error-box">❌ <strong>Error:</strong> {error}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    # Show success message
                    st.success("✅ Summary generated successfully!")

                    # Display the summary
                    st.markdown("### 📄 Video Summary")
                    st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

                    # Additional options
                    st.markdown("---")
                    col1, col2 = st.columns(2)

                    with col1:
                        # Copy to clipboard (using download as workaround)
                        st.download_button(
                            label="📋 Download Summary",
                            data=summary,
                            file_name="youtube_summary.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

                    with col2:
                        # Summarize another video
                        if st.button("🔄 Summarize Another", use_container_width=True):
                            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #888; font-size: 0.9rem;">'
        'Powered by LangChain 🦜 & Google Gemini 🤖 | Built with Streamlit ⚡'
        '</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
