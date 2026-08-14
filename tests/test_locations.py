from src.locations import is_us_location


def test_accepts_united_states():
    assert is_us_location("United States")


def test_accepts_us_remote():
    assert is_us_location("Remote - US")


def test_accepts_state_abbreviation():
    assert is_us_location("Boston, MA")


def test_accepts_full_state_name():
    assert is_us_location("New York, New York")


def test_accepts_workday_location_format():
    assert is_us_location("USA.CA.Santa Clara")


def test_accepts_multiple_locations_with_us_option():
    assert is_us_location("Austin, TX | Toronto, Canada")


def test_rejects_non_us_location():
    assert not is_us_location("London, United Kingdom")


def test_rejects_unknown_remote_location():
    assert not is_us_location("Remote")


def test_rejects_empty_location():
    assert not is_us_location("")
