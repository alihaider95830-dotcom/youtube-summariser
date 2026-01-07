"""
YouTube Video Summarizer using LangChain
This module handles the core logic for extracting transcripts and summarizing YouTube videos.
"""

import os
import re
from typing import Tuple, Optional
from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def validate_youtube_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate if the provided URL is a valid YouTube URL.

    Args:
        url (str): The URL to validate

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not url or not isinstance(url, str):
        return False, "Please provide a valid URL"

    # YouTube URL patterns
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    match = re.match(youtube_regex, url)
    if not match:
        return False, "Invalid YouTube URL. Please provide a valid YouTube video link."

    return True, None


def extract_transcript(youtube_url: str) -> Tuple[Optional[list], Optional[str]]:
    """
    Extract transcript from a YouTube video.

    Args:
        youtube_url (str): The YouTube video URL

    Returns:
        Tuple[Optional[list], Optional[str]]: (documents, error_message)
    """
    try:
        # Create YouTube loader
        loader = YoutubeLoader.from_youtube_url(
            youtube_url,
            add_video_info=True,
            language=["en", "en-US"]
        )

        # Load the transcript
        documents = loader.load()

        if not documents or len(documents) == 0:
            return None, "No transcript found for this video."

        return documents, None

    except Exception as e:
        error_msg = str(e)

        # Handle specific error cases
        if "transcript" in error_msg.lower() or "subtitle" in error_msg.lower():
            return None, "This video has no subtitles/transcript available."
        elif "video unavailable" in error_msg.lower():
            return None, "Video is unavailable or private."
        elif "Video ID" in error_msg:
            return None, "Could not extract video ID from URL."
        else:
            return None, f"Error extracting transcript: {error_msg}"


def summarize_video(
    documents: list,
    model_name: str = "gemini-1.5-flash",
    temperature: float = 0.3
) -> Tuple[Optional[str], Optional[str]]:
    """
    Summarize the video transcript using LangChain's Map-Reduce strategy.

    Map-Reduce Strategy Explanation:
    ================================
    The Map-Reduce approach is ideal for handling long videos that exceed token limits:

    1. MAP PHASE:
       - The transcript is split into smaller chunks (each within token limits)
       - Each chunk is independently summarized using the LLM
       - This creates multiple "mini-summaries"

    2. REDUCE PHASE:
       - All mini-summaries are combined
       - A final summarization pass creates a coherent, comprehensive summary
       - This final summary captures the key points from the entire video

    Benefits:
    - Handles videos of ANY length (no token limit issues)
    - Parallel processing of chunks (faster for long videos)
    - Maintains context and key information throughout

    Args:
        documents (list): List of document objects containing the transcript
        model_name (str): Google Gemini model to use (default: gemini-1.5-flash)
        temperature (float): Model temperature for creativity (default: 0.3)

    Returns:
        Tuple[Optional[str], Optional[str]]: (summary, error_message)
    """
    try:
        # Initialize the Google Gemini model
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        # Text splitter to chunk the transcript into manageable pieces
        # This is crucial for the Map phase - each chunk must fit within token limits
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,  # Characters per chunk
            chunk_overlap=500,  # Overlap to maintain context between chunks
            length_function=len,
        )

        # Split the documents into chunks
        split_docs = text_splitter.split_documents(documents)

        # MAP PROMPT: Used to summarize each individual chunk
        map_prompt_template = """
        You are an expert at analyzing and summarizing YouTube video content.
        Please provide a concise summary of the following portion of a video transcript.
        Focus on the key points, main ideas, and important details.

        Transcript excerpt:
        {text}

        Concise summary:
        """
        map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

        # REDUCE PROMPT: Used to create the final summary from all chunk summaries
        combine_prompt_template = """
        You are an expert at synthesizing information from video content.
        Below are summaries from different parts of a YouTube video.
        Please create a comprehensive, well-structured final summary that:

        1. Captures the main topic and purpose of the video
        2. Highlights the key points and important takeaways
        3. Maintains logical flow and coherence
        4. Is concise yet informative (aim for 3-5 paragraphs)

        Partial summaries:
        {text}

        Comprehensive final summary:
        """
        combine_prompt = PromptTemplate(
            template=combine_prompt_template,
            input_variables=["text"]
        )

        # Load the summarization chain with Map-Reduce strategy
        # chain_type="map_reduce" ensures we can handle long transcripts
        chain = load_summarize_chain(
            llm=llm,
            chain_type="map_reduce",  # Map-Reduce strategy for long documents
            map_prompt=map_prompt,     # Prompt for individual chunks
            combine_prompt=combine_prompt,  # Prompt for final combination
            verbose=False  # Set to True for debugging
        )

        # Run the chain to generate the summary
        # Try new API first (invoke), fallback to old API (run) if needed
        try:
            # New LangChain API (v0.1.0+)
            result = chain.invoke({"input_documents": split_docs})
            # Extract the summary from the result
            summary = result.get("output_text", result) if isinstance(result, dict) else result
        except (AttributeError, TypeError):
            # Fallback to old LangChain API
            summary = chain.run(split_docs)

        return summary, None

    except Exception as e:
        error_msg = str(e)

        # Handle specific error cases
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return None, "Google API key is missing or invalid. Please check your .env file."
        elif "rate limit" in error_msg.lower():
            return None, "Google API rate limit exceeded. Please try again later."
        elif "quota" in error_msg.lower():
            return None, "Google API quota exceeded. Please check your account."
        else:
            return None, f"Error during summarization: {error_msg}"


def process_youtube_video(
    youtube_url: str,
    model_name: str = "gemini-1.5-flash"
) -> Tuple[Optional[str], Optional[str]]:
    """
    Main function to process a YouTube video: validate, extract transcript, and summarize.

    Args:
        youtube_url (str): The YouTube video URL
        model_name (str): Google Gemini model to use

    Returns:
        Tuple[Optional[str], Optional[str]]: (summary, error_message)
    """
    # Step 1: Validate the URL
    is_valid, error = validate_youtube_url(youtube_url)
    if not is_valid:
        return None, error

    # Step 2: Extract the transcript
    documents, error = extract_transcript(youtube_url)
    if error:
        return None, error

    # Step 3: Summarize the transcript
    summary, error = summarize_video(documents, model_name=model_name)
    if error:
        return None, error

    return summary, None
