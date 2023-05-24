from utils.tree.behaviours.tool import Tool

def default_function(blackboard):
    return True

class AnswerTool(Tool):
    def __init__(self, name, blackboard=None):
        super().__init__(
            name, 
            'This tool returns an answer or a notice of completion to the user.',
            action=self.answer_query,
            args={"answer": "answer"},
            blackboard=blackboard
        )

    def answer_query(self, blackboard):
        # Execute the action associated with this tool
        return self.SUCCESS
