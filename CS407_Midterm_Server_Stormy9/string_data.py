def string_data_dict(input):
	d={}
	d['length']=len(input)
	d['reversed']="".join(reversed(input))
	d['upper']=input.upper()
	return d

# this all was working, btw...
#def string_data(input):
#	s=[]
#	s.append(len(input))
#	s.append(input.upper())
#	s.append("".join(reversed(input)))
#	return s

# print statements just for testing
#print(string_data("wolf"))
#print(string_data_dict("wolf"))
