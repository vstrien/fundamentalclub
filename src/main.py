from fundamentalclub.fundamentalguide.guide import DbBackedGuide
from fundamentalclub.cosmosbackend.cosmosbackend import CosmosBackendFundamentalGuide
import os
import dotenv
import asyncio

dotenv.load_dotenv()
guide = DbBackedGuide(
    os.getenv("OPENAI_API_KEY"), 
    "RELL", 
    CosmosBackendFundamentalGuide(
        os.getenv("COSMOS_ENDPOINT"), 
        os.getenv("COSMOS_KEY"),
        "fundamentalclub",
    )
)

asyncio.run(guide.get_all())