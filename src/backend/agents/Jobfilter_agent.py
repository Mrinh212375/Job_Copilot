from backend.state_schema import pipeline_state,job
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from backend.llm_instance import groq_llm_llama


def filter_jobs(state:pipeline_state):

    scrapped_jobs = state['scrapped_jobs']
    final_response = []
    # state['profileinfo']
    m_1 = 0
    m_2 = 5
    magic_number = 5

    # while True:

        # if m_1>len(scrapped_jobs):
        #     break
        # if m_2 > len(scrapped_jobs):
        #     m_2 = len(scrapped_jobs)

        # scrapped_jobs_input = scrapped_jobs[m_1:m_2]

        # m_1 = m_1 + magic_number
        # m_2 = m_2 + magic_number
        # print("\n\n Scrapped jobs input going to LLMs per iteration:\n",scrapped_jobs_input)
    system = f'''
                Filterout Jobs for the profile:\n {state['profileinfo']} \n among jobs:\n {scrapped_jobs}

                coseider below points while filtering:
                - filter jobs based on jobs_description field for each job and the candidate's profile
                - return the response as a JSON object only, with no extra text(follow strictly).
                - the JSON object must have a single key "filtered" whose value is a list of JSON objects, each containing the job id and description of a matching job(follow strictly).
                '''
    query = "match the jobs against the candidate's profile and respond in the required JSON format"

    response = groq_llm_llama.with_structured_output(schema=job,method ='json_mode').invoke(system + query)
    final_response.extend(response.filtered)
    print("JobFilter done")


    return {"filtered_jobs":final_response}


