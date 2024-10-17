import streamlit as st


def inject_custom_css():
    custom_css = """
    <style>
    a {
        color: #00878d;
        text-decoration: none;
    }
    a:hover {   
        text-decoration: underline;
    }
    .element.style{
        color: #00878d;
        }
    /* Change the sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #e4f4f8;
    }
    /* Change the sidebar text color */
    [data-testid="stSidebar"] .css-1d391kg, [data-testid="stSidebar"] .css-2trqyj {
        color: #00878d;
    }
    /* Change the main content background color */
    .css-1g9lxmo {
        background-color: #ffffff;
    }
    /* Change the text color for specific elements */
    .stFileUploader label, .stTextInput label {
        color: #00878d ;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    /* Change the button text color */
    .stButton button {
        color: #00878d !important;
    }
    /* Remove margins from custom paragraphs */
    .custom-paragraph {
        margin-bottom: 0px;
        padding-bottom: 0px;
        line-height: 1.1;
    }
    /* Fix the search bar and buttons at the bottom of the page */
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #ffffff;
        padding: 10px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        z-index: 9999;
    }
    /* Ensure the main content is just above the fixed bottom elements */
    .content {
        padding-bottom: 150px; /* space for the search bar and buttons */
    }
    .st-emotion-cache-ocqkz7 {
        position: fixed;
    }
    /* Fix the title at the top of the page */
    .fixed-top {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #ffffff;
        padding: 50px 10px; /* Increase padding for better visibility */
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        z-index: 9999;
        text-align: center;
    }
    /* Add padding to the top of the main content to account for the fixed title */
    .top-padding {
        padding-top: 150px; /* Adjust this value to ensure content is not hidden */
    }
    /* Align chat messages to the right for User */
    .stChatMessage[data-testid="stChatMessageUser"] {
        text-align: right;
    }
    .st-emotion-cache-1ghhuty.eeusbqq1{
        background-color: #00878d;
    }
    .st-emotion-cache-bho8sy {
        background-color: #00878d;

    }
    .st-emotion-cache-ocqkz7 {
        display: flex;
        flex-wrap: wrap;
        -webkit-box-flex: 1;
        flex-grow: 1;
        -webkit-box-align: stretch;
        align-items: stretch;
        gap: 1rem;
        position: absolute;
}
    .st-emotion-cache-qdbtli {
        position: relative;
    }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
