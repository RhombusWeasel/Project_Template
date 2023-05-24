import os
import json
from utils.async_ai import Agent
from utils.logger import Logger
from utils.tree.composites.base import Composite
from utils.json_validator import parse_json_string
from utils.db import save_data_to_db

prompt = """
SYSTEM: Answer the below users query to the best of your ability.

GOAL:

{query}

SYSTEM: You have ONLY the following tools available to use in order to complete your task.
TOOLS:

{tools}

SYSTEM: Follow the below rules and use the tools to achieve the goal.
Rules:
  1. Create a step by step plan to achieve the goal.
  2. Only the tools defined above are available to you, always include the ANSWER_TOOL at the end of the plan.
  3. Do not read files unless explicitly asked to do so, this is a privacy concern.
  4. Do not assume a file exists unless explicitly told it does.
  5. Steps are executed sequentially, in any fail, the whole chain fails.

SYSTEM: Your output must be in the json format specified below.
{
  "plot": [
    "Break down the query",
    "Into it's component steps.",
    "To aid in planning below."
  ],
  "plan": [
    { ... },
    {
      "name": "ANSWER_TOOL",
      "args": {
        "answer": "Leave this empty, the answer will be calculated elsewhere."
      }
    }
  ],
  "thoughts": "Your thoughts on the plan",
  "reasoning": "Explain why you chose this plan and other situations it might be useful in",
  "critisism": "Constructively criticise this plan, what could have been done better?"
}

SYSTEM: Ensure your response can be parsed by python's json.loads() function.
RESPONSE:
"""

class AIPlanner(Composite):
  def __init__(self, name='AI Planner', prompt='Select an AI', data={}, blackboard=None, tree_id=None):
    super().__init__(name)
    self.prompt = prompt
    self.last_prompt = prompt
    self.data = data
    self.blackboard = blackboard
    self.query = ''
    self.logger = Logger(name, log_level=Logger.DEBUG)
    self.ai = Agent(name_prefix='AIS', log_level=Logger.DEBUG, print_tokens=True, model='gpt-4')
    self.get_response = True
    self.response_processed = True
    self.response_counter = 0
    self.tree_id = tree_id
    self.plan = []
    self.history = []
    self.children = []


  def get_tools(self):
    tools = []
    for child in self.children:
      name = child.name
      description = child.description if hasattr(child, 'description') else 'No description available'
      args = child.args if hasattr(child, 'args') else {}
      tools.append(f"{name}: {description}: {args}")
    return tools
  

  def tick(self, blackboard):
    tree_id = blackboard.get('tree_id')
    if self.get_response and self.response_processed:
      global prompt
      # Get the list of tools from the children
      query = blackboard.get('objective')
      tools = self.get_tools()

      self.last_prompt = prompt
      # Insert the query into the prompt at the {query} label
      self.last_prompt = self.last_prompt.replace('{query}', query)
      # Insert the tools list into the prompt at the {tools} label
      self.last_prompt = self.last_prompt.replace('{tools}', "\n".join(tools))
      # Submit the prompt to the AI
      self.response_id = self.ai.submit_request(self.last_prompt, tree_id)
      self.response_counter = 0
      self.get_response = False
      self.response_processed = False
      # Update the blackboard
      blackboard.set('status', f'Waiting for AI response... {self.response_id}')
      self.logger.info(f"Prompt sent to AI.")
      save_data_to_db('blackboards', tree_id, 'prompt', self.last_prompt)
      return self.RUNNING
    else:
      self.response_counter += 1
      ai_response = self.ai.check_response_status(tree_id)
      self.logger.info(f"AI response: {ai_response}")
      if ai_response and 'plan' in ai_response:
        self.logger.info(f"AI response: {ai_response}")
        if 'plan' in ai_response:
          blackboard.set('plan', ai_response['plan'])
          blackboard.set('status', 'AI response received.')
          self.logger.info(f"Plan written to blackboard: {ai_response['plan']}")
          self.get_response = True
          self.response_processed = True
        else:
          blackboard.set('status', 'AI response received, but no plan was found, retrying...')
          self.get_response = True
          self.response_processed = True
      else:
        blackboard.set('status', f'waiting for AI response... ({self.response_counter})')
    return self.RUNNING