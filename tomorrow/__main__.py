import logging
import requests
from environs import Env
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# load environment variables
env = Env()
env.read_env()
tomorrow_api_key = env.str("TOMORROW_API_KEY")

# configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

setting = get_project_settings()
crawler_process = CrawlerProcess(setting)
crawler_process.crawl("tomorrow")

# start the crawler
logger.info("-" * 50)
logger.info("Spiders started running.")
logger.info("-" * 50)

crawler_process.start()
crawler_process.join()

logger.info("-" * 50)
logger.info("Spiders finished running.")
logger.info("-" * 50)
