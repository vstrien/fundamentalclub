from fundamentalclub.fundamentalguide.guide import DbBackedGuide
from fundamentalclub.cosmosbackend.cosmosbackend import CosmosBackendFundamentalGuide
import os
import dotenv

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

guide.get_all()