# from email.policy import strict

from backend.state_schema import pipeline_state,analyzer_output
from backend.llm_instance import groq_llm_opnai

# groq_llm = llm()
structured_llm = groq_llm_opnai.with_structured_output(analyzer_output,method='json_schema')


def analyzer_agent(state:pipeline_state):

    job_desc = state["selected_jobs"]
    resume = state["profileinfo"]
    system_prompt = '''
                    You are an expert career counseller having expertise in resume criticising, shortlisting and all, think like you are an ATS.
                    Now your task is to provide a matching score and missing keywords for a resume with respect to a list of job descriptions(JDs).

                    Consider below points while analysing the resume:
                    - scan the resume against each JD in the list, one at a time, and give a matching score within the range of 0 to 100 as integer for every JD, matching score is like an ATS score.
                    - return one separate score_item per JD, each with its own jd_number (1-based position in the JD list) and its own score.
                    - NEVER combine or concatenate the scores of different JDs into a single number. Each JD gets its own independent score_item.
                    - deciding a matching score should involve experience required in JD, skills requirement in JD, work requirements in JD.
                    - find those keywords that appear across the JDs but are missing in the resume, treat this like where the candidate is lagging.
                    - combine the missing keywords found across all the JDs into a single list, without duplicates.
                    - Do not include any explanation in your response, just respond with the list of score_items and the list of missing keywords.
                    - Do not include any special characters, just simple and normal response,
                    '''
    query = f'''Provide a list of matching scores and a list of missing keywords for the resume w.r.t each JD in the list.
                Resume:\n {resume}
                List of Job Descriptions(JDs):\n {job_desc}'''

    response = structured_llm.invoke(system_prompt + query)
    print(f"analyzer response: {response}")

    scores = [item.score for item in sorted(response.scores, key=lambda item: item.jd_number)]

    print(type(scores))
    print(type(response.missing))

    print(f"Analyzer Agent Done")

    return{"score":scores, "missing":response.missing}