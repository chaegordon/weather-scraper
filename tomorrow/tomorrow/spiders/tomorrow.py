import scrapy
import json
from environs import Env
from tomorrow.items import TomorrowItem
import logging
import datetime
import time

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
logger = logging.getLogger(__name__)


class TomorrowSpider(scrapy.Spider):
    name = "tomorrow"
    custom_settings = {
        "LOG_FILE": f"logs/{name}.log",
    }
    global logger

    # Define the starting URL or URLs -> one is forecast, the other realtime
    start_urls = [
        f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={TOMORROW_API_KEY}"
        for location in LOCATIONS
    ] + [
        f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={TOMORROW_API_KEY}"
        for location in LOCATIONS
    ]

    def parse(self, response):
        """
        Could equally do it via start_requests method yielding Scrapy Requests

        NB: only mandatory fields are time, longitude, and latitude
        """
        # THIS IS A HACK TO AVOID 429 TOO MANY REQUESTS, SCRAPY CONCURRENCY CAN BE ANNOYING TO TRY AND STOP
        time.sleep(0.4)
        # Convert the response to JSON
        data = json.loads(response.text)

        print(data["location"])
        scraped_at_time = datetime.datetime.now().isoformat()

        # if its a forecast response
        if "timelines" in data:
            # Extract the required fields from the JSON response
            for item in data["timelines"]["minutely"]:
                yield TomorrowItem(
                    frequency="minutely",
                    timestamp=item["time"],
                    scraped_at=scraped_at_time,
                    cloudBase=(
                        item["values"]["cloudBase"]
                        if "cloudBase" in item["values"]
                        else None
                    ),
                    cloudCeiling=(
                        item["values"]["cloudCeiling"]
                        if "cloudCeiling" in item["values"]
                        else None
                    ),
                    cloudCover=(
                        item["values"]["cloudCover"]
                        if "cloudCover" in item["values"]
                        else None
                    ),
                    dewPoint=(
                        item["values"]["dewPoint"]
                        if "dewPoint" in item["values"]
                        else None
                    ),
                    freezingRainIntensity=(
                        item["values"]["freezingRainIntensity"]
                        if "freezingRainIntensity" in item["values"]
                        else None
                    ),
                    humidity=(
                        item["values"]["humidity"]
                        if "humidity" in item["values"]
                        else None
                    ),
                    precipitationProbability=(
                        item["values"]["precipitationProbability"]
                        if "precipitationProbability" in item["values"]
                        else None
                    ),
                    pressureSurfaceLevel=(
                        item["values"]["pressureSurfaceLevel"]
                        if "pressureSurfaceLevel" in item["values"]
                        else None
                    ),
                    rainIntensity=(
                        item["values"]["rainIntensity"]
                        if "rainIntensity" in item["values"]
                        else None
                    ),
                    sleetIntensity=(
                        item["values"]["sleetIntensity"]
                        if "sleetIntensity" in item["values"]
                        else None
                    ),
                    snowIntensity=(
                        item["values"]["snowIntensity"]
                        if "snowIntensity" in item["values"]
                        else None
                    ),
                    temperature=(
                        item["values"]["temperature"]
                        if "temperature" in item["values"]
                        else None
                    ),
                    temperatureApparent=(
                        item["values"]["temperatureApparent"]
                        if "temperatureApparent" in item["values"]
                        else None
                    ),
                    uvHealthConcern=(
                        item["values"]["uvHealthConcern"]
                        if "uvHealthConcern" in item["values"]
                        else None
                    ),
                    uvIndex=(
                        item["values"]["uvIndex"]
                        if "uvIndex" in item["values"]
                        else None
                    ),
                    visibility=(
                        item["values"]["visibility"]
                        if "visibility" in item["values"]
                        else None
                    ),
                    weatherCode=(
                        item["values"]["weatherCode"]
                        if "weatherCode" in item["values"]
                        else None
                    ),
                    windDirection=(
                        item["values"]["windDirection"]
                        if "windDirection" in item["values"]
                        else None
                    ),
                    windGust=(
                        item["values"]["windGust"]
                        if "windGust" in item["values"]
                        else None
                    ),
                    windSpeed=(
                        item["values"]["windSpeed"]
                        if "windSpeed" in item["values"]
                        else None
                    ),
                    latitude=data["location"]["lat"],
                    longitude=data["location"]["lon"],
                )
            for item in data["timelines"]["hourly"]:
                yield TomorrowItem(
                    frequency="hourly",
                    timestamp=item["time"],
                    scraped_at=scraped_at_time,
                    cloudBase=(
                        item["values"]["cloudBase"]
                        if "cloudBase" in item["values"]
                        else None
                    ),
                    cloudCeiling=(
                        item["values"]["cloudCeiling"]
                        if "cloudCeiling" in item["values"]
                        else None
                    ),
                    cloudCover=(
                        item["values"]["cloudCover"]
                        if "cloudCover" in item["values"]
                        else None
                    ),
                    dewPoint=(
                        item["values"]["dewPoint"]
                        if "dewPoint" in item["values"]
                        else None
                    ),
                    freezingRainIntensity=(
                        item["values"]["freezingRainIntensity"]
                        if "freezingRainIntensity" in item["values"]
                        else None
                    ),
                    humidity=(
                        item["values"]["humidity"]
                        if "humidity" in item["values"]
                        else None
                    ),
                    precipitationProbability=(
                        item["values"]["precipitationProbability"]
                        if "precipitationProbability" in item["values"]
                        else None
                    ),
                    pressureSurfaceLevel=(
                        item["values"]["pressureSurfaceLevel"]
                        if "pressureSurfaceLevel" in item["values"]
                        else None
                    ),
                    rainIntensity=(
                        item["values"]["rainIntensity"]
                        if "rainIntensity" in item["values"]
                        else None
                    ),
                    sleetIntensity=(
                        item["values"]["sleetIntensity"]
                        if "sleetIntensity" in item["values"]
                        else None
                    ),
                    snowIntensity=(
                        item["values"]["snowIntensity"]
                        if "snowIntensity" in item["values"]
                        else None
                    ),
                    temperature=(
                        item["values"]["temperature"]
                        if "temperature" in item["values"]
                        else None
                    ),
                    temperatureApparent=(
                        item["values"]["temperatureApparent"]
                        if "temperatureApparent" in item["values"]
                        else None
                    ),
                    uvHealthConcern=(
                        item["values"]["uvHealthConcern"]
                        if "uvHealthConcern" in item["values"]
                        else None
                    ),
                    uvIndex=(
                        item["values"]["uvIndex"]
                        if "uvIndex" in item["values"]
                        else None
                    ),
                    visibility=(
                        item["values"]["visibility"]
                        if "visibility" in item["values"]
                        else None
                    ),
                    weatherCode=(
                        item["values"]["weatherCode"]
                        if "weatherCode" in item["values"]
                        else None
                    ),
                    windDirection=(
                        item["values"]["windDirection"]
                        if "windDirection" in item["values"]
                        else None
                    ),
                    windGust=(
                        item["values"]["windGust"]
                        if "windGust" in item["values"]
                        else None
                    ),
                    windSpeed=(
                        item["values"]["windSpeed"]
                        if "windSpeed" in item["values"]
                        else None
                    ),
                    latitude=data["location"]["lat"],
                    longitude=data["location"]["lon"],
                )
            for item in data["timelines"]["daily"]:
                yield TomorrowItem(
                    frequency="daily",
                    timestamp=item["time"],
                    scraped_at=scraped_at_time,
                    cloudBase=(
                        item["values"]["cloudBaseAvg"]
                        if "cloudBaseAvg" in item["values"]
                        else None
                    ),
                    cloudCeiling=(
                        item["values"]["cloudCeilingAvg"]
                        if "cloudCeilingAvg" in item["values"]
                        else None
                    ),
                    cloudCover=(
                        item["values"]["cloudCoverAvg"]
                        if "cloudCoverAvg" in item["values"]
                        else None
                    ),
                    dewPoint=(
                        item["values"]["dewPoint"]
                        if "dewPoint" in item["values"]
                        else None
                    ),
                    freezingRainIntensity=(
                        item["values"]["freezingRainIntensityAvg"]
                        if "freezingRainIntensityAvg" in item["values"]
                        else None
                    ),
                    humidity=(
                        item["values"]["humidityAvg"]
                        if "humidityAvg" in item["values"]
                        else None
                    ),
                    precipitationProbability=(
                        item["values"]["precipitationProbabilityAvg"]
                        if "precipitationProbabilityAvg" in item["values"]
                        else None
                    ),
                    pressureSurfaceLevel=(
                        item["values"]["pressureSurfaceLevelAvg"]
                        if "pressureSurfaceLevelAvg" in item["values"]
                        else None
                    ),
                    rainIntensity=(
                        item["values"]["rainIntensityAvg"]
                        if "rainIntensityAvg" in item["values"]
                        else None
                    ),
                    sleetIntensity=(
                        item["values"]["sleetIntensityAvg"]
                        if "sleetIntensityAvg" in item["values"]
                        else None
                    ),
                    snowIntensity=(
                        item["values"]["snowIntensityAvg"]
                        if "snowIntensityAvg" in item["values"]
                        else None
                    ),
                    temperature=(
                        item["values"]["temperatureAvg"]
                        if "temperatureAvg" in item["values"]
                        else None
                    ),
                    temperatureApparent=(
                        item["values"]["temperatureApparentAvg"]
                        if "temperatureApparentAvg" in item["values"]
                        else None
                    ),
                    uvHealthConcern=(
                        item["values"]["uvHealthConcernAvg"]
                        if "uvHealthConcernAvg" in item["values"]
                        else None
                    ),
                    uvIndex=(
                        item["values"]["uvIndexAvg"]
                        if "uvIndexAvg" in item["values"]
                        else None
                    ),
                    visibility=(
                        item["values"]["visibilityAvg"]
                        if "visibilityAvg" in item["values"]
                        else None
                    ),
                    weatherCode=(
                        item["values"]["weatherCodeAvg"]
                        if "weatherCodeAvg" in item["values"]
                        else None
                    ),
                    windDirection=(
                        item["values"]["windDirectionAvg"]
                        if "windDirectionAvg" in item["values"]
                        else None
                    ),
                    windGust=(
                        item["values"]["windGustAvg"]
                        if "windGustAvg" in item["values"]
                        else None
                    ),
                    windSpeed=(
                        item["values"]["windSpeedAvg"]
                        if "windSpeedAvg" in item["values"]
                        else None
                    ),
                    latitude=data["location"]["lat"],
                    longitude=data["location"]["lon"],
                )
        # if its a realtime response
        else:
            item = data["data"]
            yield TomorrowItem(
                frequency="realtime",
                timestamp=item["time"],
                scraped_at=scraped_at_time,
                cloudBase=(
                    item["values"]["cloudBase"]
                    if "cloudBase" in item["values"]
                    else None
                ),
                cloudCeiling=(
                    item["values"]["cloudCeiling"]
                    if "cloudCeiling" in item["values"]
                    else None
                ),
                cloudCover=(
                    item["values"]["cloudCover"]
                    if "cloudCover" in item["values"]
                    else None
                ),
                dewPoint=(
                    item["values"]["dewPoint"] if "dewPoint" in item["values"] else None
                ),
                freezingRainIntensity=(
                    item["values"]["freezingRainIntensity"]
                    if "freezingRainIntensity" in item["values"]
                    else None
                ),
                humidity=(
                    item["values"]["humidity"] if "humidity" in item["values"] else None
                ),
                precipitationProbability=(
                    item["values"]["precipitationProbability"]
                    if "precipitationProbability" in item["values"]
                    else None
                ),
                pressureSurfaceLevel=(
                    item["values"]["pressureSurfaceLevel"]
                    if "pressureSurfaceLevel" in item["values"]
                    else None
                ),
                rainIntensity=(
                    item["values"]["rainIntensity"]
                    if "rainIntensity" in item["values"]
                    else None
                ),
                sleetIntensity=(
                    item["values"]["sleetIntensity"]
                    if "sleetIntensity" in item["values"]
                    else None
                ),
                snowIntensity=(
                    item["values"]["snowIntensity"]
                    if "snowIntensity" in item["values"]
                    else None
                ),
                temperature=(
                    item["values"]["temperature"]
                    if "temperature" in item["values"]
                    else None
                ),
                temperatureApparent=(
                    item["values"]["temperatureApparent"]
                    if "temperatureApparent" in item["values"]
                    else None
                ),
                uvHealthConcern=(
                    item["values"]["uvHealthConcern"]
                    if "uvHealthConcern" in item["values"]
                    else None
                ),
                uvIndex=(
                    item["values"]["uvIndex"] if "uvIndex" in item["values"] else None
                ),
                visibility=(
                    item["values"]["visibility"]
                    if "visibility" in item["values"]
                    else None
                ),
                weatherCode=(
                    item["values"]["weatherCode"]
                    if "weatherCode" in item["values"]
                    else None
                ),
                windDirection=(
                    item["values"]["windDirection"]
                    if "windDirection" in item["values"]
                    else None
                ),
                windGust=(
                    item["values"]["windGust"] if "windGust" in item["values"] else None
                ),
                windSpeed=(
                    item["values"]["windSpeed"]
                    if "windSpeed" in item["values"]
                    else None
                ),
                latitude=data["location"]["lat"],
                longitude=data["location"]["lon"],
            )
