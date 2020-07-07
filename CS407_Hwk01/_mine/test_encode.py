from encode import encode

def test_empty_string():
    assert encode("") == ""

def test_non_repeating_string():
    #assert encode("") == ""
    assert encode("a") == "a1"

def test_mostly_working_solution():
    # note 'a' on both ends of string
    assert encode("aabcccccaaa") == "a2b1c5a3"
    assert encode("aaabbbbbbcccccccccbbbbbbaaa") == "a3b6c9b6a3"
    assert encode("possum") == "p1o1s2u1m1"

