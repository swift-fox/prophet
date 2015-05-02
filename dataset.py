#!/usr/bin/env python

import config as cfg

def conv_load(attribute):
	if attribute=='0':
		return 0
	elif attribute=='1':
		return 1
	else:	# ? or other things
		return -1

def conv_save(attribute):
	if attribute==0:
		return '0'
	elif attribute==1:
		return '1'
	else:	# ? or other things
		return '?'

def load():
	f=open(cfg.quesitons,'r')
	questions=f.readlines()
	f.close()
	questions=[question.strip() for question in questions]

	features=[]
	labels=[]
	max_len=0

	f=open(cfg.dataset,'r')
	for line in f.readlines():
		if not line:
			continue	

		label,attributes=line.split(':',1)
		labels.append(label.strip())

		attributes=attributes.split(',')
		features.append([conv_load(attr.strip()) for attr in attributes])

		if len(attributes)>max_len:
			max_len=len(attributes)
	f.close()
	
	for feature in features:
		feature+=[-1]*(max_len-len(feature))

	return questions,labels,features

def save(questions,labels,features):
	f=open(cfg.quesitons,'w')
	for question in questions:
		f.write(question+'\n')
	f.close()

	f=open(cfg.dataset,'w')
	for label,feature in zip(labels,features):
		attributes=','.join(map(conv_save,feature))
		f.write(label+':\t'+attributes+'\n')
	f.close()

if __name__=='__main__':
	print '--DEBUG MODE--'

	raw_input('load:')
	questions,labels,features=load()

	print 'questions:'
	print questions
	print 'labels:'
	print labels
	print 'features:'
	print features

	raw_input('save:')
	save(questions,labels,features)

	raw_input('load:')
	questions,labels,features=load()

	print 'questions:'
	print questions
	print 'labels:'
	print labels
	print 'features:'
	print features

	print '-----DONE-----'
