import os
import json
from utils.async_ai import Agent
from utils.logger import Logger
from utils.tree.composites.base import Composite
from utils.json_validator import parse_json_string
from utils.db import save_data_to_db, load_data_from_db

prompt = """
SYSTEM: Answer the below users query to the best of your ability.

GOAL:

{query}

SYSTEM: You have ONLY the following tools available to use in order to complete your task.
TOOLS:

{tools}

SYSTEM: PLAN:

{plan}

SYSTEM: Follow the below rules and use the tools to achieve the goal.
Rules:
  1.  Create a step by step long term plan if there isn't one already in place to achieve your goal, set step one to your short_term_goal and list the remaining steps as your long_term_goal.
  2.  Check the available data to see if the task is complete, if it is, skip the following and respond with the answer tool.
  3.  Only the tools defined above are available to you, always include the ANSWER_TOOL at the end of the long term plan. You may never respond with no tool, 
      if you are stuck simply use ANSWER_TOOL and state you do not know.
  4.  You may not make the same tool call twice in a row, if you are stuck simply use ANSWER_TOOL and state you do not know.
  5.  Remove the next step of the plan from the list and specify it as your tool output specifying any arguments required by the tool.
  6.  Evaluate the results of the previous steps (detailed below marked HISTORY) and update the long term plan accordingly by removing completed steps.
      If the task is complete use the ANSWER_TOOL immediately and inform the user.

SYSTEM: HISTORY:

{history}

SYSTEM: Your output must be in the json format specified below.
{
  "text": "Your thoughts on the current step",
  "short_term_goal": "a brief description of your current step",
  "tool": {
    "name": "TOOL_NAME",
    "args": {
      "arg1": "value1"
    }
  },
  "long_term_goal": [
    { ... },
    {
      "name": "ANSWER_TOOL",
      "args": {
        "answer": "the answer to the users query"
      }
    }
  ],
  "reasoning": "Explain why you chose this tool and what you hope to achieve with it",
  "critisism": "Constructively criticise your performance so far, what could you have done better?",
  "summary": "A summary of the steps you have taken so far and what you have learned from them."
}

SYSTEM: Remove completed steps from the long term plan and update the short term goal to the next step in the plan.
SYSTEM: Ensure your response can be parsed by python's json.loads() function.
RESPONSE:
"""

class AISelector(Composite):
  def __init__(self, name='AI Selector', prompt='Select an AI', data={}, blackboard=None, tree_id=None):
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
    self.iterations = 0
    self.tree_id = tree_id
    self.plan = []
    self.history = []
    self.children = []
    self.update_db()

  def update_db(self):
    save_data_to_db('blackboards', self.tree_id, 'blackboard', self.blackboard.data)
    save_data_to_db('blackboards', self.tree_id, 'prompt', self.last_prompt)


  def get_tools(self):
    tools = []
    for child in self.children:
      name = child.name
      description = child.description if hasattr(child, 'description') else 'No description available'
      args = child.args if hasattr(child, 'args') else {}
      tools.append(f"{name}: {description}: {args}")
    return tools


  def parse_response(self, data, blackboard):
    if 'tool' not in data:
      self.logger.error(f"Invalid response from AI: {data}")
      return None
    if 'args' in data['tool']:
      for arg in data['tool']['args']:
        blackboard.set(arg, data['tool']['args'][arg], namespace=data['tool']['name'])
    
    return data['tool']
  

  def query_ai(self, query):
    tools = self.get_tools()
    self.logger.info(f"Querying AI with: {query}")
    self.last_prompt = prompt
    # Insert the query into the prompt at the {query} label
    self.last_prompt = self.last_prompt.replace('{query}', query)
    # Insert the tools list into the prompt at the {tools} label
    self.last_prompt = self.last_prompt.replace('{tools}', "\n".join(tools))
    # Insert the plan into the prompt at the {plan} label
    self.last_prompt = self.last_prompt.replace('{plan}', json.dumps(self.plan, indent=2))
    # Insert the blackboard into the prompt at the {blackboard} label
    self.last_prompt = self.last_prompt.replace('{history}', json.dumps(self.history, indent=2))
    self.response_id = self.ai.submit_request(self.last_prompt, self.tree_id)
    self.response_counter = 0
    self.iterations += 1
    self.get_response = False
    self.response_processed = False
    self.logger.info(f"Response History: {self.history}")


  def tick(self, blackboard):
    if self.get_response and self.response_processed:
      global prompt
      # Get the list of tools from the children
      query = blackboard.get('objective')
      self.query_ai(query)
      blackboard.set('status', 'Waiting for AI response...')
      self.update_db()
      return self.RUNNING
    else:
      self.response_counter += 1
      ai_response = self.ai.check_response_status(self.tree_id)
      self.logger.info(f"AI response: {ai_response}")
      if ai_response:
        # Return running if we are waiting on a response.
        if 'uuid' in ai_response and ai_response['uuid'] == 'pending':
          blackboard.set('status', f'waiting for AI response... ({self.response_counter})')
          self.update_db()
          return self.RUNNING
        # Parse the response to find the selected child
        tool = self.parse_response(ai_response, blackboard)
        if not tool:
          # Bad response from AI, try again
          blackboard.set('status', f'Bad response from AI, trying again... ({self.response_counter})')
          self.get_response = True
          self.response_processed = True
          self.update_db()
          return self.RUNNING
        selected_child_name = tool['name']
        if 'long_term_goal' in ai_response:
          self.plan = ai_response['long_term_goal']
        # Check if the selected child name is in the list of child names
        child_names = [child.name for child in self.children]
        if selected_child_name not in child_names:
          self.logger.error(f"Invalid child name received from AI: {selected_child_name}")
          blackboard.set('status', f'Invalid child name received from AI: {selected_child_name}')
          self.get_response = True
          self.update_db()
          return self.FAILURE
        # Find and execute the selected child
        for child in self.children:
          if child.name == selected_child_name:
            status = child.tick(blackboard)
            blackboard.set('status', f'Executed {child.name} with status {status}')
            if status != self.RUNNING:
              self.get_response = True
              self.response_processed = True
              tool['output'] = blackboard.get_namespace(tool['name'])
              blackboard.delete_namespace(tool['name'])
              self.history.append(tool)
              blackboard.set('history', self.history)
              if child.name == 'ANSWER_TOOL':
                blackboard.set('status', 'AI response processed.')
                self.update_db()
                return self.SUCCESS
      else:
        blackboard.set('status', f'waiting for AI response... ({self.response_counter})')
    self.update_db()
    return self.RUNNING