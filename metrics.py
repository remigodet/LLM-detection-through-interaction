import random
def process_summaries(_summary_dict, all_agents):
    ''' 
    Return a tuple (to_improve, summaries) of same length that are the agent prompted to improve their answer given the results from the judgements
    '''
    # metric : summarydict -> {(agentid: metric score)}
    # simple -> sum the binary judgemnts. Summary is a sample of them
    metric = {n:0 for n in range(len(all_agents))}
    metric[-1] = 0
    
    arguments = {n:[] for n in range(len(all_agents))}
    
    
    for judge, agent1, agent2 in _summary_dict.keys():
        result = _summary_dict[(judge, agent1, agent2)][0]
        print(result)
        if "ONE" in result:
            metric[agent1] += 1
            arguments[agent1].append(result)
        elif "TWO" in result:
            metric[agent2] += 1
            arguments[agent2].append(result)
        else:
            print("No definite answer")
            metric[-1] += 0
            
    to_improve = [max(list(metric.items()), key=lambda x: x[1])[0]]
    for i in to_improve:
        assert i >= 0
        assert i < len(all_agents)
    summaries = [random.sample(arguments[i],1) for i in to_improve]
                
    print(to_improve)     
    return to_improve, summaries

