from backend.state_schema import pipeline_state,job,rank
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from backend.llm_instance import groq_llm_llama


def rank_jobs(state:pipeline_state):

    # state['scrapped_jobs']
    # state['profileinfo']

    system = f'''
                Rank the following jobs for the candidate's profile:\n {state['profileinfo']} \n among jobs:\n {state['filtered_jobs']}

                Consider below points while ranking:
                - Rank each job based on its description against the candidate's profile (skills, experience, projects, education)
                - After ranking keep the job ids as per the ranking order,if its get shuffled from the actual order in jobs list, then no worries.
                - response should contain ranked job ids with comma separated manner like jobs list.
                - Stricty follow this point: list containing ranked job ids should be comma separated.don't make it a single integer, e.g - [1,2,3...] not like [123..]
                - return the response as a JSON object only, with no extra text
                - the JSON object must have a single key "ranks" whose value is a list of integer job ids in ranked order.
                '''
    query = "rank the jobs against the candidate's profile and respond in the required JSON format"


    response = groq_llm_llama.with_structured_output(schema=rank,method ='json_mode').invoke(system + query)

    print("Job Rank Done")
    return {"ranks":response.ranks}