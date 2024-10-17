import streamlit as st
import base64
from pathlib import Path


file_agence_path = Path(__file__).resolve().parent.parent / "files" / "AGENCES.pdf"


def display_pdf(file_path):
    with open(file_path, "rb") as file:
        base64_pdf = base64.b64encode(file.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)


def pdf_page():

    st.title("Les villes disponibles pour vous implanter")

    pdf_path = file_agence_path
    display_pdf(pdf_path)

    if st.sidebar.button("Retourner au menu principal"):
        st.session_state["page"] = "main"
