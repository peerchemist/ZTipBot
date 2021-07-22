from src import util

import pytest


def test_find_amount():
    assert util.find_amount("$tip @belovachap 10 ppc") == 10.0
    assert util.find_amount("$tip @belovachap 10.000001 ppc") == 10.000001

    with pytest.raises(util.TipBotException, match="amount_not_found"):
        util.find_amount("$tip @belovachap -10 ppc")

    with pytest.raises(util.TipBotException, match="too_many_decimals"):
        util.find_amount("$tip @belovachap 10.0000000 ppc")

