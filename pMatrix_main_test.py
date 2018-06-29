import pMatrix_main

def test():

	results = pMatrix_main.compute([[0,6],[0,0]],[0,6])
	
	p_list = []
	for result in results:
		p = 0
		for prob in result:
			if type(prob) is list:
				for i in range(len(prob)):
					p = p + (1/prob[i])
		p_list.append(p)
			
	print("All probabilities: ", p_list)
	print("Length: ", len(p_list))
	
	
test() 