from fundamentalclub.chatutils.chat_utils import ChatGPT
import json
import os
from fundamentalclub.cosmosbackend.cosmosbackend import CosmosBackendFundamentalGuide
import logging
import asyncio

def strip_markdown(text):
    return text.replace("```json", "").replace("```", "")

class Guide(ChatGPT):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the queries.json file
    queries_path = os.path.join(script_dir, 'queries.json')

    with open(queries_path, "r") as file:
        queries = json.load(file)

    def __init__(self, api_key, ticker_name, num_retries_before_failing = 3):
        super().__init__(api_key, Guide.queries["GPT_ROLE"])
        self.name = "Guide"
        self.ticker_name = ticker_name
        self.industry = None
        self.key_financial_indicators = None
        self.risks = None
        self.competitors = None
        self.num_retries_before_failing = num_retries_before_failing

    async def get_industry(self):
        if self.industry is None or len(self.industry) == 0:
            self.industry = await self._get_gpt_response_with_retries(Guide.queries["GET_INDUSTRY_PROMPT"].format(ticker = self.ticker_name))
        return self.industry

    async def get_key_financial_indicators(self):
        if self.key_financial_indicators is None or len(self.key_financial_indicators) == 0:
            self.key_financial_indicators = await self._get_gpt_response_with_retries(Guide.queries["GET_KFIS_PROMPT"].format(ticker_name = self.ticker_name, industry = self.get_industry()))
        return self.key_financial_indicators

    async def get_risks(self):
        if self.risks is None or len(self.risks) == 0:
            self.risks = await self._get_gpt_response_with_retries(Guide.queries["GET_RISKS_PROMPT"].format(ticker_name = self.ticker_name, industry = self.get_industry()))
        return self.risks

    async def _get_gpt_response_with_retries(self, prompt):
        loop = asyncio.get_event_loop()
        succeeded = False
        gpt_response = None
        n_retry = 0
        while n_retry < self.num_retries_before_failing and not succeeded:
            gpt_response = await loop.run_in_executor(None, self.call_chatgpt_api, prompt)
            try:
                gpt_response = json.loads(strip_markdown(gpt_response))
                succeeded = True
            except Exception as e:
                logging.error(f"""Error getting response for {prompt}: {e}\nChatGPT output: {gpt_response}""")
                n_retry += 1

        return gpt_response

    async def get_competitors(self):
        if self.competitors is None or len(self.competitors) == 0:
            self.competitors = await self._get_gpt_response_with_retries(Guide.queries["GET_COMPETITORS_PROMPT"].format(ticker_name = self.ticker_name, industry = self.get_industry()))
        return self.competitors

class DbBackedGuide(Guide):
    def __init__(self, api_key, ticker_name, database: CosmosBackendFundamentalGuide):
        super().__init__(api_key, ticker_name)
        self.database = database
    
    async def get_industry(self):
        if self.industry is None:
            self.industry = self.database.get_industry(self.ticker_name)
        if self.industry is None or len(self.industry) == 0:
            self.industry = await super().get_industry()
            self.database.set_industry(self.ticker_name, self.industry)
        return self.industry
    
    async def get_key_financial_indicators(self):
        if self.key_financial_indicators is None:
            self.key_financial_indicators = self.database.get_kfis(self.ticker_name)
        if self.key_financial_indicators is None or len(self.key_financial_indicators) == 0:
            self.key_financial_indicators = await super().get_key_financial_indicators()
            self.database.set_kfis(self.ticker_name, self.key_financial_indicators)
        return self.key_financial_indicators
    
    async def get_risks(self):
        if self.risks is None:
            self.risks = self.database.get_risks(self.ticker_name)
        if self.risks is None or len(self.risks) == 0:
            self.risks = await super().get_risks()
            self.database.set_risks(self.ticker_name, self.risks)
        return self.risks
    
    async def get_competitors(self):
        if self.competitors is None:
            self.competitors = self.database.get_competitors(self.ticker_name)
        if self.competitors is None or len(self.competitors) == 0:
            self.competitors = await super().get_competitors()
            self.database.set_competitors(self.ticker_name, self.competitors)
        return self.competitors
    
    async def get_all(self):
        industry_future = asyncio.ensure_future(self.get_industry())
        kfi_future = asyncio.ensure_future(self.get_key_financial_indicators())
        risks_future = asyncio.ensure_future(self.get_risks())
        competitors_future = asyncio.ensure_future(self.get_competitors())

        await asyncio.gather(industry_future, kfi_future, risks_future, competitors_future)

        return {
            "ticker": self.ticker_name,  # "AAPL"
            "industry": industry_future.result(),
            "key_financial_indicators": kfi_future.result(),
            "risks": risks_future.result(),
            "competitors": competitors_future.result()
        }
