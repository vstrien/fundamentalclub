from azure.cosmos import CosmosClient, PartitionKey

class CosmosBackend():    
    def __init__(self, containers_needed: dict, endpoint: str, key: str, database_name: str):
        self.client = CosmosClient(endpoint, key)
        self.database = self.client.create_database_if_not_exists(database_name)
        
        for container_name, key_path in containers_needed.items():
            self.database.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path=key_path))

class CosmosBackendFundamentalGuide(CosmosBackend):
    def __init__(self, endpoint: str, key: str, database_name: str):
        containers_needed = {
            "users": "/id"
        }

        containers_needed = {
            "Risks": "/ticker"
            , "Competitors": "/ticker"
            , "KFIs": "/ticker"
            , "Industry": "/ticker"
            , "Tickers": "/ticker"
        }
        super().__init__(containers_needed, endpoint, key, database_name)
    
    def get_tickers(self):
        container = self.database.get_container_client("Tickers")
        return container.query_items(query='SELECT * FROM c')

    def get_risks(self, ticker):
        container = self.database.get_container_client("Risks")
        return container.query_items(query='SELECT * FROM c WHERE c.ticker = "' + ticker + '"')

    def set_risks(self, ticker, risks):
        container = self.database.get_container_client("Risks")
        container.upsert_item({
            "ticker": ticker,
            "risks": risks
        })
    
    def get_competitors(self, ticker):
        container = self.database.get_container_client("Competitors")
        return container.query_items(query='SELECT * FROM c WHERE c.ticker = "' + ticker + '"')

    def set_competitors(self, ticker, competitors):
        container = self.database.get_container_client("Competitors")
        container.upsert_item({
            "ticker": ticker,
            "competitors": competitors
        })

    def get_kfis(self, ticker):
        container = self.database.get_container_client("KFIs")
        return container.query_items(query='SELECT * FROM c WHERE c.ticker = "' + ticker + '"')
    
    def set_kfis(self, ticker, kfis):
        container = self.database.get_container_client("KFIs")
        container.upsert_item({
            "ticker": ticker,
            "kfis": kfis
        })
    
    def get_industry(self, ticker):
        container = self.database.get_container_client("Industry")
        return container.query_items(query='SELECT * FROM c WHERE c.ticker = "' + ticker + '"')
    
    def set_industry(self, ticker, industry):
        container = self.database.get_container_client("Industry")
        container.upsert_item({
            "ticker": ticker,
            "industry": industry
        })

    