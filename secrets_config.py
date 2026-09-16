import os

from dotenv import load_dotenv

load_dotenv()


def get_secret(name: str) -> str | None:
    try:
        import streamlit as st

        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.getenv(name)
