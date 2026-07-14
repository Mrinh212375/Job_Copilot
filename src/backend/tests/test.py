# # import os
# # from typing import TypedDict

# # from dotenv import load_dotenv
# # from pydantic import BaseModel, Field

# # from langchain_groq import ChatGroq
# # from langgraph.graph import StateGraph, START, END


# # # ---------------------------------------------------------------------------
# # # llm_instance.py
# # # ---------------------------------------------------------------------------
# # class llm:

# #     def __init__(self):

# #         if load_dotenv(r"D:\Learning\Learning_Langgraph\key.env"):
# #             self.api_key = os.getenv("GROQ_API_KEY")
# #         else:
# #             self.api_key = None

# #     def get_llm(self):

# #         llm = ChatGroq(model="openai/gpt-oss-120b", api_key=self.api_key)
# #         return llm


# # groq_llm = llm().get_llm()


# # # ---------------------------------------------------------------------------
# # # state_schema.py
# # # ---------------------------------------------------------------------------
# # class critic_state(TypedDict):

# #     jd: str
# #     pdf_path: str
# #     resume_content: str
# #     score: int
# #     missing: list[str]
# #     updated_resume_content: str


# # class job(BaseModel):
# #     filtered: list[dict] = Field(description="filtered job details stored")


# # class rank(BaseModel):
# #     ranks: list[int] = Field(description=" store ranked jobs based on the description and profile")


# # class summary(BaseModel):
# #     final: list[str] = Field(description="store summarised job descriptions")


# # class jobfinder(TypedDict):

# #     profileinfo: str
# #     scrapped_jobs: str
# #     filtered_jobs: list[dict]
# #     ranks: list[int]
# #     selected_jobs: list[str]


# # # ---------------------------------------------------------------------------
# # # agents/Jobfilter_agent.py
# # # ---------------------------------------------------------------------------
# # def filter_jobs(state: jobfinder):

# #     system = f'''
# #                 Filterout Jobs for the profile:\n {state['profileinfo']} \n among jobs:\n {state['scrapped_jobs']}

# #                 coseider below points while filtering:
# #                 - filter jobs based on jobs_description field for each job and the candidate's profile
# #                 - return the response as list of dictionary containing job ids and descriptions.
# #                 '''
# #     query = "match the jobs against the candidate's profile"

# #     response = groq_llm.with_structured_output(schema=job, method='json_schema').invoke(system + query)

# #     return {"filtered_jobs": response.filtered}


# # # ---------------------------------------------------------------------------
# # # agents/JobRank_agent.py
# # # ---------------------------------------------------------------------------
# # def rank_jobs(state: jobfinder):

# #     system = f'''
# #                 Rank the following jobs for the candidate's profile:\n {state['profileinfo']} \n among jobs:\n {state['filtered_jobs']}

# #                 Consider below points while ranking:
# #                 - Rank each job based on its description against the candidate's profile (skills, experience, projects, education)
# #                 - After ranking keep the job ids as per the ranking order
# #                 - response should contain ranked job ids, no need to maintain any extra serial number.

# #                 '''
# #     query = "rank the jobs against the candidate's profile"

# #     response = groq_llm.with_structured_output(schema=rank, method='json_schema').invoke(system + query)

# #     return {"ranks": response.ranks}


# # # ---------------------------------------------------------------------------
# # # agents/JobSummary_agent.py
# # # ---------------------------------------------------------------------------
# # def summary_jobs(state: jobfinder):

# #     system = f'''
# #                 You have to provide final job lists using job details:\n {state['filtered_jobs']} \n and ranked job ids: \n {state['ranks']}

# #                 Consider below points while finalising:
# #                 - match job ids from ranked id list and pick corresponding job description from job details.
# #                 - job ids in ranked job ids are referring the job ids in job details list. this is how you will join both the lists.
# #                 - N.B - ranked job ids are list of integers(as job ids), e.g - [143] treat them as job_id:1, job_id:2 and job_id:3 respectively.
# #                 - response should be list of all those job descriptions as per the ranking order.
# #                 '''
# #     query = "Finalize the jobs"

# #     response = groq_llm.with_structured_output(schema=summary, method='json_schema').invoke(system + query)

