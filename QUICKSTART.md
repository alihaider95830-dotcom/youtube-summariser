# 🚀 Quick Start Guide

Get up and running with the YouTube Video Summarizer in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation Steps

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd youtube-summariser
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Having installation issues?** Try:
```bash
# Create a virtual environment first
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Then install
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure API Key
```bash
# Copy the example file
cp .env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

**On Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
notepad .env
```

### 4. Test the Setup
```bash
python test_setup.py
```

You should see:
```
✅ All files have valid syntax!
✅ All imports successful!
✅ URL validation working correctly!
✅ ALL TESTS PASSED!
```

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Test

1. Copy this URL: `https://www.youtube.com/watch?v=_uQrJ0TkZlc`
2. Paste it in the text box
3. Click "Summarize Video"
4. Wait 30-60 seconds for the summary

## Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:** Run `pip install -r requirements.txt`

### Issue: `OpenAI API key is missing or invalid`
**Solution:**
- Check that `.env` file exists
- Verify `OPENAI_API_KEY=sk-...` is set correctly
- No quotes or spaces around the key

### Issue: `This video has no subtitles/transcript available`
**Solution:** The video must have captions enabled. Try a different video.

### Issue: `Rate limit exceeded`
**Solution:**
- Wait a few minutes and try again
- Check your OpenAI API usage: https://platform.openai.com/usage
- Consider upgrading your plan

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

## Verify It's Working

Expected behavior:
1. ✅ App loads without errors
2. ✅ URL input field visible
3. ✅ Can paste YouTube URL
4. ✅ "Summarize Video" button clickable
5. ✅ Processing message appears
6. ✅ Summary displays after 30-60 seconds

## Project Structure
```
youtube-summariser/
├── app.py              # Streamlit frontend
├── summarizer.py       # LangChain logic
├── requirements.txt    # Dependencies
├── test_setup.py       # Test script
├── .env               # Your API key (create this)
└── .env.example       # Template
```

## What Can Go Wrong?

### LangChain Version Issues
The code is designed to work with both old and new LangChain APIs. If you get errors:

```bash
# Try specific versions that are known to work
pip install langchain==0.1.9 langchain-community==0.0.24 langchain-openai==0.0.6
```

### YouTube Transcript Extraction Issues
Some videos don't have transcripts. Look for videos with the "CC" icon on YouTube.

### API Costs
- **gpt-4o-mini**: ~$0.01 per video (recommended)
- **gpt-3.5-turbo**: ~$0.02 per video
- **gpt-4o**: ~$0.20 per video (most expensive)

## Next Steps

- Try summarizing different types of videos (short, long, educational, etc.)
- Experiment with different models in the sidebar
- Check out the full README.md for detailed documentation

## Still Not Working?

1. Run the test script: `python test_setup.py`
2. Check the error message carefully
3. Verify Python version: `python --version` (should be 3.9+)
4. Check OpenAI API status: https://status.openai.com/
5. Create an issue on GitHub with the error message

---

**Estimated Time:** 5 minutes
**Difficulty:** Beginner
**Cost:** ~$0.01 per video summary
