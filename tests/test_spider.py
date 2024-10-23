import pytest

from tomorrow.tomorrow.pipelines import TomorrowPipeline


def test_mock():
    # fake test
    assert 1 + 1 == 2


def test_tomorrow_pipeline():
    pipeline = TomorrowPipeline()
    assert pipeline is not None
    assert hasattr(pipeline, "open_spider")
    assert hasattr(pipeline, "close_spider")
    assert hasattr(pipeline, "process_item")
    assert hasattr(pipeline, "insert_batch")


def test_tomorrow_pipeline_open_spider():
    pipeline = TomorrowPipeline()
    pipeline.open_spider(None)
    assert pipeline.connection is not None
    assert pipeline.cursor is not None
    assert pipeline.batch == []
    assert pipeline.batch_size == 100
    assert pipeline.count == 0


# could test assertions on the data within the connection object etc.