# #     return {"selected_jobs": response.final}


# # # ---------------------------------------------------------------------------
# # # workflow_jobscrapper.py
# # # ---------------------------------------------------------------------------
# # workflow = StateGraph(jobfinder)

# # workflow.add_node("filter", filter_jobs)
# # workflow.add_node("rank", rank_jobs)
# # workflow.add_node("summary", summary_jobs)

# # workflow.add_edge(START, "filter")
# # workflow.add_edge("filter", "rank")
# # workflow.add_edge("rank", "summary")
# # workflow.add_edge("summary", END)

# # compiled_graph = workflow.compile()


# # # ---------------------------------------------------------------------------
# # # main.py
# # # ---------------------------------------------------------------------------
# # def main():

# #     profile = '''
# #     Mrinmoy Halder
# # +91-8583853565 | mrinmoyh64@gmail.com | Mrinmoy-H | Github

# # Education

# # Indian Institute of Technology, Delhi — Aug 2021 - Jun 2023, Delhi
# # Master of Technology (M.tech) in Computer Technology

# # University Institute of Technology, University of Burdwan — Aug 2014 - Jul 2018, Burdwan
# # Bachelor of Engineering (B.E) in Computer Science and Engineering

# # Experience

# # Technical Lead, (HCL-Tech, Bengaluru) — Jul 2023 – Present

# # RAG
# # - Developed a RAG Pipeline using LangChain framework.
# # - Leveraged all-mpnet-base-v2 for embeddings, ChromaDB for vector storage and Mistral-7B-instruct for response generation.
# # - Conducted benchmarking of various LLMs, leveraged time complexity, BLEU and ROUGE score.
# # - Built a chatbot using Cohere models and Gradio, achieving superior accuracy and efficiency.

# # Finetuning
# # - Fine-tuned Large Language Models (LLMs) to predict taint propagation and sink vulnerabilities from Java method signatures.
# # - Achieved a 25% accuracy improvement in taint prediction using CodeLlama and a 15% improvement in sink vulnerability detection with codeT5-220M.
# # - Conducted a comparative analysis between CodeLlama and CatBoost, noting close competition.

# # Content Generation and Analysis
# # - Developed an AI-driven platform to generate and optimize email subject lines for sales and marketing campaigns using OpenAI-Gpt4.
# # - Delivered 10 high-impact alternatives per input, enhanced with scoring metrics such as readability, subjectivity, spam, actionability, and persuasive power.
# # - Integrated SQLAlchemy ORM with FastAPI to capture and manage requests in MariaDB.

# # Re-Inforcement Learning
# # - Conducted a comparative study of RLHF using PPO and DPO on a summarization dataset.
# # - Trained a reward model with a preference dataset for PPO and directly used the preference dataset for DPO.
# # - Demonstrated that DPO outperformed PPO in summarization quality, highlighting its efficiency in preference-based tasks.

# # Agentic AI
# # - Developed a Multi-agentic solution to generate requirements document (URS, SRS etc.) according to the user requirements provided by user in realtime.
# # - Leveraged LangGraph's Multi-Agent Supervisor architecture to build the workflow.

# # Notification system
# # - Created an alert notification system in Outlook to send notification of audit Trail deviations to L1 and L2 approvers.

# # Technical Skills
# # - Programming Languages: Python, C, C++, SQL.
# # - Technologies: LLMs, RAG, Finetuning, NLP, Generative AI, Machine Learning, Deep Learning, Time Series Forecasting, Agentic AI, MCP etc.
# # - Frameworks: LangChain, Langgraph, Transformers, TRL, SQLAlchemy, FastAPI, Microsoft GraphAPI, NumPy, Matplotlib, scikit-learn, PyTorch, Streamlit, Gradio, DARTS, etc.
# #                 '''

