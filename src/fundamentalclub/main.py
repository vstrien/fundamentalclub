from fundamentalguide.guide import Guide
import os
import dotenv

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
guide = Guide(OPENAI_API_KEY, "RELL")
