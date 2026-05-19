"""
test validators
"""

from pytest import raises


def test_validate_link_valid():
    from core.validators import validate_link

    assert validate_link("https://www.example.com/a/b/c?query=1&3")
    assert validate_link("www.example.com/a/b/c?query=1")  # failed
    assert validate_link("example.com/a/b/c?query=2")
    assert validate_link("example.example.com/a/b/c?query=1")
    assert validate_link("example.example.com/")
    assert validate_link("example.example.com/u/name?id=1")
    assert validate_link("example.com")
    assert validate_link("https://example.com/")
    assert validate_link("https://example.example.com")
    assert validate_link("https://example.com/t/?query=21")
    assert validate_link("https://example.example.com/q/?query=1")
    assert validate_link("")


def test_validate_link_invalid():
    from core.validators import validate_link

    with raises(ValueError):
        validate_link("http://somelinks.com")
        validate_link("http:/example.com")
        validate_link("http:://example.com")
        validate_link("http:example.com")
        validate_link("/example.com")
        validate_link("https:example.com")
        validate_link("https/example.com")
        validate_link("example")


def test_validate_phone_number_valid():
    from core.validators import phone_number_validator

    assert phone_number_validator("+91 12345 12345")
    assert phone_number_validator("+91 1234512345")
    assert phone_number_validator("+9112345 12345")
    assert phone_number_validator("+911234512345")
    assert phone_number_validator("91 12334 12345")
    assert phone_number_validator("")


def test_validate_phone_number_invalid():
    from core.validators import phone_number_validator

    with raises(ValueError):
        phone_number_validator("0 12345 12345")
        # TODO


def test_validate_username():
    from core.validators import validate_username

    assert validate_username("@1982random_username")
    assert validate_username("@" + "a" * 30)
    assert validate_username("@__username")
    assert validate_username("@_.user._")
    assert validate_username("")


def test_validate_username_invalid():
    from core.validators import validate_username

    with raises(ValueError):
        validate_username("@")
        validate_username("@ username")
        validate_username("@,userame")
        validate_username("@._username!")
        validate_username("@'bla'")
        validate_username("@something?")
