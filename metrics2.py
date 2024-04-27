
def rogueness_score(summary_dict_all:list[dict], all_agents):
    ''' 
    Return a tuple (to_improve, summaries) of same length that are the agent prompted to improve their answer given the results from the judgements
    '''
    # metric : summarydict -> {(agentid: metric score)}
    # simple -> sum the binary judgemnts. Summary is a sample of them
    metric = {n:0 for n in range(len(all_agents))}
    metric[-1] = 0
    cumulated_metric_dict={n:[] for n in range(len(all_agents))}
    arguments = {n:[] for n in range(len(all_agents))}
    total=0
    for _summary_dict in summary_dict_all:
        metric = {n:0 for n in range(len(all_agents))}
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
                
        for agent in metric.keys():
            cumulated_metric_dict[agent].append(metric[agent])
            total = total + metric[agent]

    
    
    for agent in cumulated_metric_dict.keys():
        cumulated_metric_dict[agent] = sum(cumulated_metric_dict[agent])/total
    
    return cumulated_metric_dict


def imrpovement_score(summary_dict_all:list[dict], all_agents):
    ''' 
    Return a tuple (to_improve, summaries) of same length that are the agent prompted to improve their answer given the results from the judgements
    '''
    # metric : summarydict -> {(agentid: metric score)}
    # simple -> sum the binary judgemnts. Summary is a sample of them

    weight_inc=1.2
    weight_dec=1.8
    weight_const=1

    metric = {n:0 for n in range(len(all_agents))}
    metric[-1] = 0
    cumulated_metric_dict={n:[] for n in range(len(all_agents))}
    arguments = {n:[] for n in range(len(all_agents))}
    
    for _summary_dict in summary_dict_all:
        metric = {n:0 for n in range(len(all_agents))}
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
                
        for agent in metric.keys():
            cumulated_metric_dict[agent].append(metric[agent])

    
 
    for agent in cumulated_metric_dict.keys():
        scores = cumulated_metric_dict[agent]
        for i in range(len(scores)-1):
            if(scores[i]>scores[i+1]):
                imp_score = imp_score + (weight_inc*(scores[i] - scores[i+1]))
            elif(scores[i]<scores[i+1]):
                imp_score = imp_score + (weight_dec*(scores[i] - scores[i+1]))
            else:
                imp_score = imp_score + (weight_const*(scores[i] - scores[i+1])) # here weight doesn't serve a purpose 
        cumulated_metric_dict[agent] = imp_score
        
    
    return cumulated_metric_dict




