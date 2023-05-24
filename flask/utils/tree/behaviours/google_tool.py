import requests
from bs4 import BeautifulSoup
from utils.tree.behaviours.tool import Tool

class GoogleSearchTool(Tool):
  def __init__(self, name='', blackboard=None):
    super().__init__(
      name=name,
      description='This tool searches Google and returns the first 5 URLs found.',
      args={'query': 'search_query'},
      action=self.google_search,
      blackboard=blackboard
    )

  def google_search(self, blackboard):
    blackboard.set('status', 'Searching Google...', namespace=self.name)
    query = blackboard.get('query', namespace=self.name)

    num_results = 5
    base_url = "https://www.google.com/search"
    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    params = {
      "q": query + ' -.gov',
      "num": num_results
    }
    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")
      search_results = []

      for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text
        link = g.find('a')['href']
        search_results.append({"title": title, "link": link})

      blackboard.set('search_results', search_results, namespace=self.name)
      return self.SUCCESS
    else:
      blackboard.set('status', 'Failed to search Google.', namespace=self.name)
      blackboard.set('output', 'Error fetching search results.', namespace=self.name)
      return self.FAILURE