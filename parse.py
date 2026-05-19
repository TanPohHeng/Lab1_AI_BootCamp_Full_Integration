from pypdf import PdfReader, errors
import sys
import re


def read_resume_pdf(path: str) -> str: 
    try:
        reader = PdfReader(path)
        #num_pages = len(reader.pages)
        num_pages = len(reader.pages)
        if num_pages > 2:
            sys.stderr.write("Resume is more than 2 pages!\n")
        text = ""
        for i in range (num_pages):
            text += (reader.pages[i].extract_text()) or ""
            text += ("\n\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        if len(text) < 200:
            raise ValueError
        elif len(text) > 24000:
            text = text[0:24000]
            sys.stderr.write("Resume is more than 24000 characters!\n")
        return text
    except errors.EmptyFileError:
        print(f"Error: The file {path} is empty.\n")
        raise ValueError
    except errors.ParseError as e:
        print(f"Error: {path} is not a valid PDF or is corrupted. {e}\n")
        raise ValueError
    except Exception as e:
        print(f"An unexpected error occurred: {e}\n")
        raise ValueError

def read_jd_text(path: str) -> str: 
    try:
        jd = open(path, encoding = "utf-8")
        jdText = jd.read()
        if len(jdText) < 100:
            print(f"Error: The file at {path} has < 100 characters.\n")
            raise ValueError
        # if isinstance(jd,str):
        #     print("text is string")
        return jdText
    except errors.EmptyFileError:
        print(f"Error: The file {path} is empty.\n")
        raise ValueError
