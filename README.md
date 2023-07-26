# google

Convenience wrapper for Googling using the requests library.

Useful as a tool for LLM research agents, but prone to being blocked by Google if you send too many requests.


```python
from google import Google

# Initialize search object.
search_engine = Google(num_results=20, sleep_interval=5, timeout=10)

# Return top urls for a given search.
search_engine.search('github')

# Return request reponses for top urls.
search_engine.advanced_search('github')

```
