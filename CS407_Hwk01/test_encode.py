from encode import encode


def test_empty_string():
    print("testing empty")
    assert encode("") == ""


def test_non_repeating_string():
    assert encode("a") == "a"


def test_final_solution():
    assert encode("aabcccccaaa") == "a2b1c5a3"


def test_several_edge_cases():
    assert encode("abc") == "abc"
    assert encode("aabbaa") == "aabbaa"


def test_longer_string_that_should_not_be_encoded():
    assert encode ("mississippi") == "mississippi"
