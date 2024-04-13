# generate prompts for given situations
def first_prompt():
    return "$$ This is the first prompt ! $$"

def comparison_prompt(judge, agent1, agent2):
    # use Agent.memory to get most recent answer
    return f'''Completion prompt between :
{agent1.id}
and
{agent2.id}
by 
{judge.id}'''

def improvement_prompt(summary, agent):
    return f"$$ This is the improvement prompt from {summary} for agent {agent.id}$$"