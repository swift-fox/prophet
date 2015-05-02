#!/usr/bin/env python

import sys

def check(candidate,answers):
	for index,answer in answers.items():
		if (answer==1 or answer==0) and candidate[index]!=answer:
			return False
	return True

def eliminate(candidates,answers,dataset):
	return filter(lambda candidate:check(dataset[candidate],answers),candidates)

def select(candidates,answers,dataset):
	if not candidates or not dataset:
		return -1

	certainty=[]
	for candidate in candidates:
		features=dataset[candidate]
		certainty+=[0]*(len(features)-len(certainty))

		for i in range(len(features)):
			if features[i]==1:
				certainty[i]+=1
			elif features[i]==0:
				certainty[i]-=1

	certainty=[abs(x) for x in certainty]

	for i,answer in answers.items():
		certainty[i]=123#sys.maxint

	print 'Certainty: '+str(certainty)
	if min(certainty)==len(candidates):
		return -1
	else:
		return certainty.index(min(certainty))

def ask(n,question):
	print 'Q{0}: {1}'.format(n,question)

	while True:
		answer=raw_input()
		if answer=='y':
			return 1
		elif answer=='n':
			return 0
		elif answer=='d':
			return -1
		else:
			print 'Please input \'y\', \'n\' or \'d\'.'

if __name__=='__main__':
	import dataset

	questions,labels,features=dataset.load()

	print 'Please think of a figure or an object in your mind.'
	print 'Then answer questions with "y", "n" or "d" (don\'t know).'
	print 'Press ENTER to continue.'
	raw_input()

	answers={}
	candidates=[n for n in range(len(labels))]

	n=0
	while True:
		index=select(candidates,answers,features)
		if index==-1:
			break

		n+=1
		answers[index]=ask(n,questions[index])
		candidates=eliminate(candidates,answers,features)
		print candidates

	if candidates:
		print 'My guess is: '+labels[candidates[0]]
	else:
		print 'Unknown'

	dataset.save(questions,labels,features)
