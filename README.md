# Usage

create a .env file in the root of the repository with the following contents:

```
TOMORROW_API_KEY=<your api key>
```

To transition to prod you would need to change the logger level in __main__.py to INFO and also refactor to make the postgres details environment variables.

while at the root of the repository, run the following command:

```bash
docker compose up --build
```

If you want to run a once off scrape, run the following command:

```bash
docker compose up --build tomorrow
```

To access the latest temperature data for locations navigate to the jupyter notebook at "http://localhost:8888/notebooks/analysis.ipynb". You can also reuse connection logic there to look at the postgres database.

To check everything is working as expected, navigate to logs files in ./logs directory.
 - cron_test.log
    This log file should contain the output of the cron job that runs every minute. If the time there is fresh, then the cron system is working as expected.
 - cron.log
    This log file should contain the output of the cron job that runs every hour. Should contain spider stats, and ideally show no errors.
 - test_results.log
    This log file should contain the output of the test that runs when the container is built. If the tests pass, then the tomorrow spider is instantiated correctly.

The spider logs are stored in the ./tomorrow/logs directory. If you want to see the output of the spider, navigate to the logs directory and open the log file.

# Architecture

The system is composed of 3 main components:
 - A postgres database
    I didnt see any reason to change the database so I stuck with the postgres setup provided in the docker compose file. I opted to have a single table for data for all the timelines and the realtime data but with materialized views to make it easier to query the data. Arguably, I think these coudld be separate tables, especially as the forecast data is different from the realtime data in "essence" and the fields dont quite match between the daily timeline data and the rest of them. However, for the purposes of this exercise, I think it is fine to have them in the same table and performance wise it doesn't seem an issue. The decision was mainly taken to make the scraper easier to implement as only one table is inserted into and only one item is defined in the scrapy spider. If we used the different views in vastly different ways or if it grew to be very large so that scanning time was impacting performance, then it would make sense to separate them into different tables or to partition the table instead. To see the insertion, refresh logic and the materialized views, navigate to the ./tomorrow/tomorrow/pipelines.py file.
 - A scrapy spider that fetches the weather data from the tomorrow api
    The spider is a simple one that fetches the data from the tomorrow api and inserts it into the postgres database. The spider is run every hour by a cron job. The spider is also run once when the container is built to check that it is working as expected. Its probably a bit overkill to use scrapy framework; however, the spider is very simple and the pipeline abstraction is useful for instantiating the database connection, inserting the data and then refreshing the materialized views and it allows for graceful shutdown with the the close_spider method. To see the scraping logic, navigate to the ./tomorrow/tomorrow/spiders/tomorrow.py file.
 - A cron job that runs the spider every hour
    I would probably have just setup a simple cron job on host, had the assignment not asked for it all to be runnable with the docker compose up command. There are two cron jobs, one runs every minute to make sure the cron system is working and the other runs the spider every hour. I had started working with airflow but hooking it up and configuring it was taking too long so I decided it was overkill. Although I dont think having cron on docker is very standard practice, I have separated cron into its own service (although its not quite one thing per service as technically it runs two cronjobs). To see the cron jobs, navigate to the ./cronjobs file.

# Other notes
I used poetry instead of requirements.txt+venv for the scrapy aspect because its what I'm familiar with; however, I didn't opt to change the requirements.txt to poetry for Jupyter so it naturally enforces different environments for the scraping and the analysis. I think this is fine as the scraping environment is quite different from the analysis environment in their needs. I began writing some very basic tests with pytest however, if we were to stick with scrapy for the scraping elements there is a native "contracts" abstraction for testing within it (which is how we would approach testing for that aspect because getting absolute imports to work is hard due to the tomorrow/tomorrow/ structure of the directory enforced by scrapy). Some more tests around the database could be made if we had expectations on % of null values in fields etc; however, this would be better managed with something like great expectations as it is less pass/fail binary in nature (in that it may not be caused by code alterations it may just be bad data from the provider). There are a few different docker related files, what they relate to can be inferred from the docker-compose.yml. When running in prod you would want to not have