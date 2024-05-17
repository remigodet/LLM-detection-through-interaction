from openai import OpenAI
client = OpenAI()

token_usage = {"completion_tokens":0, "prompt_tokens":0}
model_cost = {"gpt-4": (0.03,0.06), "gpt-4-turbo": (0.01, 0.03), "gpt-3.5-turbo": (0.0005,0.0015), "gpt-4o": (0.01, 0.02),}
cost = 0
def get_completion(agent_prompt, prompt, engine, temperature=0, debug=False):
    '''
    Returns a completion for the given prompts
    '''
    global token_usage
    global cost
    
    messages=[
        {"role": "system", "content": agent_prompt},
        {"role": "user", "content": prompt},
    ]
    if debug:
        return "$$ LLM COMPLETION $$"
    # OPEN AI call
    completion = client.chat.completions.create(messages=messages, model=engine, temperature=temperature)
    
    # print(completion)
    token_usage["completion_tokens"] += completion.usage.completion_tokens
    token_usage["prompt_tokens"] += completion.usage.prompt_tokens
    in_cost, out_cost = model_cost.get(engine)
    cost += in_cost * completion.usage.prompt_tokens/1000 + out_cost * completion.usage.completion_tokens/1000
    
    return completion.choices[0].message.content
    
def print_cost():
    print(token_usage)
    print(cost)
    
if __name__ =="__main__":
    get_completion("You are a chat assistant.", "Give me 2 random words", "gpt-3.5-turbo")
    get_completion("You are a chat assistant.", "Give me 2 random words", "gpt-3.5-turbo")