from analysis.roi_calculator import normalize


def test_normalize_scales_to_0_100_range():
    # value right in the middle of the range should land around 50
    result = normalize(50, min_value=0, max_value=100)
    assert result == 50


def test_normalize_min_value_gives_zero():
    result = normalize(10, min_value=10, max_value=100)
    assert result == 0


def test_normalize_max_value_gives_hundred():
    result = normalize(100, min_value=10, max_value=100)
    assert result == 100


def test_normalize_handles_equal_min_and_max():
    # avoid division by zero when every value in the dataset is the same
    result = normalize(50, min_value=50, max_value=50)
    assert result == 0