from typing import TypedDict,Annotated
from pydantic import BaseModel,Field
import operator



class score_item(BaseModel):
     jd_number: int = Field(description="1-based index of the JD this score belongs to, matching its position in the input JD list")
     score: int = Field(ge=0, le=100, description="ATS style matching score for this single JD only, an integer between 0 and 100")

class analyzer_output(BaseModel):
     scores: list[score_item] = Field(description="One score_item per JD, in the same order as the input list of JDs, never merge multiple JDs' scores into one number")
     missing: list[str] = Field(description="Keywords that appear across the job descriptions but are missing in the resume")

# class special_dict(TypedDict):
#      job_serial_number: int
#      job_description: str

# class filter_agent_output(BaseModel):
#      filtered_jobs: list[special_dict] = Field(description="Filter out Jobs from a list of special_dict considering candidate's profile and job_description")

class job(BaseModel):
     filtered: list[dict] = Field(description="")

class rank(BaseModel):
     ranks: list[int] = Field(description=" store ranked jobs based on the description and profile")

class summary(BaseModel):
     final: list[str]  = Field(description="store summarised job descriptions")


                                 
class pipeline_state(TypedDict):
    """Single state model shared by every node in the sequential
    extractor -> job_search -> critic workflow (workflow.py)."""

    messages: Annotated[list, operator.add]
    resume_path: str
    profileinfo: str
    scrapped_jobs: list[dict]
    filtered_jobs: list[dict]
    ranks: list[int]
    selected_jobs: list[str]

    #resume_content: str
    score: list[int]
    missing: list[str]
    updated_resume_content: str
