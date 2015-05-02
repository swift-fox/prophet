#!/usr/bin/env python

def data_filter(index,value,dataset,mask):
	filtered=[data for data in dataset if data[index]==value]

	mask[index]=value

	if len(filtered):
		for i in range(len(mask)):
			if mask[i]!=-1:	# Decided
				continue

			for data in filtered:
				if data[i]!=filtered[0][i]:
					break
			else:
				mask[i]=filtered[0][i]

	return filtered,mask

def most_uncertain(dataset):
	length=len(dataset[0])
	uncertainty=[0]*length
	for data in dataset:
		for i in range(length):
			uncertainty[i]+=1 if data[i] else -1

	uncertainty=[abs(x) for x in uncertainty]
	minimal=min(uncertainty)

	return uncertainty.index(minimal)

if __name__=='__main__':
	import dataset

	questions,labels,features=dataset.load()

	print 'Please think of an object in your mind.'
	print 'Then answer questions with "y", "n", "d" (don\'t know) or i (irrelevant).'
	print 'Press ENTER to continue.'
	raw_input()

	answers={}

	qn=0;
	while True:
		if len(dataset)==1:
			break
	
		i=most_uncertain(dataset)

		qn+=1
		print 'Q'+str(qn)+': '+questions[i]

		while True:
			answer=raw_input()
			if answer=='y':
				value=1
				break
			elif answer=='n':
				value=0
				break
			else:
				print 'Please input \'y\' or \'n\'.'

		dataset,mask=data_filter(i,value,dataset,mask)

		if len(dataset)==0:
			break

		for bit in mask:
			if bit!=-1:
				break
		else:
			break

	if dataset:
		for label,data in zip(labels,_dataset):
			if data==dataset[0]:
				print 'My guess is: '+label
	else:
		print 'Unknown'

	dataset.save(questions,labels,features)
