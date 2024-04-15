from fundamentalclub.fundamentalguide.guide import DbBackedGuide
from fundamentalclub.cosmosbackend.cosmosbackend import CosmosBackendFundamentalGuide
import os
import dotenv
import asyncio
import logging
import concurrent.futures

logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)

dotenv.load_dotenv()

list_to_analyze = ["BLDR", "ENR", "GPS", "MTW", "SCS", "JPM", "AEO", "SKX", "KBH"]
guides = []
for ticker in list_to_analyze:
    guides.append(DbBackedGuide(
        os.getenv("OPENAI_API_KEY"), 
        ticker, 
        CosmosBackendFundamentalGuide(
            os.getenv("COSMOS_ENDPOINT"), 
            os.getenv("COSMOS_KEY"),
            "fundamentalclub",
        )
    ))

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(lambda guide: asyncio.run(guide.get_all()), guides)

