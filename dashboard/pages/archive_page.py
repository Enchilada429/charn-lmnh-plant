"""This script will contain downloadable links to CSV files of past plant data."""

import sys
from pathlib import Path
from os import environ as ENV

import streamlit as st
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parents[1]))

from load_s3_data import get_s3_client, get_object_list, generate_object_url


def display_archive_page() -> None:
    """Displays the archive page."""
    st.set_page_config(page_title="Archived Data")

    st.title("Archived Data")
    
    s3 = get_s3_client(ENV)
    bucket = ENV["S3_BUCKET"]

    csv_files = get_object_list(s3, bucket, regex=r".*\.csv$")

    if not csv_files:
        st.info("No CSV files found.")
    else:
        for csv in csv_files:
            url = generate_object_url(s3, bucket, csv)
            st.markdown(f"📄 **{csv}**  \n[⬇️ Download]({url})")


if __name__ == '__main__':
    load_dotenv()
    display_archive_page()