from azure.cosmos import CosmosClient, PartitionKey

class CosmosBackend():    
    def __init__(self, containers_needed: dict, endpoint: str, cosmos_api_key: str, database_name: str):
        self.client = CosmosClient(endpoint, cosmos_api_key)
        self.database = self.client.create_database_if_not_exists(database_name)
        
        for container_name, key_path in containers_needed.items():
            self.database.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path=key_path))

class CosmosBackendFundamentalGuide(CosmosBackend):
    def __init__(self, endpoint: str, cosmos_api_key: str, database_name: str):
        containers_needed = {
            "Risks": "/ticker"
            , "Competitors": "/ticker"
            , "KFIs": "/ticker"
            , "Industry": "/ticker"
            , "Tickers": "/ticker"
        }
        super().__init__(containers_needed, endpoint, cosmos_api_key, database_name)
    
    def _query_unpaged(self, container_name, query, elements=[]):
        if isinstance(elements, str):
            elements = [elements]
    
        container = self.database.get_container_client(container_name)
        items_paged = container.query_items(query=query)
        items = []
        for item in items_paged:
            for e in elements:
                items.append(item[e])
        return items[0] if len(items) == 1 else items

    def get_tickers(self):
        return self._query_unpaged("Tickers", 'SELECT * FROM c', ['ticker'])
        
    def get_risks(self, ticker):
        return self._query_unpaged("Risks", 'SELECT * FROM c WHERE c.ticker = "' + ticker + '"', ['risks'])
        
    def set_risks(self, ticker, risks):
        container = self.database.get_container_client("Risks")
        container.upsert_item({
            "id": ticker,
            "ticker": ticker,
            "risks": risks
        })
    
    def get_competitors(self, ticker):
        return self._query_unpaged("Competitors", 'SELECT * FROM c WHERE c.ticker = "' + ticker + '"', 'competitors')
        
    def set_competitors(self, ticker, competitors):
        container = self.database.get_container_client("Competitors")
        container.upsert_item({
            "id": ticker,
            "ticker": ticker,
            "competitors": competitors
        })

    def get_kfis(self, ticker):
        return self._query_unpaged("KFIs", 'SELECT * FROM c WHERE c.ticker = "' + ticker + '"', 'kfis')
        
    def set_kfis(self, ticker, kfis):
        container = self.database.get_container_client("KFIs")
        container.upsert_item({
            "id": ticker,
            "ticker": ticker,
            "kfis": kfis
        })
    
    def get_industry(self, ticker):
        return self._query_unpaged("Industry", 'SELECT * FROM c WHERE c.ticker = "' + ticker + '"', 'industry')
        
    def set_industry(self, ticker, industry):
        container = self.database.get_container_client("Industry")
        container.upsert_item({
            "id": ticker,
            "ticker": ticker,
            "industry": industry
        })

    