from src import util

import pytest


def test_find_amount():
    assert util.find_amount("$tip @belovachap 10 ppc") == 10.0
    assert util.find_amount("$tip @belovachap 10.000001 ppc") == 10.000001

    with pytest.raises(util.TipBotException, match="amount_not_found"):
        util.find_amount("$tip @belovachap -10 ppc")

    with pytest.raises(util.TipBotException, match="too_many_decimals"):
        util.find_amount("$tip @belovachap 10.0000000 ppc")


def test_find_address():

    assert util.find_address("$tip FouNdAtiOn 10 ppc") == "p92W3t7YkKfQEPDb7cG9jQ6iMh7cpKLvwK"
    assert util.find_address("$withdraw PBGM16nDjX4x8NXrdKHDk1gsAndVHzh3fv 10") == "PBGM16nDjX4x8NXrdKHDk1gsAndVHzh3fv"
    assert util.find_address("$withdraw pc1qzv4xpgjhdqjmj36qcpmz94k2q2ahzx3qtzeava 1") == "pc1qzv4xpgjhdqjmj36qcpmz94k2q2ahzx3qtzeava"