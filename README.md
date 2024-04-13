# fundamentalclub
A small exercise where virtual investment advisors discuss with each other about stocks and companies

Needed:
* A setup of the [ChatGPT Retrieval Plugin](https://github.com/openai/chatgpt-retrieval-plugin#quickstart)
  * Connected to a vector database like Pinecone
  * Connected to OpenAI
  * A setup can be found at [Enhancing ChatGPT with Infinite External Memory](https://betterprogramming.pub/enhancing-chatgpt-with-infinite-external-memory-using-vector-database-and-chatgpt-retrieval-plugin-b6f4ea16ab8)
* Environment variables (or a `.env` file) with the following components:

```python
OPENAI_API_KEY = "<your_openai_api>"
DATABASE_INTERFACE_BEARER_TOKEN = "<your_database_interface_api_key>"
PINECONE_API_KEY = "<your_pinecone_api_key>"
```

* a file `config_fundamentalclub.py` with the following components:

```python
GENERAL_INDEX_URL = "<URL_TO_YOUR_PINECONE_INDEX>"
GENERAL_INDEX_NAME = "<name_of_your_index>"
```

Also, add a folder called 'sample data' with data about stocks you want to analyze. It could be anything that's remotely interesting:

* Forms like 10-K, 10-Q, etc.
* Transcripts of earnings calls
* Letters to shareholders
* Interesting facts about related businesses
* Etc.

## Overall plan:

* Use the `autogen` framework to create a set of bots
  * These bots have the ability to [search the internet for themselves](https://github.com/microsoft/autogen/blob/main/notebook/agentchat_surfer.ipynb)
  * Also, operating on GPT, they do have quite some general knowledge about the world
  * Fundamental qualities of stocks don't change that much
  * Quantitative current information (for example information about cycles) can be found easily using internet searches, probably the agents can handle that
* For fundamental analysis, reports from companies and things like earnings calls are important as well. Ways to solve this:
  * Integrate with existing stock-information API's (yfinance, interactivebrokers, ...)
  * Web searches for reports and filings
  * On-demand additions to the vector database
    * Keep a list of all stocks and stored information on hand, for example:  

      Stock | Report or filing | Timeframe | Date of retrieval | source URL
      ---|---|---|---|---
      RELL | 10-Q | FY2024 Q2 | 2024-01-11 | https://www.rell.com/webfoo/wp-content/uploads/2024/01/10Q-Q2-FY24-Final-Filed-01.11.24.docx  
    * Load contents into the vector database
    * Try to find more resources periodically

## Tests to add:

DbBackedGuide:

- [ ] Check if with data in Cosmos (mock), no call is made to ChatGPT (mock)