import scrapy
import json
from environs import Env
from items import TomorrowItem

"""
LOCATIONS:

|   lat   |   lon    |
|:-------:|:--------:|
| 25.8600 | -97.4200 |
| 25.9000 | -97.5200 |
| 25.9000 | -97.4800 |
| 25.9000 | -97.4400 |
| 25.9000 | -97.4000 |
| 25.9200 | -97.3800 |
| 25.9400 | -97.5400 |
| 25.9400 | -97.5200 |
| 25.9400 | -97.4800 |
| 25.9400 | -97.4400 |

"""

# list in format "lat,lon" e.g. "42.3478,-71.0466"
LOCATIONS = [
    "25.8600,-97.4200",
    "25.9000,-97.5200",
    "25.9000,-97.4800",
    "25.9000,-97.4400",
    "25.9000,-97.4000",
    "25.9200,-97.3800",
    "25.9400,-97.5400",
    "25.9400,-97.5200",
    "25.9400,-97.4800",
    "25.9400,-97.4400",
]

# load environment variables
env = Env()
env.read_env()
# global variable TOMORROW_API_KEY
TOMORROW_API_KEY = env.str("TOMORROW_API_KEY")


class TomorrowSpider(scrapy.Spider):
    name = "tomorrow"

    # Define the starting URL or URLs
    start_urls = [
        f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={TOMORROW_API_KEY}"
        for location in LOCATIONS
    ]

    def parse(self, response):
        """
        Could equally do it via start_requests method yielding Scrapy Requests
        """
        # Convert the response to JSON
        data = json.loads(response.body_as_unicode())

        # Extract the required fields from the JSON response
        for item in data["data"]["timelines"]:
            yield TomorrowItem(
                freqency=item["timestep"],
                timestamp=item["startTime"],
                cloudBase=item["values"]["cloudBase"],
                cloudCeiling=item["values"]["cloudCeiling"],
                cloudCover=item["values"]["cloudCover"],
                dewPoint=item["values"]["dewPoint"],
                freezingRainIntensity=item["values"]["freezingRainIntensity"],
                humidity=item["values"]["humidity"],
                precipitationProbability=item["values"]["precipitationProbability"],
                pressureSurfaceLevel=item["values"]["pressureSurfaceLevel"],
                rainIntensity=item["values"]["rainIntensity"],
                sleetIntensity=item["values"]["sleetIntensity"],
                snowIntensity=item["values"]["snowIntensity"],
                temperature=item["values"]["temperature"],
                temperatureApparent=item["values"]["temperatureApparent"],
                uvHealthConcern=item["values"]["uvHealthConcern"],
                uvIndex=item["values"]["uvIndex"],
                visibility=item["values"]["visibility"],
                weatherCode=item["values"]["weatherCode"],
                windDirection=item["values"]["windDirection"],
                windGust=item["values"]["windGust"],
                windSpeed=item["values"]["windSpeed"],
            )
