#!/usr/bin/env python

import config as cfg

n=0

def ask(index):
	global n
	n+=1
	print 'Q{0}: {1}'.format(n,cfg.questions[index])

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

def ask2(question):
	answer=raw_input(question)
	while True:
		if answer=='y' or answer=='':
			return 1
		elif answer=='n':
			return 0
		else:
			answer=raw_input('Please input \'y\' or \'n\':')

def get_unknowns(features,answers):
	res=[]
	for i in range(len(features)):
		if features[i]==-1 and ((i not in answers) or (i in answers and answers[i]==-1)):
			res.append(i)
	return res

def learn(answers,candidates,label,labels,questions,dataset):
	# New data
	if label not in labels:
		labels.append(label)

		feature=[-1]*len(dataset[0])
		dataset.append(feature)
	else:
		# Existing data
		i=labels.index(label)
		if i in candidates:
			feature=dataset[i]
		else:
			print 'DEBUG: malicious user'
			return

	# Ask about unknown attributes
	global n
	n=0
	unknowns=get_unknowns(feature,answers)
	if unknowns:
		print 'Please answer several questions about '+label+'.'
		for i in unknowns:
			answers[i]=ask(i)
			if n>=cfg.max_questions:
				break

	# Input a new question to distinguish the object
	if n<cfg.max_questions:
		print 'Please input a question that is true for '+label+':'
		question=raw_input().strip()
		if question:
			questions.append(question)
	
			for data in dataset:
				data.append(-1)
			feature[-1]=1

	merge_answer(feature,answers)

def merge_answer(feature,answers):
	for index,answer in answers.items():
		if answer!=-1:
			feature[index]=answer

def match(candidates,answers,dataset):
	res=[]
	for candidate in candidates:
		matches=0
		for index,answer in answers.items():
			if answer==dataset[candidate][index]:
				matches+=1
		res.append((matches,candidate))
	match_list=[c for m,c in sorted(res,reverse=True)]
	return match_list[0]

if __name__=='__main__':
	import data
	from core import round_A,round_B

	cfg.questions,labels,dataset=data.load()

	print 'Please think of a figure or an object in your mind.'
	print 'Then answer questions with "y", "n" or "d" (don\'t know).'
	print 'Press ENTER to continue.'
	raw_input()

	candidates=[x for x in range(len(labels))]
	candidates,answers=round_A(candidates,{},dataset)

	if max(answers.values())==-1:
		print 'I don\'t know what do you know.'
		print 'Thank you for playing!'
		exit()

	best_match=match(candidates,answers,dataset)
	print 'My guess is: '+labels[best_match]
	correct=ask2('Am I correct? (y/n):')
	if correct:
		result=dataset[best_match]
		merge_answer(result,answers)
		data.save(cfg.questions,labels,dataset)
		print 'Thank you for playing!'
		exit()

	candidates,answers=round_B(answers,dataset)

	if best_match in candidates:
		candidates.remove(best_match)

	best_match=match(candidates,answers,dataset)
	print 'My guess is: '+labels[best_match]
	correct=ask2('Am I correct? (y/n):')
	if correct:
		result=dataset[best_match]
		merge_answer(result,answers)
		data.save(cfg.questions,labels,dataset)
		print 'Thank you for playing!'
		exit()

	print 'Please tell me what you think:'
	label=raw_input()
	if label==labels[best_match]:
		print 'Thank you for playing!'
		exit()

	learn(answers,candidates,label,labels,cfg.questions,dataset)

	data.save(cfg.questions,labels,dataset)
	print 'Thank you for playing!'
