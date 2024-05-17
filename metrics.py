import random
def process_judgments(_judgments_dict, all_agents):
    ''' 
    Return a tuple (to_improve, summaries) of same length that are the agent prompted to improve their answer given the results from the judgements
    '''
    # metric : summarydict -> {(agentid: metric score)}
    # simple -> sum the binary judgemnts. Summary is a sample of them
    metric = {n:0 for n in range(len(all_agents))}
    metric[-1] = 0
    
    arguments = {n:[] for n in range(len(all_agents))}
    
    
    for judge, agent1, agent2 in _judgments_dict.keys():
        
        result = _judgments_dict[(judge, agent1, agent2)][0]
        if "$AGENT_TWO$" in result:
            print("Chosen AGENT 1")
            metric[agent1] += 1
            arguments[agent1].append(result)
        elif "$AGENT_ONE$" in result:
            print("Chosen AGENT 2")
            metric[agent2] += 1
            arguments[agent2].append(result)
        else:
            print("No definite answer")
            metric[-1] += 0
            
    to_improve = [max(list(metric.items()), key=lambda x: x[1])[0]]
    for i in to_improve:
        assert i >= 0
        assert i < len(all_agents)
    # 
    summaries = ["\n\n".join(arguments[i]) for i in to_improve]
    print("metrics", metric)
    print(to_improve)     
    return to_improve, summaries, metric

