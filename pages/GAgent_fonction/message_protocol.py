import streamlit as st
import logging
import streamlit.components.v1 as components
import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent
module_dir = base_dir / "API_connection"
module_sen_message = "sen_message"

if module_dir not in sys.path:
    sys.path.append(str(module_dir))

imported_message = __import__(module_sen_message)


def generate_response_stream(prompt):
    response_text = st.empty()
    full_response = []

    def update_response(partial_text):
        transformed_text = imported_message.make_links_clickable(partial_text)
        full_response.append(transformed_text)
        response_text.markdown("".join(full_response), unsafe_allow_html=True)

    try:
        imported_message.send_message_stream(prompt, update_response)
        return "".join(full_response)
    except Exception as e:
        error_message = str(e)
        logging.error(f"An error occurred while streaming the message: {e}")
        return error_message


def open_link_in_new_tab(url):
    components.html(
        f"""
            <script type="text/javascript">
                window.open("{url}", "_blank");
            </script>
        """
    )
