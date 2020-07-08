# take a number input/parameter/argument... 
# ... find & reutrn it's divisors as a list
def divisors(num):
	div_list=[]
	for i in range(1,num+1):
		if(num%i==0):
			div_list.append(i)
	return div_list
