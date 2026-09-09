import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "MeetingMind"
    APP_VERSION = "1.0.0"

    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

    FFMPEG_PATH = os.getenv(
        "FFMPEG_PATH",
        r"C:\ffmpeg\bin"
    )

    CHROMA_DIR = os.getenv(
        "CHROMA_DIR",
        "vector_db"
    )


settings = Settings()