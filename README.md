# fundamentalclub
A small exercise where virtual investment advisors discuss with each other about stocks and companies

Needed:
* A setup of the [ChatGPT Retrieval Plugin](https://github.com/openai/chatgpt-retrieval-plugin#quickstart)
  * Connected to a vector database like Pinecone
  * Connected to OpenAI
  * A setup can be found at [Enhancing ChatGPT with Infinite External Memory](https://betterprogramming.pub/enhancing-chatgpt-with-infinite-external-memory-using-vector-database-and-chatgpt-retrieval-plugin-b6f4ea16ab8)
* A file 'secrets.py' with the following components:

```python
OPENAI_API_KEY = "<your_openai_api>"
DATABASE_INTERFACE_BEARER_TOKEN = "<your_database_interface_api_key>"
```
