from first import first

def follow(s, productions, follow_dict):
	
	if len(s)!=1 :
		return follow_dict

	if follow_dict[s][1]: #Follow already known
		return follow_dict

	for key in productions:
		for value in productions[key]:
			#Serach RHS of all productions
			f = value.find(s)
			if f!=-1: #Found in RHS
				if f==(len(value)-1): #Last character in RHS
					if key!=s: #To avoid infinite loop
						if follow_dict[key][1]: #Follow already known
							temp = follow_dict[key][0]
						else: #Find follow
							follow_dict = follow(key, productions, follow_dict)
							temp = follow_dict[key][0]
						follow_dict[s][0] = follow_dict[s][0].union(temp)
				else: #Not the last character
					first_of_next = first(value[f+1:], productions) #Find first of next
					if '@' in first_of_next: #epsilon production in first of next
						if key!=s: #To avoid infinite loop
							if follow_dict[key][1]: #Follow already known
								temp = follow_dict[key][0]
							else: #Find follow
								follow_dict = follow(key, productions, follow_dict)
								temp = follow_dict[key][0]
							follow_dict[s][0] = follow_dict[s][0].union(temp)
							follow_dict[s][0] = follow_dict[s][0].union(first_of_next) - {'@'}
					else: #Not an epsilon production
						follow_dict[s][0] = follow_dict[s][0].union(first_of_next)
	follow_dict[s][1]=True
	return follow_dict