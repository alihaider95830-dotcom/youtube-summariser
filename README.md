# 🎥 YouTube Video Summarizer

An AI-powered application that generates comprehensive summaries of YouTube videos using LangChain and Google Gemini. Perfect for quickly understanding long videos without watching them entirely.

## ✨ Features

- **Smart Summarization**: Uses Google Gemini models (gemini-1.5-flash, gemini-1.5-pro, or gemini-pro)
- **Handles Long Videos**: Map-Reduce strategy automatically handles videos over 20 minutes
- **Automatic Transcript Extraction**: Fetches video transcripts automatically
- **User-Friendly Interface**: Built with Streamlit for an intuitive experience
- **Error Handling**: Gracefully handles missing transcripts and API errors
- **Multiple Model Options**: Choose between different Gemini models based on your needs

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Framework**: LangChain (latest version)
- **Frontend**: Streamlit
- **LLM**: Google Gemini (gemini-1.5-flash, gemini-1.5-pro, or gemini-pro)
- **Transcript Loader**: YoutubeLoader from langchain_community

## 📋 Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd youtube-summariser
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your Google Gemini API key
   # GOOGLE_API_KEY=your_api_key_here
   ```

## 🎯 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app should automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

3. **Summarize a video**
   - Paste a YouTube URL into the input field
   - Click "Summarize Video"
   - Wait for the AI to generate your summary (may take 30-60 seconds for long videos)

## 📁 Project Structure

```
youtube-summariser/
│
├── app.py                 # Streamlit frontend application
├── summarizer.py          # LangChain logic with Map-Reduce strategy
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .env                  # Your actual environment variables (create this)
└── README.md             # This file
```

## 🔧 How It Works

### Map-Reduce Strategy

The application uses a **Map-Reduce strategy** to handle long videos that exceed token limits:

1. **Map Phase**:
   - The transcript is split into smaller chunks (10,000 characters each)
   - Each chunk is independently summarized by the LLM
   - This creates multiple "mini-summaries"

2. **Reduce Phase**:
   - All mini-summaries are combined
   - A final summarization pass creates a coherent, comprehensive summary
   - The final summary captures key points from the entire video

**Benefits**:
- ✅ Handles videos of ANY length (no token limit issues)
- ✅ Maintains context and key information
- ✅ More efficient than processing the entire transcript at once

### Workflow

```
YouTube URL → Validation → Transcript Extraction → Text Splitting →
Map (Summarize Chunks) → Reduce (Combine Summaries) → Final Summary
```

## 🎨 Supported YouTube URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## ⚙️ Configuration

### Model Selection

You can choose between different Google Gemini models in the sidebar:

- **gemini-1.5-flash** (Recommended): Fast and cost-effective
- **gemini-1.5-pro**: Most capable with advanced reasoning
- **gemini-pro**: Balanced performance

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |

## ❌ Error Handling

The application handles various error scenarios:

- **Invalid URL**: Validates YouTube URL format
- **No Transcript**: Detects videos without subtitles/transcripts
- **Private/Unavailable Videos**: Handles access restrictions
- **API Errors**: Manages rate limits, authentication, and quota issues

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your Google Gemini API key secure
- The `.env` file is included in `.gitignore`

## 💡 Tips

1. **For best results**: Use videos with clear, well-structured content
2. **Long videos**: May take 1-2 minutes to process
3. **API costs**: gemini-1.5-flash is the most cost-effective option
4. **No transcript**: The video must have subtitles/captions available

## 🐛 Troubleshooting

### "This video has no subtitles/transcript available"
- The video needs to have captions enabled
- Try enabling auto-generated captions in YouTube settings

### "Google API key is missing or invalid"
- Check that your `.env` file exists and contains `GOOGLE_API_KEY`
- Verify your API key is correct

### "Rate limit exceeded"
- Wait a few minutes and try again
- Google Gemini has generous free tier limits

## 📦 Dependencies

See `requirements.txt` for the full list of dependencies:
- streamlit
- langchain
- langchain-community
- langchain-google-genai
- google-generativeai
- youtube-transcript-api
- pytube
- python-dotenv
- tiktoken

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Powered by [Google Gemini](https://ai.google.dev/)
- UI created with [Streamlit](https://streamlit.io/)

---

**Made with ❤️ by a Senior Python AI Engineer**
