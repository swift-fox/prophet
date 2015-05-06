from main import ask
import config as cfg

def check(candidate,answers):
	for index,answer in answers.items():
		if answer!=-1 and candidate[index]!=-1 and candidate[index]!=answer:
			return False
	return True

def eliminate(candidates,answers,dataset):
	return filter(lambda candidate:check(dataset[candidate],answers),candidates)

def select(candidates,answers,dataset):
	# Coarse selection
	certainty=[0]*len(dataset[0])
	unknown=[0]*len(dataset[0])

	for candidate in candidates:
		features=dataset[candidate]

		for i in range(len(features)):
			if features[i]==1:
				certainty[i]+=1
			elif features[i]==0:
				certainty[i]-=1
			else:
				unknown[i]+=1

	certainty=[abs(x) for x in certainty]

	#print 'Certainty: '+str(certainty)
	#print 'Unknown: '+str(unknown)

	weighted=[c+u for c,u in zip(certainty,unknown)]

	for i in answers:
		weighted[i]=len(candidates)

	i=weighted.index(min(weighted))
	if weighted[i]<len(candidates):
		return i

	# Refined selection
	unknown=[len(candidates) if x==0 else x for x in unknown]

	for t in range(cfg.unknown_probe_times):
		i=unknown.index(min(unknown))
		if i in answers:
			unknown[i]=len(candidates)	
		elif unknown[i]<len(candidates):
			return i

	return -1

def round_A(candidates,answers,dataset):
	candidates=list(candidates)
	while True:
		index=select(candidates,answers,dataset)
		if index==-1:
			break

		answers[index]=ask(index)
		if answers[index]!=-1:
			candidates=eliminate(candidates,answers,dataset)

		print candidates
	return candidates,answers

def distance(a,b):
	d=0
	for u,v in zip(a,b):
		if u+v==1:
			d+=1
	return d

def round_B(answers,dataset):
	vector=[-1]*len(dataset[0]) if dataset else []
	for index,answer in answers.items():
		vector[index]=answer

	candidates=[i for i,data in enumerate(dataset) if distance(vector,data)<=cfg.distance]
	print "Round B candidates:"+str(candidates)

	_answers={}
	for index in answers:
		_answers[index]=-1

	candidates,_answers=round_A(candidates,_answers,dataset)
	
	for i,v in _answers.items():
		if v!=-1:
			answers[i]=v

	return candidates,answers
