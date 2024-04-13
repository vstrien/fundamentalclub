from chatutils.chat_utils import ChatGPT
import json
from fundamentalclub.cosmos_backend import CosmosBackendFundamentalGuide

def strip_markdown(text):
    return text.replace("```json", "").replace("```", "")

class Guide(ChatGPT):
    def __init__(self, api_key, ticker_name):
        super().__init__(api_key, """The GPT is a fundamental analyst, specialized in scrutinizing companies with a focus on financial stability and risk aversion. 
It possesses a deep understanding of financial history, allowing it to provide insightful analysis and cautionary advice. 
This GPT actively points out when users ask for inappropriate indicators for an industry or overlook crucial financial information. 
Its primary role is to assist in making informed, cautious investment decisions by analyzing financial statements, market trends, and historical data. 
The GPT should avoid speculative or high-risk advice and emphasize conservative, well-researched strategies. 
It should ask for clarification when needed to ensure accurate and relevant advice. 
The GPT's responses should be tailored to reflect a cautious, detail-oriented personality, focusing on thorough analysis and risk management.""")
        self.name = "Guide"
        self.ticker_name = ticker_name
        self.industry = None
        self.key_financial_indicators = None
        self.risks = None
        self.competitors = None

    def get_industry(self):
        if self.industry is None:
            self.industry = self.call_chatgpt_api(f"I'm researching company {self.ticker_name}. What industry is this company in? Anser with a single industry name, no further explanation.")
        return self.industry

    def get_key_financial_indicators(self):
        if self.key_financial_indicators is None:
            self.key_financial_indicators = json.loads(strip_markdown(self.call_chatgpt_api(f"""I'm researching company {self.ticker_name} in industry {self.get_industry()}. What are the key financial indicators I should be looking at? Answer with a list of key financial indicators in JSON, structured like this:
```json
{
    [
        {
            'indicator': 'Revenue',
            'description': 'The total amount of money a company makes from selling goods or services.',
            'sources': ['Income Statement'],
            'importance': 'High',
            'formula': 'Total Sales - Returns',
            'formula_components': [
            {'component': 'Total Sales', 
                'source': 'Income Statement',
                'aliases': ['Sales', 'Net Sales']
            },
            {
                'component': 'Returns',
                'source': 'Income Statement',
                'aliases': ['Refunds']
            }
        ]
        }
        # , More indicators...
    ]
}```""")))
        return self.key_financial_indicators

    def get_risks(self):
        if self.risks is None:
            self.risks = json.loads(strip_markdown(self.call_chatgpt_api(f"""I'm researching company {self.ticker_name} in industry {self.get_industry()}. What are the risks associated with this company? Answer with a list of risks in JSON, structured like this:
```json
{
    [
        {
            'risk': 'Market Risk',
            'description': 'The risk of an investment''s value changing due to changes in the market.',
            'likelihood': 'High',
            'impact': 'High',
            'mitigation': 'Diversification',
            'sources': ['SEC Filings', 'Financial Statements'],
            'phrases': ['Market crash', 'Economic downturn', 'Recession']
        }
        # , More risks...
    ]
}```
""")))
        return self.risks

    def get_competitors(self):
        if self.competitors is None:
            self.competitors = json.loads(strip_markdown(self.call_chatgpt_api(f"""I'm researching company {self.ticker_name} in industry {self.get_industry()}. Who are the main competitors of this company? Answer with a list of competitors in JSON, structured like this:
```json
{
    [
        {
            'competitor': 'Company A',
            'description': 'Company A is a direct competitor of the company, offering similar products and services.',
            'strengths': ['Strong brand recognition', 'Large market share'],
            'weaknesses': ['High debt', 'Low profit margin'],
            'sources': ['SEC Filings', 'Company Website'],
            'stock ticker': 'A'
        }
        # , More competitors...
    ]
}```
""")))
        return self.competitors

class DbBackedGuide(Guide):
    def __init__(self, api_key, ticker_name, database: CosmosBackendFundamentalGuide):
        super().__init__(api_key, ticker_name)
        self.database = database
    
    def get_industry(self):
        if self.industry is None:
            self.industry = self.database.get_industry(self.ticker_name)
        if self.industry is None or len(self.industry) == 0: ## Empty dictionary
            self.industry = super().get_industry()
            self.database.set_industry(self.ticker_name, self.industry)
        return self.industry
    
    def get_key_financial_indicators(self):
        if self.key_financial_indicators is None:
            self.key_financial_indicators = self.database.get_kfis(self.ticker_name)
        if self.key_financial_indicators is None or len(self.key_financial_indicators) == 0:
            self.key_financial_indicators = super().get_key_financial_indicators()
            self.database.set_kfis(self.ticker_name, self.key_financial_indicators)
        return self.key_financial_indicators
    
    def get_risks(self):
        if self.risks is None:
            self.risks = self.database.get_risks(self.ticker_name)
        if self.risks is None or len(self.risks) == 0:
            self.risks = super().get_risks()
            self.database.set_risks(self.ticker_name, self.risks)
        return self.risks
    
    def get_competitors(self):
        if self.competitors is None:
            self.competitors = self.database.get_competitors(self.ticker_name)
        if self.competitors is None or len(self.competitors) == 0:
            self.competitors = super().get_competitors()
            self.database.set_competitors(self.ticker_name, self.competitors)
        return self.competitors
    
    def get_all(self):
        return {
            "ticker": self.ticker_name, ## "AAPL"
            "industry": self.get_industry(),
            "key_financial_indicators": self.get_key_financial_indicators(),
            "risks": self.get_risks(),
            "competitors": self.get_competitors()
        }
