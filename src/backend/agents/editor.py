from backend.state_schema import pipeline_state
from backend.llm_instance import groq_llm_opnai

# groq_llm = llm()

def editor_agent(state:pipeline_state):
     
        system_prompt = '''
                    You are an expert in editing resume for candidates actively looking for Job change.your task is to edit
                    the resume content provided a list of missing keywords, gathered across multiple job descriptions the candidate is targeting.after editing you have to return the edited resume content as response.

                    Consider below points while editing the resume:
                    - edit the resume by weaving in every keyword from the list, in a professional way.
                    - use your intelligence to decide what are the best possible places or way to edit the resume with these missing keywords.
                    - you have to decide on your own that where each and every keyword perfectly sits.
                    - not every keyword needs to fit into the same section, spread them across the resume wherever they fit best.
                    - there is no harm in editing the resume on your own, this is for experimental purpose.
                    - try to keep the actual resume content's layout, design intact so that the edited resume content can be dumped to a pdf in subsequent steps.
                    - Just return the edited resume content, don't include anything else like explanations etc.
                    '''

        query = f'''Edit the resume content with the mentioned list of missing keywords.
            Resume:\n {state["profileinfo"]}
            List of missing keywords:\n {state["missing"]}'''
        
        response = groq_llm_opnai.invoke(system_prompt+query)

        print(f"Editor Agent Done")
        return {"updated_resume_content":response.content}