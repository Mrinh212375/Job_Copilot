import os
from backend.workflow import compiled_graph_pipeline
from fastapi import FastAPI,UploadFile,File
from typing import Annotated
import uvicorn
from pydantic import BaseModel

# profile = '''
#         Mrinmoy Halder
# +91-8583853565 | mrinmoyh64@gmail.com | Mrinmoy-H | Github

# Education

# Indian Institute of Technology, Delhi — Aug 2021 - Jun 2023, Delhi
# Master of Technology (M.tech) in Computer Technology

# University Institute of Technology, University of Burdwan — Aug 2014 - Jul 2018, Burdwan
# Bachelor of Engineering (B.E) in Computer Science and Engineering

# Experience

# Technical Lead, (HCL-Tech, Bengaluru) — Jul 2023 – Present

# RAG
# - Developed a RAG Pipeline using LangChain framework.
# - Leveraged all-mpnet-base-v2 for embeddings, ChromaDB for vector storage and Mistral-7B-instruct for response generation.
# - Conducted benchmarking of various LLMs, leveraged time complexity, BLEU and ROUGE score.
# - Built a chatbot using Cohere models and Gradio, achieving superior accuracy and efficiency.

# Finetuning
# - Fine-tuned Large Language Models (LLMs) to predict taint propagation and sink vulnerabilities from Java method signatures.
# - Achieved a 25% accuracy improvement in taint prediction using CodeLlama and a 15% improvement in sink vulnerability detection with codeT5-220M.
# - Conducted a comparative analysis between CodeLlama and CatBoost, noting close competition.

# Content Generation and Analysis
# - Developed an AI-driven platform to generate and optimize email subject lines for sales and marketing campaigns using OpenAI-Gpt4.
# - Delivered 10 high-impact alternatives per input, enhanced with scoring metrics such as readability, subjectivity, spam, actionability, and persuasive power.
# - Integrated SQLAlchemy ORM with FastAPI to capture and manage requests in MariaDB.

# Re-Inforcement Learning
# - Conducted a comparative study of RLHF using PPO and DPO on a summarization dataset.
# - Trained a reward model with a preference dataset for PPO and directly used the preference dataset for DPO.
# - Demonstrated that DPO outperformed PPO in summarization quality, highlighting its efficiency in preference-based tasks.

# Agentic AI
# - Developed a Multi-agentic solution to generate requirements document (URS, SRS etc.) according to the user requirements provided by user in realtime.
# - Leveraged LangGraph's Multi-Agent Supervisor architecture to build the workflow.

# Notification system
# - Created an alert notification system in Outlook to send notification of audit Trail deviations to L1 and L2 approvers.

# Technical Skills
# - Programming Languages: Python, C, C++, SQL.
# - Technologies: LLMs, RAG, Finetuning, NLP, Generative AI, Machine Learning, Deep Learning, Time Series Forecasting, Agentic AI, MCP etc.
# - Frameworks: LangChain, Langgraph, Transformers, TRL, SQLAlchemy, FastAPI, Microsoft GraphAPI, NumPy, Matplotlib, scikit-learn, PyTorch, Streamlit, Gradio, DARTS, etc.
#                 '''

file_path = None

class Output(BaseModel):
        score:list[int]
        missing_keywords:list[str]


app = FastAPI(description="Job Agent APIs")


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
        return {"file_size": len(file)}

@app.post("/upload/")
async def upload_file(file: UploadFile = File()):
    global file_path
    content = await file.read()

    os.makedirs("uploaded_files", exist_ok=True)
    with open(f"uploaded_files/{file.filename}", "wb") as f1:
        f1.write(content)
    file_path = f"uploaded_files/{file.filename}"
    return {"message": "File uploaded successfully"}


@app.post("/invoke",response_model=Output)
def invoke(path: str | None = None):
        path = path or file_path
        final_result = compiled_graph_pipeline.invoke({"resume_path":path})

        return {"score": final_result['score'], "missing_keywords": final_result['missing']}



if __name__== "__main__":

        uvicorn.run(app,host="127.0.0.1",port=8000)
        

        
        # print(f"\n\n Score:\n{final_result['score']}\n Missing Keyword:\n{final_result['missing']}")


        # print(f"\n\nscrapped_JobIds:\n {[i.get('id','') for i in result['scrapped_jobs']]}")
        # print(f"\n\nselected Job IDs:\n {[i.get('id','') for i in result['filtered_jobs']]}")
        # print("\n\nranked Job Ids:\n",result['ranks'])
        # print("\n\nFinal state after execution:\n",result['selected_jobs'])
        # print(f"\n Length of scrapped Jobs: {len(result['scrapped_jobs'])}\n\n\nFinal Message keys:\n {result['messages']} ")

