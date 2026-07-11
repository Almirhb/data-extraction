import pytest

from extractors.base_extractor import BaseExtractor


def test_base_extractor_requires_source_name():
    # a subclass without source_name set should raise an error on init
    class BadExtractor(BaseExtractor):
        def extract(self):
            return []

    with pytest.raises(ValueError):
        BadExtractor()


def test_base_extractor_run_saves_records(mocker):
    # fake out the storage calls so this test doesn't touch a real database
    mock_insert = mocker.patch("extractors.base_extractor.insert_raw_record")
    mocker.patch("extractors.base_extractor.get_connection")
    mocker.patch("extractors.base_extractor.create_tables")

    class FakeExtractor(BaseExtractor):
        source_name = "fake_source"

        def extract(self):
            return [{"name": "record_1"}, {"name": "record_2"}]

    extractor = FakeExtractor()
    count = extractor.run()

    assert count == 2
    assert mock_insert.call_count == 2