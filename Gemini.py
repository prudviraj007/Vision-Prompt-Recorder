import streamlit as st 
import google.generativeai as genai 
import google.ai.generativelanguage as glm 
from dotenv import load_dotenv
from PIL import Image
import os 
import io 
from pdf2image import convert_from_path
import tempfile
import sqlite3
from sqlite3 import Error
import datetime
import pandas as pd

load_dotenv()

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='JPEG')
    imgByteArr=imgByteArr.getvalue()
    return imgByteArr

def create_connection():
    conn = None;
    db_file = '/Users/prudviraj/Documents/sqlite/invoice.db' 
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    if conn:
        return conn 

def create_table(conn):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS prompts (
                                        id integer PRIMARY KEY,
                                        prompt text NOT NULL,
                                        response text,
                                        date text
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_prompt(conn, prompt):
    """
    Create a new prompt
    :param conn:
    :param prompt:
    :return: prompt id
    """
    sql = ''' INSERT INTO prompts(prompt,response,date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    # Ensure strings are encoded in UTF-8
    utf8_prompt = (prompt[0].encode('utf-8'), prompt[1].encode('utf-8'), prompt[2])
    cur.execute(sql, utf8_prompt)
    conn.commit()
    return cur.lastrowid

API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

st.image("./Google-Gemini-AI-Logo.png", width=200)
st.write("")

tab = st.sidebar.selectbox("Choose a tab", ["Gemini Pro", "Gemini Pro Vision"])

def main():
    conn = create_connection()
    create_table(conn)

    if tab == "Gemini Pro":
        st.header("Interact with Gemini Pro")
        st.write("")

        prompt = st.text_input("prompt please...", placeholder="Prompt")
        model = genai.GenerativeModel("gemini-pro")

        if st.button("SEND",use_container_width=True):
            response = model.generate_content(prompt)

            st.write("")
            st.header("Response")
            st.write("")

            st.markdown(response.text)

            st.write("Data to be inserted: ")
            data = {'ID': 1,
                    'Prompt': [prompt],
                    'Response': [response.text],
                    'CurrentDate': [datetime.date.today().isoformat()]}
            df = pd.DataFrame(data)
            st.table(df)

            prompt_record = (prompt, response.text, datetime.date.today().isoformat())
            prompt_id = insert_prompt(conn, prompt_record)

            st.write("")
            st.write(f"Record inserted with ID: {prompt_id}")

    elif tab == "Gemini Pro Vision":
        st.header("Interact with Gemini Pro Vision")
        st.write("")
        
        image_prompt = st.text_input("Interact with the Image", placeholder="Prompt")
        uploaded_file = st.file_uploader("Choose an Image or PDF", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp", "pdf"])

        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    images = convert_from_path(tmp.name)
                if images:
                    image = images[0]  # Use the first page of the PDF as the image
                    st.image(image, use_column_width=True)
            else:
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)

            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)
            
        if st.button("GET RESPONSE", use_container_width=True):
            model = genai.GenerativeModel("gemini-pro-vision")

            if uploaded_file is not None:
                if image_prompt != "":
                    if uploaded_file.type == "application/pdf":
                        image = images[0]  # Use the first page of the PDF as the image

                    response = model.generate_content(
                        glm.Content(
                            parts = [
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()

                    st.write("")
                    st.write("Response")
                    st.write("")

                    st.markdown(response.text)

                    st.write("Data to be inserted: ")
                    data = {'ID': 1,
                            'Prompt': [image_prompt],
                            'Response': [response.text],
                            'CurrentDate': [datetime.date.today().isoformat()]}
                    df = pd.DataFrame(data)
                    st.table(df)

                    prompt_record = (image_prompt, response.text, datetime.date.today().isoformat())
                    prompt_id = insert_prompt(conn, prompt_record)

                    st.write("")
                    st.write(f"Record inserted with ID: {prompt_id}")

                else:
                    st.write("")
                    st.header("Please Provide a prompt")

            else:
                st.write("")
                st.header("Please Provide an image")

if __name__ == "__main__":
    main()