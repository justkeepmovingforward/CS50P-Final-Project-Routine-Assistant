import pytest
from project import convert_to_24hour, validation

def test_AM():
    assert convert_to_24hour(12, 00, "AM")=="00:00"
    assert convert_to_24hour(12, 1, "AM")=="00:01"
    assert convert_to_24hour(12, 59, "AM")== "00:59"
    assert convert_to_24hour(11, 00, "AM")== "11:00"
    assert convert_to_24hour(1, 00, "AM")== "01:00"

def test_PM():
    assert convert_to_24hour(12, 00, "PM")== "12:00"
    assert convert_to_24hour(12, 1, "PM")== "12:01"
    assert convert_to_24hour(12, 59, "PM")== "12:59"
    assert convert_to_24hour(1, 00, "PM")== "13:00"
    assert convert_to_24hour(9, 9, "PM")== "21:09"
    assert convert_to_24hour(11, 00, "PM")== "23:00"

def test_invalid_time():
    assert convert_to_24hour(13, 00, "AM")== None
    assert convert_to_24hour(00, 00, "PM")== None
    assert convert_to_24hour(12, 60, "AM")== None
    assert convert_to_24hour(9, 75, "PM")== None
    assert convert_to_24hour(22, 00, "PM")== None

def test_validInput(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "12:00pm-lunch")
    result = validation()
    assert result == (12, 00, "PM", "lunch")

    monkeypatch.setattr('builtins.input', lambda _: "12:00pm - lunch")
    result = validation()
    assert result == (12, 00, "PM", "lunch")

def test_invalidInput(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "12:00 water")
    result = validation()
    assert result is None

    monkeypatch.setattr('builtins.input', lambda _: "12:00ampm water")
    result = validation()
    assert result is None
