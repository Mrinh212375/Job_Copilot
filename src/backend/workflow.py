from langgraph.graph import StateGraph, START, END

from backend.state_schema import pipeline_state
from backend.agents.extractor import extractor_agent
from backend.agents.job_search_agent import agent_method, toolnode
from backend.agents.Jobfilter_agent import filter_jobs
from backend.agents.JobRank_agent import rank_jobs
from backend.agents.JobSummary_agent import summary_jobs
from backend.agents.analyzer import analyzer_agent
from backend.agents.editor import editor_agent
from backend.agents.writer import pdf_writer_agent


def route(state: pipeline_state):
    if state["messages"][-1].tool_calls:
        return "toolnode"
    return "next_node"


workflow = StateGraph(pipeline_state)

workflow.add_node("extractor", extractor_agent)
workflow.add_node("job_scrapper", agent_method)
workflow.add_node("tool_call_node", toolnode)
workflow.add_node("filter", filter_jobs)
workflow.add_node("rank", rank_jobs)
workflow.add_node("summary", summary_jobs)
workflow.add_node("analyzer", analyzer_agent)
workflow.add_node("editor", editor_agent)
workflow.add_node("writer", pdf_writer_agent)

workflow.add_edge(START, "extractor")
workflow.add_edge("extractor", "job_scrapper")
workflow.add_conditional_edges("job_scrapper", route, {"toolnode": "tool_call_node", "next_node": "filter"})
workflow.add_edge("tool_call_node", "job_scrapper")
workflow.add_edge("filter", "rank")
workflow.add_edge("rank", "summary")
workflow.add_edge("summary", "analyzer")
workflow.add_edge("analyzer", "editor")
workflow.add_edge("editor", "writer")
workflow.add_edge("writer", END)

compiled_graph_pipeline = workflow.compile()
