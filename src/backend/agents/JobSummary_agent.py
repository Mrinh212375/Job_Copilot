from backend.state_schema import pipeline_state,job,summary
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from backend.llm_instance import groq_llm_llama


def summary_jobs(state:pipeline_state):

    # state['scrapped_jobs']
    # state['profileinfo']

    system = f'''
                You have to provide final job lists using job details:\n {state['filtered_jobs']} \n and ranked job ids: \n {state['ranks']}

                Consider below points while finalising:
                - match job ids from ranked id list and pick corresponding job description from job details.
                - job ids in ranked job ids are referring the job ids in job details list. this is how you will join both the lists.
                - Ranked job ids are list of integers(as job ids), e.g - if [143] treat them as job_id:1, job_id:4 and job_id:3 respectively.
                - response should be list of all those job descriptions as per the ranking order.
                - return the response as a JSON object only, with no extra text
                - the JSON object must have a single key "final" whose value is a list of strings, each being a job description
                '''
    query = "Finalize the jobs and respond in the required JSON format"


    response = groq_llm_llama.with_structured_output(schema=summary,method ='json_mode').invoke(system + query)

    print("Job Summaery Done")
    return {"selected_jobs":response.final}