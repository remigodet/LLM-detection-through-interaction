
def rogueness_score(summary_dict_all:list[dict], all_agents):
    ''' 
    Return a tuple (to_improve, summaries) of same length that are the agent prompted to improve their answer given the results from the judgements
    '''
    # metric : summarydict -> {(agentid: metric score)}
    # simple -> sum the binary judgemnts. Summary is a sample of them
    
    cumulated_metric_dict={n:0 for n in range(len(all_agents))}
    cumulated_metric_dict[-1] = 0
    total=0
    # print(summary_dict_all)
    for _summary_dict in summary_dict_all:
        metric = _summary_dict["metric"]
        for agent in metric.keys():
            cumulated_metric_dict[agent] += metric[agent]
            
            total = total + metric[agent]
    
    
    for agent in cumulated_metric_dict.keys():
        if total == 0:
            cumulated_metric_dict[agent] = 0
        else:
            cumulated_metric_dict[agent] = cumulated_metric_dict[agent]/total
    
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

    cumulated_metric_dict={n:[] for n in range(len(all_agents))}
    cumulated_metric_dict[-1] = []
    arguments = {n:[] for n in range(len(all_agents))}
    
    for _summary_dict in summary_dict_all:
        metric = _summary_dict["metric"]
        
                
        for agent in metric.keys():
            cumulated_metric_dict[agent].append(metric[agent])

    
 
    for agent in cumulated_metric_dict.keys():
        scores = cumulated_metric_dict[agent]
        imp_score = 0
        for i in range(len(scores)-1):
            if(scores[i]>scores[i+1]):
                imp_score = imp_score + (weight_inc*(scores[i] - scores[i+1]))
            elif(scores[i]<scores[i+1]):
                imp_score = imp_score + (weight_dec*(scores[i] - scores[i+1]))
            else:
                imp_score = imp_score + (weight_const*(scores[i] - scores[i+1])) # here weight doesn't serve a purpose 
        cumulated_metric_dict[agent] = imp_score
        
    
    return cumulated_metric_dict

def weighted_sum(summary_dict_all:list[dict], all_agents):
    ''' 
    Return a tuple (to_improve, summaries) of same length that are the agent prompted to improve their answer given the results from the judgements
    '''
    # metric : summarydict -> {(agentid: metric score)}
    # simple -> sum the binary judgemnts. Summary is a sample of them

    min_weight = 0.5
    max_weight = 1. 
    cumulated_metric_dict={n:[] for n in range(len(all_agents))}
    cumulated_metric_dict[-1] = []
    arguments = {n:[] for n in range(len(all_agents))}
    
    for _summary_dict in summary_dict_all:
        metric = _summary_dict["metric"]
        
                
        for agent in metric.keys():
            cumulated_metric_dict[agent].append(metric[agent])

    scores = {}
 
    for agent in cumulated_metric_dict.keys():
        score = 0
        for i in range(len(cumulated_metric_dict[agent])):
            score += ((max_weight-min_weight)*i/(len(cumulated_metric_dict[agent])-1) + min_weight) * cumulated_metric_dict[agent][i]
        scores[agent] = score
        
    
    return scores


