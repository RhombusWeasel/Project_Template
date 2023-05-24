import re
import math
import requests
from readability import Document
from utils.async_ai import Agent
from urllib.parse import urlparse
from utils.tree.behaviours.tool import Tool

class SummarizeTool(Tool):
    def __init__(self, name, blackboard=None):
        super().__init__(
            name=name, 
            description='Use this to read a website or file. Only text relevant to the query will be returned, all other data is lost.',
            action=self.tick,
            args={"query": "query for information", "source": "http://example.com or file.ext"},
            blackboard=blackboard
        )


    def tick(self, blackboard):
        chunks = blackboard.get('text_chunks', namespace=self.name)
        summarized_chunks = blackboard.get('summarized_chunks', namespace=self.name)
        final_summary = blackboard.get('final_summary', namespace=self.name)
        if chunks is not None:
            if not chunks:  # Check if chunks is empty
                final_summary = self.summarize(blackboard.get("query", namespace=self.name), ' '.join(summarized_chunks))
                blackboard.set('final_summary', final_summary, namespace=self.name)
                blackboard.set('status', f"Summarized {len(summarized_chunks)} chunks.", namespace=self.name)
                blackboard.set('summarized_chunks', None, namespace=self.name)
                return self.SUCCESS
            
            if final_summary is not None:
                return self.SUCCESS

            if summarized_chunks is None:
                summarized_chunks = []

            query = blackboard.get("query", namespace=self.name)
            next_chunk = chunks.pop(0)

            summarized_chunks.append(self.summarize(query, next_chunk))

            blackboard.set('status', f"Summarizing  chunk {len(summarized_chunks)}/{len(summarized_chunks) + len(chunks)}.", namespace=self.name)
            blackboard.set('summarized_chunks', summarized_chunks, namespace=self.name)
            blackboard.set('text_chunks', chunks, namespace=self.name)
        else:
            source = blackboard.get("source", namespace=self.name)
            chunks = self.get_text_from_source(source)
            blackboard.set("text_chunks", chunks, namespace=self.name)
            blackboard.set("status", f"Summarizing {source} in {len(chunks)} chunks.", namespace=self.name)
        return self.RUNNING


    def summarize(self, query, data):
        a = summary_agent(query, data)
        return a.get_summary()


    def get_text_from_source(self, source, max_tokens=1000):
        s = 'url' if self.is_url(source) else 'file'
        if s == 'url':
            text = self.get_text_from_url(source)
        else:
            text = self.get_text_from_file(source)

        # Divide the text into chunks of max_tokens
        text_chunks = []
        scan_range = math.floor(max_tokens/20)
        for i in range(0, len(text), max_tokens):
            start = i > scan_range and i - scan_range or i
            end = i+max_tokens+scan_range < len(text) and i+max_tokens+scan_range or len(text)
            text_chunks.append(text[start:end])
        return text_chunks


    def is_url(self, source):
        try:
            result = urlparse(source)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


    def get_text_from_url(self, url):
        r = requests.get(url)
        doc = Document(r.text)
        text = doc.summary()
        cleaned_text = re.sub('<[^>]*>', ' ', text)
        return cleaned_text


    def get_text_from_file(self, file_path):
        with open(file_path, 'r') as file:
            text = file.read()
        return text


class summary_agent(Agent):
    def __init__(self, query, data):
        super().__init__(name_prefix='SUM', print_tokens=True, model='gpt-3.5-turbo')
        self.values = {'query': query, 'data': data}


    def get_summary(self):
        p = f"""
        Goal:
        - Summarize the provided data as succinctly as possible
        - Preserve meaning and technical details included in the text
        - Retain links related to the query
        - Include only data related to the query in the returned text
        - ALWAYS include code examples in the returned text

        Query: {self.values['query']}

        Data: {self.values['data']}
        """
        response = self.get_response(p)
        return response
