import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
from sentiment_analysis import sentiment_analysis

def check_password():
    def password_entered():
        if st.session_state["password"] == "myapps2025":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("PASSWORD :", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("PASSWORD :", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect ❌")
        return False
    else:
        return True

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="SentimentResults")
    return output.getvalue()

def plot_sentiment_distribution(df):
    counts = df["Sentiment_Category"].value_counts()
    total = counts.sum()
    fig, ax = plt.subplots()
    counts.plot(kind="bar", ax=ax, color=["green", "red", "grey"])
    for i, value in enumerate(counts):
        percent = (value / total) * 100
        ax.text(i, value + 0.5, f"{percent:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_title("Sentiments Repartition")
    ax.set_ylabel("Verbatims %")
    ax.set_xlabel("Sentiment Segment")
    st.pyplot(fig)

if check_password():
    st.title("📊 Sentiment Analysis Application")

    uploaded_file = st.file_uploader("Upload Your Excel File (ID / Verbatims)", type=["xlsx", "xls"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Data Overview :")
        st.dataframe(df.head())

        df = sentiment_analysis(df)
        st.write("Analysis Results :")
        st.dataframe(df)

        plot_sentiment_distribution(df)

        st.download_button(
            label="Download The Excel Results",
            data=to_excel(df),
            file_name="sentiment_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Footer (top-level, no extra indentation)
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f9f9f9;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 16px;
        color: #444;
        border-top: 1px solid #ddd;
    }
    .footer-left { max-width: 65%; }
    .footer-right {
        display: flex;
        align-items: center;
        font-weight: bold;
        color: grey;
        font-size: 18px;
    }
    .footer-right img {
        height: 30px;
        margin-left: 10px;
    }
    </style>
    <div class="footer">
        <div class="footer-left">
            <b>Sentiment Analysis App:</b> Transform raw feedback into actionable insights.
            This application leverages advanced AI to classify emotions, highlight trends,
            and empower smarter business decisions. Simple, powerful, and client‑ready.
        </div>
        <div class="footer-right">
            📊 Developed by : Driss Arabe- EXPANSION CONSULTEAM
    <!-- <img src="https://drive.google.com/uc?export=view&id=1XH71wLJ6hBjrsxbaU9dCONZof-m2j-U8" alt="Logo"> -->
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
