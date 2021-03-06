# core packages
import streamlit as st
import streamlit.components.v1 as stc

# additional packages
# Load EDA packages
import pandas as pd

# Data Viz Packages
#import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

#matplotlib.use("Agg")

# text cleaning packages
import neattext as nt
import neattext.functions as nfx


# utils
from collections import Counter
from wordcloud import WordCloud
import base64
import time
import re

timestr = time.strftime("%Y%m%d-%H%M%S")
# External Utils
from app_utils import *


# Functions

from langdetect import detect
from google_trans_new import google_translator  

#simple function to detect and translate text 
def detect_and_translate(text,target_lang):
    
    result_lang = detect(text)
    
    if result_lang == target_lang:
        return text 
    
    else:
        translator = google_translator()
        translate_text = translator.translate(text,lang_src=result_lang,lang_tgt=target_lang)
        return translate_text


# function to get wordcloud
def plot_wordcloud(my_text):
    my_wordcloud = WordCloud().generate(my_text)
    fig = plt.figure(figsize=(15, 9))
    plt.imshow(my_wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig)


# # function to download result
# def make_downloadable(data):
#     csvfile = data.to_csv(index=False)
#     b64 = base64.b64encode(csvfile.encode()).decode()
#     new_filename = f"ChangeBlock_{timestr}_.csv"
#     st.markdown("### ** 📩 ⬇️ Download CSV file **")
#     href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click here!</a>'
#     st.markdown(href, unsafe_allow_html=True)


def main():
    st.title("ChangeBlock APP")
    menu = ["Home", "NLP", "Translation", "About"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home: Sentiment Analysis")
        raw_text = st.text_area("Enter text Here")
        num_of_most_common = st.sidebar.number_input("Most Common Tokens", 5, 15)
        if st.button("Analyze"):
            with st.expander("Original Text"):
                st.write(raw_text)
            with st.expander("Sentiment Analysis"):
                sent = sentiment_analysis(raw_text)
                st.write(sent)
            with st.expander("Entities"):
                entity_result = get_entities(raw_text)
                # st.write(entity_result)

                entity_result = render_entities(raw_text)
                stc.html(entity_result, height=1000, scrolling=True)
            # Layout

            with st.expander("Plot WordCloud"):
                plot_wordcloud(raw_text)

            with st.expander("Text summarization"):
                st.info("Text Summary")
                docx = text_summarizer(raw_text)
                st.write(docx)

            with st.expander("Translation"):
                st.info("Translation")
                docx = detect_and_translate(raw_text,'en')
                st.write(docx)    

                

            col1, col2 = st.columns(2)
            with col1:

                with st.expander("Top Keywords"):
                    st.info("Top Keywords/Tokens")
                    processed_text = nfx.remove_stopwords(raw_text)
                    Keywords = get_most_common_tokens(
                        processed_text, num_of_most_common
                    )
                    st.write(Keywords)

            with col2:
                with st.expander("Plot Word Frequency"):
                    fig = plt.figure()
                    top_Keywords = get_most_common_tokens(
                        processed_text, num_of_most_common
                    )
                    plt.bar(top_Keywords.keys(), top_Keywords.values())
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

            with st.expander("Download Text Analysis Result"):
                pass
    
    elif choice == "Translation":
        st.subheader("Translation")



    # elif choice == "NLP":
    #     st.subheader("NLP Task")
    #     text_file = st.file_uploader("Upload Files", type=["pdf", "docx", "txt"])
    #     num_of_most_common = st.sidebar.number_input("Most Common Tokens", 5, 15)

    #     if text_file is not None:
    #         if text_file.type == "application/pdf":
    #             raw_text = read_pdf(text_file)
    #             # st.write(raw_text)
    #         elif text_file.type == "text/plain":
    #             raw_text = str(text_file.read(), "utf-8")
    #             # st.write(raw_text)

    #         else:
    #             raw_text = docx2txt.process(text_file)
    #             # st.write(raw_text)

    #         with st.expander("Original Text"):
    #             st.write(raw_text)

    #         with st.expander("Entities"):
    #             entity_result = render_entities(raw_text)
    #             stc.html(entity_result, height=1000, scrolling=True)

    #         with st.expander("Plot WordCloud"):
    #             plot_wordcloud(raw_text)



    #         with st.expander("Question Answering"):
    #                   question = st.text_area("Enter text Here")

    #                   if question is not None:
    #                     if question == question:
    #                         if st.button("Analyze"):
    #                             docx = quest_ans(question=question, context= raw_text)
    #                             st.write(docx)

    #         col1, col2 = st.columns(2)
    #         with col1:

    #             with st.expander("Top Keywords"):
    #                 st.info("Top Keywords/Tokens")
    #                 processed_text = nfx.remove_stopwords(raw_text)
    #                 Keywords = get_most_common_tokens(
    #                     processed_text, num_of_most_common
    #                 )
    #                 st.write(Keywords)

    #         with col2:
    #             with st.expander("Plot Word Frequency"):
    #                 fig = plt.figure()
    #                 top_Keywords = get_most_common_tokens(
    #                     processed_text, num_of_most_common
    #                 )
    #                 plt.bar(top_Keywords.keys(), top_Keywords.values())
    #                 plt.xticks(rotation=45)
    #                 st.pyplot(fig)

    #         with st.expander("Download Text Analysis Result"):
    #             pass


    else:
        st.subheader("About")


if __name__ == "__main__":
    main()



