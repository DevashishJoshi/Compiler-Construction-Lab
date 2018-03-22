def first(s, productions):
	
	if len(s)<=0:
		return {}

	c = s[0] #First character
	first_set = set() #Set to store first
	if c.isupper():
		#Non terminal
		for st in productions[c]: #For each production in the non terminal
			if st == '@' : #epsilon production
				if len(s)!=1 : #If there are more characters after c 
					first_set = first_set.union( first(s[1:], productions) )
				else : #No more characters
					first_set = first_set.union('@')
			else :
				f = first(st, productions) #Not an epsilon production
				first_set = first_set.union(x for x in f)
	else:
		#Terminal
		first_set = first_set.union(c)
	return first_set