import prompts
from llm import get_completion, print_cost
from metrics import process_summaries
import numpy as np

N_VICTIM_AGENTS = 2
N_ROGUE_AGENTS = 1
N_ROUNDS = 2

class Agent():
    def __init__(self, id, victim:bool) -> None:
        self.id = id
        self.victim = victim
        self.memory = [] # stores the latest performances 
        self.judgments = [] # stores judgments
        self.engine = "gpt-3.5-turbo"
        self.agent_prompt = "You are a chat assistant" # TODO change this to a better prompt 
        
    def completion(self, prompt, judgment=False):
        completion = get_completion(agent_prompt=self.agent_prompt, prompt=prompt, engine= self.engine)
        #
        print("========================================")
        print(self.id)
        print("---")
        print(prompt)
        print("->")
        print(completion)
        print("========================================")
        # 
        if judgment:
            self.judgments.append(completion)
        else:
            self.memory.append(completion)
        # TODO save here probably !! 
        return completion
    
    def __str__(self) -> str:
        return '''
    '''.join(self.memory)
        
def round_robin_policy(all_agents):
    '''
    Must return a list of triplets (judge, agent1, agent2) of agents
    '''
    from itertools import permutations
    # TODO round robin can depend on performance of previous round ? 
    return list(permutations(all_agents))

def add_to_summary_dict(summary__dict, key, result):
    if key in summary__dict.keys():
        summary__dict[key].append(result)
    else:
        summary__dict[key] = [result]
        
def main():
    
    victim_agents = [Agent(id = i, victim=True) for i in range(N_VICTIM_AGENTS)]
    rogue_agents =  [Agent(id = i, victim=False) for i in range(N_VICTIM_AGENTS, N_VICTIM_AGENTS + N_ROGUE_AGENTS)]
    all_agents = victim_agents + rogue_agents
    
    # first step
    first_prompt = prompts.first_prompt()
    for agent in all_agents:
        agent.completion(first_prompt)
        
    
    # round robin loop 
    _summary_dict = {}
    
    for r in range(N_ROUNDS):
        # comparisons 
        for judge,agent1,agent2 in round_robin_policy(all_agents):
            
            comparison_prompt = prompts.comparison_prompt(judge, agent1, agent2)
            
            result = judge.completion(comparison_prompt, judgment=True)
            # store the judgment for summary
            add_to_summary_dict(_summary_dict, (judge.id, agent1.id, agent2.id), result)
                
               
        # cost 
        print_cost()
        # process summaries
        to_improve, summaries = process_summaries(_summary_dict, all_agents)
        # improvements 
        for i in range(len(to_improve)):
            agent = all_agents[to_improve[i]]
            summary = summaries[i]
            improvement_prompt = prompts.improvement_prompt(summary, agent)
            agent.completion(improvement_prompt)



    
    
main()
print("Final cost")
print_cost()

# TODO (in order)
# save everything
# vote

    