# import requests
import json
import ast
from bs4 import BeautifulSoup
import requests
from backend.state_schema import pipeline_state
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from backend.llm_instance import groq_llm_llama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from backend.state_schema import job


def parse_tool_content(content):
    """Tool results come back as a string (ToolNode stringifies the return value);
    parse it back into Python data, whether it was serialized as JSON or repr()."""
    try:
        return json.loads(content)
    except (json.JSONDecodeError, TypeError):
        return ast.literal_eval(content)


def clean_description(html_text: str) -> str:
    """Strip HTML tags from a job description and return clean text."""
    return BeautifulSoup(html_text, "html.parser").get_text(separator=" ", strip=True)

@tool
def searching_jobs_remotive():

    """ scrape jobs from remotive portal and return a list of dictionaries
        agrs: None
    """

    scrapped_jobs=[]
    resp = requests.get("https://remotive.com/api/remote-jobs?search=AIEngineer")
    data = resp.json()

    # print(data)
    print("Total jobs:", len(data["jobs"]))
    for i in range(len(data['jobs'])):
        # print("\n\n",i)
        job_id = data['jobs'][i].get("id","")
        job_description = data['jobs'][i].get("description","")
        scrapped_jobs.append({"id":job_id,"description":clean_description(job_description)[:200]}) 
    

    # print(scrapped_jobs)
    # return {"scrapped_jobs":scrapped_jobs}
    print("returning scrapped jobs from remotive portal.")
    return scrapped_jobs

@tool
def searching_jobs_jobicy():

    """ scrape jobs from jobicy portal and return a list of dictionaries
        agrs: None
    """

    scrapped_jobs=[]
    resp = requests.get("https://jobicy.com/api/v2/remote-jobs?tag=AI+Engineer&count=10")
    data = resp.json()

    # print(data)
    print("Total jobs:", len(data["jobs"]))
    for i in range(len(data['jobs'])):
        # print("\n\n",i)
        job_id = data['jobs'][i].get("id","")
        job_description = data['jobs'][i].get("jobDescription","")
        scrapped_jobs.append({"id":job_id,"description":clean_description(job_description)[:200]}) 
    

    # print(scrapped_jobs)
    # return {"scrapped_jobs":scrapped_jobs}
    print("retruning scracpped jobs from jobicy portal.")
    return scrapped_jobs


toolnode = ToolNode([searching_jobs_remotive,searching_jobs_jobicy])

llm_with_tool = groq_llm_llama.bind_tools([searching_jobs_remotive,searching_jobs_jobicy])


# def agent_method(state:jobfinder):

#     system = '''
#                 You are a Job Search Agent in a multi-agent recruiting pipeline. Your only
#                 responsibility is to obtain the raw job postings that downstream agents
#                 (filter, rank, summary) will work with.

#                 You have access to two tools to scrape jobs from two different portals :
#                 - searching_jobs_remotive: scrapes jobs from a remotive job portal and returns a list
#                   of dicts, each with an "id" and a "description". It takes no arguments.
#                 - searching_jobs_jobicy: scrapes jobs from a jobicy job portal and returns a list
#                   of dicts, each with an "id" and a "description". It takes no arguments.

#                 Tool Invoking rule:
#                 - Being a Job search agent you will always call two tools to scrape jobs from these 2 portals.

#                 Decision rules:
#                 1. If the conversation so far does NOT contain a tool result with scraped
#                    jobs, call the "searching_jobs" tool. Never invent job data yourself.
#                 2. If a tool result with scraped jobs is already present, do not call the
#                    tool again. Just reply "done" - the scraped jobs are read directly from
#                    the tool result, not from your reply.
#             '''
#     query = "Search Jobs from a portal."    ### later this query may come from state['messages']

#     messages = state['messages'] or [HumanMessage(query)]

#     response = llm_with_tool.invoke([SystemMessage(system)] + messages)
#     print(f"job_search LLM response:{response}")

#     update = {"messages":[response]}

#     if not response.tool_calls:
#         for m in reversed(messages):
#             if isinstance(m, ToolMessage) and m.name == "searching_jobs":
#                 update["scrapped_jobs"] = parse_tool_content(m.content)
#                 break

#     return update


# --- Option 2 (not used): tool-calling model + separate formatter call ---
# Keeps an LLM-shaped final output (matching the `job` schema) instead of
# reading the tool result directly, at the cost of an extra LLM call per run
# and the risk of the model rewriting/hallucinating job data while
# "formatting" it. with_structured_output() and bind_tools() can't be
# stacked on the same model call, so this uses two separate LLM objects.

formatter_llm = groq_llm_llama.with_structured_output(job, method='json_mode')

def agent_method(state: pipeline_state):

    system = '''
                You are a Job Search Agent in a multi-agent recruiting pipeline. Your only
                responsibility is to obtain the raw job postings that downstream agents
                (filter, rank, summary) will work with.

                You have access to two tools to scrape jobs from two different portals :
                - searching_jobs_remotive: scrapes jobs from a remotive job portal and returns a list
                  of dicts, each with an "id" and a "description". It takes no arguments.
                - searching_jobs_jobicy: scrapes jobs from a jobicy job portal and returns a list
                  of dicts, each with an "id" and a "description". It takes no arguments.

                Tool Invoking rule:
                - Being a Job search agent you will always call these two tools to scrape jobs from these 2 portals. 
                
                Decision rules:
                1. If the conversation so far does NOT contain a tool result with scraped
                   jobs, or need to call more tools, call the appropriate tools to finish the work. Never invent job data yourself.
                2. If one or more tool results with scraped jobs is already present, do not call the same
                   tool again. Just reply "done".
            '''
    
    query = "Search Jobs from a portal."
    messages = state['messages'] or [HumanMessage(query)]

    response = llm_with_tool.invoke([SystemMessage(system)] + messages)

    print(f"\n\nLLM responses: {response}")

    if response.tool_calls:
        return {"messages": [response]}

    format_system = '''
        Combine all the scraped jobs from one or multiple tool calls(returned as ToolMessage()) from this conversation and format them into a single JSON with a
        single key "filtered" holding the list of job dicts. Do not alter
        ids or descriptions.
    '''
    formatted = formatter_llm.invoke([SystemMessage(format_system)] + messages)
    # print(f" formatter output:\n {formatted.filtered}")
    return {"messages": [response], "scrapped_jobs": formatted.filtered}

# if __name__=="__main__":


