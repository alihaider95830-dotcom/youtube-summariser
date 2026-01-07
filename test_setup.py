"""
Test script to verify the YouTube Summarizer setup
This checks imports and basic functionality without needing an API key
"""

import sys

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Testing imports...")

    try:
        import streamlit
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import streamlit: {e}")
        return False

    try:
        import langchain
        print(f"✅ langchain imported successfully (version: {langchain.__version__})")
    except ImportError as e:
        print(f"❌ Failed to import langchain: {e}")
        return False

    try:
        from langchain_community.document_loaders import YoutubeLoader
        print("✅ YoutubeLoader imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import YoutubeLoader: {e}")
        return False

    try:
        from langchain_openai import ChatOpenAI
        print("✅ ChatOpenAI imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ChatOpenAI: {e}")
        return False

    try:
        from langchain.chains.summarize import load_summarize_chain
        print("✅ load_summarize_chain imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import load_summarize_chain: {e}")
        return False

    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        print("✅ RecursiveCharacterTextSplitter imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import RecursiveCharacterTextSplitter: {e}")
        return False

    try:
        import openai
        print(f"✅ openai imported successfully (version: {openai.__version__})")
    except ImportError as e:
        print(f"❌ Failed to import openai: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("✅ dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import dotenv: {e}")
        return False

    print("\n✅ All imports successful!\n")
    return True


def test_url_validation():
    """Test URL validation function."""
    print("🔍 Testing URL validation...")

    try:
        from summarizer import validate_youtube_url

        # Test valid URLs
        test_urls = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
            ("https://youtu.be/dQw4w9WgXcQ", True),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", True),
            ("invalid_url", False),
            ("https://google.com", False),
        ]

        for url, expected_valid in test_urls:
            is_valid, error = validate_youtube_url(url)
            if is_valid == expected_valid:
                print(f"✅ Correctly validated: {url[:50]}...")
            else:
                print(f"❌ Failed validation for: {url}")
                return False

        print("✅ URL validation working correctly!\n")
        return True

    except Exception as e:
        print(f"❌ Error testing URL validation: {e}\n")
        return False


def test_syntax():
    """Test if Python files have correct syntax."""
    print("🔍 Testing Python syntax...")

    files = ["app.py", "summarizer.py"]

    for filename in files:
        try:
            with open(filename, 'r') as f:
                compile(f.read(), filename, 'exec')
            print(f"✅ {filename} has valid syntax")
        except SyntaxError as e:
            print(f"❌ Syntax error in {filename}: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return False

    print("✅ All files have valid syntax!\n")
    return True


def main():
    print("=" * 60)
    print("YouTube Video Summarizer - Test Suite")
    print("=" * 60)
    print()

    # Test syntax first
    if not test_syntax():
        print("\n❌ Syntax test failed. Please fix syntax errors.")
        sys.exit(1)

    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Run: pip install -r requirements.txt")
        sys.exit(1)

    # Test URL validation
    if not test_url_validation():
        print("\n❌ URL validation test failed.")
        sys.exit(1)

    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Create .env file with your OPENAI_API_KEY")
    print("2. Run: streamlit run app.py")
    print("3. Test with a real YouTube URL")
    print()


if __name__ == "__main__":
    main()
