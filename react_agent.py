import re
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "user", "parts": [{"text": self.system}]})

    def __call__(self, message):
        self.messages.append({"role": "user", "parts": [{"text": message}]})
        result = self.execute()
        self.messages.append({"role": "model", "parts": [{"text": result}]})
        return result

    def execute(self):
        try:
            response = model.generate_content(self.messages)
            if not response.text:
                return "Error: Empty response from model"
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()

def calculate(what):
    try:
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in what):
            raise ValueError("Invalid characters in expression")
        return str(eval(what, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error calculating expression: {e}"

def average_dog_weight(name):
    name = name.lower().strip()
    breed_weights = {
        "scottish terrier": 20,
        "border collie": 37,
        "toy poodle": 7
    }
    for breed, weight in breed_weights.items():
        if breed in name:
            return str(weight)  
    return "50" 

known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}

action_re = re.compile(r'^Action:\s+(\w+):\s+(.+)$')

def query(question, max_turns=5):
    bot = Agent(prompt)
    next_prompt = question
    
    for i in range(max_turns):
        result = bot(next_prompt)
        print(f"Turn {i+1}:\n{result}\n")
        
        action_match = next(
            (m for line in result.split('\n') 
            if (m := action_re.match(line))), 
            None
        )
        if not action_match:
            if "Answer:" in result:
                return result.split("Answer:")[-1].strip()
            break
            
        action, action_input = action_match.groups()
        if action not in known_actions:
            raise ValueError(f"Unknown action: {action}")
            
        print(f"Executing: {action} {action_input}")
        observation = known_actions[action](action_input.strip())
        print(f"Observation: {observation}\n")
        next_prompt = f"Observation: {observation}"

    return "Unable to determine answer after maximum turns."

if __name__ == "__main__":
    question = """I have 2 dogs, a border collie and a scottish terrier. 
    What is their combined weight?"""
    answer = query(question)
    print("\nFinal Answer:", answer)