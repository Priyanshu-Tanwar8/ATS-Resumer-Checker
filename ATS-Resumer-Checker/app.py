from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # convert the pdf to image
        image=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = image[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
             "mime_type": "image/jpeg",
             "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    



# Streamlit App

st.set_page_config(page_title="Resume EXpert")
st.header("ATS Tracking")
input_text = st.text_area("Job Description",key="input")
uploaded_file = st.file_uploader("Upload Your Resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

Submit1 = st.button("Tell Me About The Resume")

Submit2 = st.button("How Can I Improvise My Skills")

#Submit1 = st.button("What are the keyword are missing")

Submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR With Tech Experience in the field of any one job role Data Science , Full stack
Web development, Big Data Engineering, DEVOPS,Data Analyst, your task is to review
the provided resume against the job description for these profiles .
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if Submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response Is")
        st.write(response)

    else:
        st.write("Please upload the resume")    

if Submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response Is")
        st.write(response)

    else:
        st.write("Please upload the resume")    
