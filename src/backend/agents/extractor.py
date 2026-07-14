from pypdf import PdfReader
from backend.state_schema import pipeline_state


def extractor_agent(state:pipeline_state):

    if state.get('resume_path') is None:
          if state.get('profileinfo'):
                print(f"Extractor Agent Done")
                return {}
    resume_path = state["resume_path"]
    reader = PdfReader(resume_path)
    number_of_pages = len(reader.pages)
    pdf_content= ""
    if number_of_pages>0:
            pdf_content = "\nnext-page\n".join(reader.pages[i].extract_text() for i in range(number_of_pages))

    print(f"Extractor Agent Done")
    return {"profileinfo":pdf_content}


# uploaded_files\MrinmoyHalder_CV.pdf

# D:\Learning\Resume_Critic\uploaded_files\MrinmoyHalder_CV.pdf