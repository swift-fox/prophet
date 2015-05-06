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
		update(result,answers)
		data.save(cfg.questions,labels,dataset)
		print 'Thank you for playing!'
		exit()

	candidates,answers=round_B(answers,dataset)

	best_match=match(candidates,answers,dataset)
	print 'My guess is: '+labels[best_match]
	correct=ask2('Am I correct? (y/n):')
	if correct:
		result=dataset[best_match]
		update(result,answers)
		data.save(cfg.questions,labels,dataset)
		print 'Thank you for playing!'
		exit()

	print 'Please tell me what you think:'
	label=raw_input()
	if label==labels[best_match]:
		print 'Thank you for playing!'
		exit()

	if label not in labels:
		labels.append(label)
		dataset.append(result)
		result=[-1]*len(dataset[0])
		update(result,answers)
		data.save(cfg.questions,labels,dataset)
		print 'Thank you for playing!'
		exit()

	i=labels.index(label)
	if i in candidates:
		attrs=get_unknowns(dataset[i],answers)
		if attrs:
			print 'Please answer several questions about '+label+'.'
			n=0
			for index in attrs:
				answers[index]=ask(index)
				if n>=cfg.max_questions:
					break
		else:
			print 'Please input a question that is true for '+label+':'
			question=raw_input().strip()
			cfg.questions.append(question)
			for item in dataset:
				item.append(-1)
			dataset[i][-1]=1

		update(dataset[i],answers)
		data.save(cfg.questions,labels,dataset)
		print 'Thank you for playing!'
	else:
		print 'DEBUG: malicious user'
		print 'Thank you for playing!'
		exit(0)
