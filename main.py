#!/usr/bin/env python

import sys

def check(candidate,answers):
	for index,answer in answers.items():
		if answer!=-1 and candidate[index]!=-1 and candidate[index]!=answer:
			return False
	return True

def eliminate(candidates,answers,dataset):
	return filter(lambda candidate:check(dataset[candidate],answers),candidates)

def select(candidates,answers,dataset):
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
	combined=[abs(x)+u for x,u in zip(certainty,unknown)]

	for index,answer in answers.items():
		combined[index]=len(candidates)
		certainty[index]=len(candidates)

	#print 'Certainty: '+str(certainty)
	#print 'Combined: '+str(combined)
	if min(combined)==len(candidates):
		if len(candidates)!=1 and min(certainty)!=len(candidates) and min(certainty)!=0:
			for index in range(len(certainty)):
				if certainty[index]==len(candidates):
					certainty[index]=0
			return certainty.index(max(certainty))
		else:
			return -1
	else:
		return combined.index(min(combined))

def ask(n,question):
	print 'Q{0}: {1}'.format(n,question)

	while True:
		answer=raw_input().strip()
		if answer=='y':
			return 1
		elif answer=='n':
			return 0
		elif answer=='d':
			return -1
		else:
			print 'Please input \'y\', \'n\' or \'d\'.'

def get_unknowns(features,answers):
	res=[]
	for i in range(len(features)):
		if features[i]==-1 and ((i not in answers) or (i in answers and answers[i]==-1)):
			res.append(i)
	return res

def update(item,answers):
	for index,answer in answers.items():
		if answer!=-1:
			item[index]=answer

def match(candidates,answers,dataset):
	res=[]
	for candidate in candidates:
		matches=0
		for index,answer in answers.items():
			if answer==dataset[candidate][index]:
				matches+=1
		res.append((matches,candidate))
	return [c for m,c in sorted(res,reverse=True)]

if __name__=='__main__':
	import data
	import config as cfg

	questions,labels,dataset=data.load()

	print 'Please think of a figure or an object in your mind.'
	print 'Then answer questions with "y", "n" or "d" (don\'t know).'
	print 'Press ENTER to continue.'
	raw_input()

	answers={}
	candidates=[n for n in range(len(labels))]

	n=0
	while True:
		index=select(candidates,answers,dataset)
		if index==-1:
			break

		n+=1
		answers[index]=ask(n,questions[index])
		if answers[index]!=-1:
			candidates=eliminate(candidates,answers,dataset)
		#print candidates

	matches=match(candidates,answers,dataset)
	print 'My guess is: '+labels[matches[0]]
	answer=raw_input('Am I correct? (y/n):')
	while True:
		if answer=='y' or answer=='n':
			break
		else:
			answer=raw_input('Please input \'y\' or \'n\':')

	if answer=='y':
		result=dataset[candidates[0]]
	else:
		print 'Please tell me what you think:'
		label=raw_input()
		
		if label==labels[matches[0]]:
			print 'DEBUG: malicious user.'
			print 'Thank you for playing!'
			exit()

		for candidate in candidates:
			if label==labels[candidate]:
				attrs=get_unknowns(dataset[candidate],answers)
				if attrs:
					print 'Please answer several questions about '+label+'.'
					n=0
					for index in attrs:
						n+=1
						answers[index]=ask(n,questions[index])
						if n>=cfg.max_questions:
							break
				else:
					print 'Please input a question that is true for '+label+':'
					question=raw_input().strip()
					questions.append(question)
					for item in dataset:
						item.append(-1)
					dataset[candidate][-1]=1
				result=dataset[candidate]
				break
		else:
			if label in labels:
				print 'DEBUG: malicious user.'
				print 'Thank you for playing!'
				exit()
			else:
				result=[-1]*len(dataset[0]) if dataset else []
				labels.append(label)
				dataset.append(result)

	update(result,answers)
	data.save(questions,labels,dataset)
	print 'Thank you for playing!'
