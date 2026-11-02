
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# Parking fee branches

def test_invalid_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


def test_negative_minutes():
    with pytest.raises(ValueError):
        parking_fee("car", -1, False, False)


def test_free_parking():
    assert parking_fee("car", 30, False, False) == 0


def test_paid_parking():
    assert parking_fee("car", 60, False, False) == 30


def test_exact_hour():
    assert parking_fee("car", 120, False, False) == 60


def test_partial_hour():
    assert parking_fee("car", 90, False, False) == 60


def test_ev_discount_applies():
    assert parking_fee("car", 60, True, False) == 15


def test_ev_discount_for_bike():
    assert parking_fee("bike", 60, True, False) == 5


def test_ev_discount_excluded_for_truck():
    assert parking_fee("truck", 60, True, False) == 60


def test_lost_ticket_applies():
    assert parking_fee("car", 60, False, True) == 230


def test_no_lost_ticket():
    assert parking_fee("car", 60, False, False) == 30


# Parking slot branches

def test_no_free_slots():
    assert find_slot("car", 0, False) == "full"


def test_negative_free_slots():
    assert find_slot("car", -1, False) == "full"


def test_disabled_parking():
    assert find_slot("car", 5, True) == "ground floor"


def test_truck_parking():
    assert find_slot("truck", 5, False) == "basement"


def test_normal_parking():
    assert find_slot("car", 5, False) == "any floor"


# Monthly pass branches

def test_bike_non_resident():
    assert monthly_pass("bike", False) == 500


def test_bike_resident():
    assert monthly_pass("bike", True) == 400


def test_car_non_resident():
    assert monthly_pass("car", False) == 1500


def test_car_resident():
    assert monthly_pass("car", True) == 1200


def test_invalid_pass_vehicle():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)
