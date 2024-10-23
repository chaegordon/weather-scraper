# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


"""
https://docs.tomorrow.io/reference/weather-forecast

# timelines
    # minutely - 60 values
        # List of 60 {time, values}
            # time
            # values
                # cloudBase 
                # cloudCeiling
                # cloudCover
                # dewPoint
                # freezingRainIntensity
                # humidity
                # precipitationProbability
                # pressureSurfaceLevel
                # rainIntensity
                # sleetIntensity
                # snowIntensity
                # temperature
                # temperatureApparent
                # uvHealthConcern
                # uvIndex
                # visibility
                # weatherCode
                # windDirection
                # windGust
                # windSpeed
    # hourly - 120 values
    # daily - 7 values
# location
"""


class TomorrowItem(scrapy.Item):
    freqency = scrapy.Field()
    timestamp = scrapy.Field()
    cloudBase = scrapy.Field()
    cloudCeiling = scrapy.Field()
    cloudCover = scrapy.Field()
    dewPoint = scrapy.Field()
    freezingRainIntensity = scrapy.Field()
    humidity = scrapy.Field()
    precipitationProbability = scrapy.Field()
    pressureSurfaceLevel = scrapy.Field()
    rainIntensity = scrapy.Field()
    sleetIntensity = scrapy.Field()
    snowIntensity = scrapy.Field()
    temperature = scrapy.Field()
    temperatureApparent = scrapy.Field()
    uvHealthConcern = scrapy.Field()
    uvIndex = scrapy.Field()
    visibility = scrapy.Field()
    weatherCode = scrapy.Field()
    windDirection = scrapy.Field()
    windGust = scrapy.Field()
    windSpeed = scrapy.Field()
