from fpdf import FPDF
from backend.state_schema import pipeline_state


def pdf_writer_agent(state:pipeline_state):
      
    edited_content = state["updated_resume_content"]
    #   with open("updated_resume.pdf","")
    safe_content = edited_content.encode('latin-1', 'replace').decode('latin-1')


    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(w=0, h=10,txt=safe_content)
    pdf.output("tailored_resume.pdf")
    print(f"Writer Agent Done")
    return {}