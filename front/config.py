from httpx import Client
from dotenv import load_dotenv

from utils import get_env_variable

load_dotenv()

API_URL = get_env_variable(env_variable_name="API_URL")
client = Client(base_url=API_URL)

PAGE_SIZE = 25
