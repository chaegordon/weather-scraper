# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import psycopg2
import psycopg2.extras


class TomorrowPipeline:
    def __init__(self):
        # Initialize logger
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        # Open the database connection
        self.connection = psycopg2.connect(
            host="postgres",  # PGHOST
            port="5432",  # PGPORT
            database="tomorrow",  # PGDATABASE
            user="postgres",  # PGUSER
            password="postgres",  # PGPASSWORD
        )
        self.cursor = self.connection.cursor()
        self.batch = []  # List to store the batch of items
        self.batch_size = 100  # Size of the batch before inserting
        self.count = 0

    def close_spider(self, spider):
        # Insert any remaining items in the batch
        if self.batch:
            self.insert_batch(spider)
        # Refresh the materialized views after all items are inserted
        try:
            self.cursor.execute(
                "REFRESH MATERIALIZED VIEW CONCURRENTLY minutely_weather;"
            )
            self.cursor.execute(
                "REFRESH MATERIALIZED VIEW CONCURRENTLY hourly_weather;"
            )
            self.cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY daily_weather;")
            self.cursor.execute(
                "REFRESH MATERIALIZED VIEW CONCURRENTLY realtime_weather;"
            )
            spider.logger.info("Materialized views refreshed successfully.")

        except Exception as e:
            spider.logger.error(f"Error refreshing materialized views: {e}")
            self.connection.rollback()  # Roll back in case of error
        finally:
            # Commit changes and close the connection
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        # Get spider stats information
        spider_status_dict = spider.crawler.stats.get_stats()
        # if key "log-count/ERROR" doesn't exist create it and set it to 0, likewise for WARNING and INFO
        if "log_count/ERROR" not in spider_status_dict.keys():
            spider_status_dict["log_count/ERROR"] = 0
        if "log_count/WARNING" not in spider_status_dict.keys():
            spider_status_dict["log_count/WARNING"] = 0
        if "log_count/INFO" not in spider_status_dict.keys():
            spider_status_dict["log_count/INFO"] = 0
        spider_status_dict["spider"] = spider.name
        spider_status_dict["count"] = self.count

    def insert_batch(self, spider):
        """Inserts the accumulated batch of items into the database."""
        try:
            psycopg2.extras.execute_batch(
                self.cursor,
                """INSERT INTO weather_data (frequency, timestamp, scraped_at, cloud_base, cloud_ceiling, cloud_cover,
        dew_point, freezing_rain_intensity, humidity, precipitation_probability, pressure_surface_level,
        rain_intensity, sleet_intensity, snow_intensity, temperature, temperature_apparent, uv_health_concern,
        uv_index, visibility, weather_code, wind_direction, wind_gust, wind_speed, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                [
                    (
                        item["frequency"],
                        item["timestamp"],
                        item["scraped_at"],
                        item["cloudBase"],
                        item["cloudCeiling"],
                        item["cloudCover"],
                        item["dewPoint"],
                        item["freezingRainIntensity"],
                        item["humidity"],
                        item["precipitationProbability"],
                        item["pressureSurfaceLevel"],
                        item["rainIntensity"],
                        item["sleetIntensity"],
                        item["snowIntensity"],
                        item["temperature"],
                        item["temperatureApparent"],
                        item["uvHealthConcern"],
                        item["uvIndex"],
                        item["visibility"],
                        item["weatherCode"],
                        item["windDirection"],
                        item["windGust"],
                        item["windSpeed"],
                        item["latitude"],
                        item["longitude"],
                    )
                    for item in self.batch
                ],
            )

            self.connection.commit()
            self.batch = []  # Clear the batch after inserting
        except Exception as e:
            spider.logger.error(f"Error inserting batch: {e}")
            self.connection.rollback()

    def process_item(self, item, spider):
        # Add item to the batch
        self.batch.append(item)

        # If batch is full, insert the batch
        if len(self.batch) >= self.batch_size:
            self.count += len(self.batch)
            self.insert_batch(spider)

        return item