# #     jobs = '''
# #     {
# #         "job_id": 5,
# #         "job_description": "Role: Data Analyst. Looking for a candidate with 2+ years in business intelligence. Strong skills in SQL, Excel, Power BI, and Tableau required. Responsibilities include building dashboards, writing queries, and presenting insights to stakeholders. Knowledge of statistics and A/B testing preferred. Python for data manipulation is a plus but not mandatory. No deep learning or LLM work involved."
# #     },
# #     {
# #         "job_id": 1,
# #         "job_description": "Role: Generative AI Engineer. We are seeking an engineer with 3+ years of experience in Python and LLM-based applications. Must have hands-on experience building RAG pipelines, working with vector databases (Pinecone, FAISS, ChromaDB), and frameworks like LangChain and LangGraph. Responsibilities include designing multi-agent systems, prompt engineering, and deploying GenAI solutions to production. Familiarity with Groq, OpenAI, or Claude APIs preferred."
# #     },
# #     {
# #         "job_id": 4,
# #         "job_description": "Role: Agentic AI Engineer. Seeking 3-5 years building multi-agent systems and LLM-powered workflows. Must have strong Python skills and hands-on experience with LangGraph supervisor architectures, tool-calling agents, and human-in-the-loop pipelines. Experience fine-tuning LLMs and working with RLHF (PPO/DPO) is highly desirable. You will design autonomous agents that generate documents and automate enterprise workflows."
# #     },
# #     {
# #         "job_id": 2,
# #         "job_description": "Role: Senior Frontend Developer. Looking for a React expert with 5+ years building responsive web applications. Strong proficiency in TypeScript, Next.js, Tailwind CSS, and state management (Redux/Zustand). Experience with REST and GraphQL APIs, CI/CD pipelines, and component testing required. UI/UX sensibility and cross-browser compatibility knowledge essential. No AI/ML experience needed."
# #     },
# #     {
# #         "job_id": 6,
# #         "job_description": "Role: Senior DevOps Engineer. 6+ years managing cloud infrastructure on AWS and Azure. Expertise in Kubernetes, Docker, Terraform, CI/CD pipelines (Jenkins, GitLab), and infrastructure-as-code required. Strong scripting in Bash and Python. Experience with monitoring tools (Prometheus, Grafana) and incident response. This is a pure infrastructure role with no machine learning responsibilities."
# #     },
# #     {
# #         "job_id": 3,
# #         "job_description": "Role: Machine Learning Engineer (NLP focus). 4+ years in ML with deep expertise in NLP. Must know PyTorch/TensorFlow, transformer architectures, fine-tuning LLMs (LoRA, PEFT), and model evaluation. Experience with MLOps, cloud deployment (AWS/Azure), and distributed training. RAG and agentic AI exposure is a plus. Strong understanding of embeddings and retrieval systems."
# #     }
# #                 '''

# #     result = compiled_graph.invoke({"profileinfo": profile, "scrapped_jobs": jobs})

# #     print(f"Final state after execution:\n\n {result}")


# # if __name__ == "__main__":
# #     main()


# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# # Define Item model
# class Item(BaseModel):
#     name: str
#     price: float

# # Temporary in-memory storage
# items = {}

# # CREATE
# @app.post("/items/")
# async def create_item(item: Item):
#     item_id = len(items) + 1
#     items[item_id] = item
#     return {"id": item_id, "item": item}

# # READ
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return items.get(item_id, {"error": "Item not found"})

# # UPDATE
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     if item_id in items:
#         items[item_id] = item
#         return {"message": "Item updated", "item": item}
#     return {"error": "Item not found"}

# # DELETE
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     if item_id in items:
#         deleted_item = items.pop(item_id)
#         return {"message": "Item deleted", "item": deleted_item}
#     return {"error": "Item not found"}


from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

# Imaginary database class
class Database:
    def __init__(self):
        self.db = []

    def add_blog_post(self, blog_post: dict):
        self.db.append(blog_post)

    def get_blog_posts(self):
        return self.db

db = Database()

class BlogPost(BaseModel):
    title: str
    # Making content optional
    content: Optional[str] = None  

@app.post("/create_blog_post")
async def create_blog_post():
    # Input validation
    # if not blog_post.title:
    #     raise HTTPException(status_code=400, detail="Title is required")

    # # Database operation
    # db.add_blog_post(blog_post.dict())

    # Returning a confirmation message
    return {"message": "Blog post created successfully"}

@app.get("/get_blog_posts")
async def get_blog_posts():
    # Returning the list of blog posts from the imaginary database
    return db.get_blog_posts()