from divisors import divisors


def test_one():
    assert divisors(1) == [1]


def test_two():
    assert divisors(2) == [1, 2]


def test_100():
    assert 50 in divisors(100)
    assert 25 in divisors(100)
    assert 10 in divisors(100)


def test_negatives():
    assert 3 not in divisors(7)
    assert 5 not in divisors(11)


def test_product_of_primes():
    assert divisors(901) == [1, 17, 53, 901]
