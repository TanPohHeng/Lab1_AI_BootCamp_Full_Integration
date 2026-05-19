import streamlit as st
from main import analyze

file = st.file_uploader("Upload your resume", type=["pdf"])
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = file
if file:
    st.session_state["uploaded_file"] = file

degree = st.sidebar.selectbox(
    "Degree",
    ["RTIS", "IMGD", "UXGD", "BFA"]
)

if st.session_state["uploaded_file"]:
    #do stuff
    st.success("File uploaded!")
    pass

jd = st.text_area("Job description:")

analysize_btn = st.button("Analyze Resume")

if analysize_btn:
    st.write("Analyzing Resume")
    #do analysis
    st.session_state["report"] = analyze(st.session_state["uploaded_file"], jd,str(degree))
    st.write(st.session_state["report"])

