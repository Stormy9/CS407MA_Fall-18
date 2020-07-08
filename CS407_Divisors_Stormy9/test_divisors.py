from divisors import divisors

def test_one():
	assert divisors(1)==[1]

def test_two():
	assert divisors(2)==[1,2]

def test_three_to_nine():
	assert divisors(3)==[1,3]
	assert divisors(4)==[1,2,4]
	assert divisors(5)==[1,5]
	assert divisors(6)==[1,2,3,6]
	assert divisors(7)==[1,7]
	assert divisors(8)==[1,2,4,8]
	assert divisors(9)==[1,3,9]

def test_thirty_six():
	assert divisors(36)==[1,2,3,4,6,9,12,18,36]

#def test_no_2_in_3():
#	assert divisors(3) 
#	assert 2 in div_list == False
# this ^^^ did not work...
# gave NameError: name 'div_list' is not defined

#def test_2_not_in_3():
#	assert 2 in divisors(3).div_list == False
# this ^^^ did not work either...
# gave AttributeError: 'list' object has no attribute 'div_list'

# aha!  it goes like this:
def test_for_not_divisors():
	assert 2 not in divisors(3)
	assert 4 not in divisors(7)
	assert 5 not in divisors(9)


