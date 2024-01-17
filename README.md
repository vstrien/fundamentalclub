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

## Overall plan:

* Use the `autogen` framework to create a set of bots
  * These bots have the ability to search the internet for themselves
  * Also, operating on GPT, they do have quite some general knowledge about the world
  * Fundamental qualities of stocks don't change that much
  * Quantitative current information (for example information about cycles) can be found easily using internet searches, probably the agents can handle that
* For fundamental analysis, reports from companies and things like earnings calls are important as well. We can solve that, if we know beforehand what companies we want to analyze:
  * Reports and filings can be loaded on beforehand to a vector database
* Pre-load the vector database with annual reports and other important fundamental information