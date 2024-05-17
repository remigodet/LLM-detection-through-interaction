import prompts
from llm import get_completion, print_cost
from metrics import process_judgments
import numpy as np
import random
import pickle

N_VICTIM_AGENTS = 3
N_ROGUE_AGENTS = 1
N_ROUNDS = 15
summary_dict_all = []
class Agent():
    def __init__(self, id, victim:bool) -> None:
        self.id = id
        self.victim = victim
        self.memory = [] # stores the latest performances 
        self.judgments = [] # stores judgments
        def get_engine(victim):
            if victim: 
                return "gpt-3.5-turbo"
            else:
                return "gpt-4o"
        self.temperature = 0. if self.victim else 0.
        self.engine = get_engine(victim)
        self.agent_prompt = "You are a chat assistant" # TODO change this to a better prompt 
        
    
    def completion(self, prompt, judgment=False):
        completion = get_completion(agent_prompt=self.agent_prompt, prompt=prompt, engine= self.engine, temperature=self.temperature)
        #
        # print("========================================")
        # print(self.id)
        # print("---")
        # print(prompt)
        # print("->")
        # print(completion)
        # print("========================================")
        # 
        if judgment:
            self.judgments.append(completion)
        else:
            self.memory.append(completion)
        return completion
    
    def __str__(self) -> str:
        return '''
    '''.join(self.memory)
        
def round_robin_policy(all_agents, sample=False):
    '''
    Must return a list of triplets (judge, agent1, agent2) of agents
    '''
    from itertools import permutations
    # TODO round robin can depend on performance of previous round ? 
    judges = [i for i in range(N_VICTIM_AGENTS)]
    adversaries = [i+N_VICTIM_AGENTS for i in range(N_ROGUE_AGENTS)]
    ids = permutations(list(range(N_ROGUE_AGENTS+N_VICTIM_AGENTS)), 3)
    ids = [id for id in ids if id[0] not in adversaries]
    ids = [id for id in ids if id[1]<id[2]]
    res = [(all_agents[id[0]],all_agents[id[1]],all_agents[id[2]]) for id in ids]
    if sample:
        return random.sample(res, sample)
    else: return res

def add_to_judgement_dict(summary__dict, key, result):
    if key in summary__dict.keys():
        summary__dict[key].append(result)
    else:
        summary__dict[key] = [result]
        
def main():
    
    victim_agents = [Agent(id = i, victim=True) for i in range(N_VICTIM_AGENTS)]
    rogue_agents =  [Agent(id = i, victim=False) for i in range(N_VICTIM_AGENTS, N_VICTIM_AGENTS + N_ROGUE_AGENTS)]
    all_agents = victim_agents + rogue_agents
    
    # # first step
    # first_prompt = prompts.first_prompt()
    # for agent in all_agents:
    #     agent.completion(first_prompt)
        
    
    # # round robin loop 
    
    # for r in range(N_ROUNDS):
    #     print(f"############### ROUND {r} #############")
    #     _judgments_dict = {}
    #     # comparisons 
    #     for judge,agent1,agent2 in round_robin_policy(all_agents, sample=False):
    #         print(judge.id, agent1.id, agent2.id)
    #         comparison_prompt = prompts.comparison_prompt(judge, agent1, agent2)
            
    #         result = judge.completion(comparison_prompt, judgment=True)
    #         # store the judgment for summary
    #         add_to_judgement_dict(_judgments_dict, (judge.id, agent1.id, agent2.id), result)
                
        
    #     # process summaries
    #     to_improve, summaries, metric = process_judgments(_judgments_dict, all_agents)
    #     # save 
    #     _judgments_dict["info"] = (N_VICTIM_AGENTS, N_ROGUE_AGENTS, r, to_improve)
    #     _judgments_dict["metric"] = metric
    #     summary_dict_all.append(_judgments_dict)
        
    #     # improvements 
    #     for i in range(len(to_improve)):
    #         agent = all_agents[to_improve[i]]
    #         summary = summaries[i]
    #         improvement_prompt = prompts.improvement_prompt(summary, agent)
    #         agent.completion(improvement_prompt)
    #     print("CURRENT ROUND COST")
    #     print_cost()
    # print("saving")
    
    # with open('experiment_35vs4o.pickle', 'wb') as handle:
    #     pickle.dump(summary_dict_all, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # print("saving complete")
    print("loading")
    with open('experiment_35vs4o.pickle', 'rb') as handle:
        b = pickle.load(handle)
        
    for d in b:
        print(d["metric"])
    from final_vote import rogueness_score, imrpovement_score, weighted_sum
    print(rogueness_score(b, all_agents))
    print(imrpovement_score(b, all_agents))
    print(weighted_sum(b, all_agents))
    


main()
print("Final cost")
print_cost()
    