#coding:utf-8
#from __future__ import division
#import networkx as nx
#import matplotlib.pyplot as plt
import random
from sys import argv

alpha = 7
beta = 1
gamma = 0.0
LearningRate = 0.001
filename = 'well-mix-TFT-r=0.txt'

def CBLM(BA_network): 
	utilities_ALLC = 0
	num_ALLC = 0
	mean_ALLC = 0
	utilities_ALLD = 0
	num_ALLD = 0
	mean_ALLD = 0
	utilities_TFT = 0
	num_TFT = 0
	mean_TFT = 0
	
	for i in BA_network.nodes():
		if BA_network.node[i]['strategy'] == 'ALLC':
			num_ALLC += 1
			utilities_ALLC += BA_network.node[i]['utility']
		elif BA_network.node[i]['strategy'] == 'ALLD':
			num_ALLD += 1
			utilities_ALLD += BA_network.node[i]['utility']
		elif BA_network.node[i]['strategy'] == 'TFT':
			num_TFT += 1
			utilities_TFT += BA_network.node[i]['utility']
	
	if num_ALLC == 0:
		mean_ALLC = 0
	else:	
		mean_ALLC = utilities_ALLC / num_ALLC
	
	if num_ALLD == 0:
		mean_ALLD = 0
	else:
		mean_ALLD = utilities_ALLD / num_ALLD
		
	if num_TFT == 0:
		mean_TFT = 0
	else:	
		mean_TFT = utilities_TFT / num_TFT - gamma
	
	print( "ALLC_num: %d, ALLD_num: %d, TFT_num: %d" % (num_ALLC, num_ALLD, num_TFT))
	#print "ALLC: %d, ALLD: %d, TFT: %d" % (utilities_ALLC, utilities_ALLD, utilities_TFT)	
	#print "mean_ALLC: %f, mean_ALLD: %f, mean_TFT: %f" % (mean_ALLC, mean_ALLD, mean_TFT)	
	
	max_utility = max([mean_ALLC, mean_ALLD, mean_TFT])
	#print "max_utility is " + str(max_utility)
	best_strategies = []
	if mean_ALLC == max_utility:
		best_strategies.append('ALLC')
	if mean_ALLD == max_utility:
		best_strategies.append('ALLD')
	if mean_TFT == max_utility:
		best_strategies.append('TFT')
	
	#print best_strategies
	
	for i in BA_network.nodes():
		index = random.randint(0,len(best_strategies)-1)
		target_strategy = best_strategies[index]
		#print "target_strategy is " + target_strategy
		if not BA_network.node[i]['strategy'] == target_strategy:
			rand = random.random()
			if rand < LearningRate:
				old_strategy = BA_network.node[i]['strategy']
				BA_network.node[i]['strategy'] = target_strategy
				#print "agent %d from %s changes to %s" % (i, old_strategy, target_strategy)
	# print "agent " + str(user)
	# neighbors = BA_network.neighbors(user)
	# max_utility = -100
	# best_user = -1
	# for u in neighbors:
		# print "user " + str(u)
		# print BA_network.node[u]
		# if BA_network.node[u]['utility'] > max_utility:
			# best_user = u
			# max_utility = BA_network.node[u]['utility']
	# return best_user
		

def Fractions(BA_network): #不用变化
	num_ALLC = 0
	num_ALLD = 0
	num_TFT = 0
	for i in BA_network.nodes():
		if BA_network.node[i]['strategy'] == 'ALLC':
			num_ALLC += 1
		elif BA_network.node[i]['strategy'] == 'ALLD':
			num_ALLD += 1
		elif BA_network.node[i]['strategy'] == 'TFT':
			num_TFT += 1
	return [num_ALLC,num_ALLD,num_TFT]

def Initialization(BA_network): #不用变化
	Utility_clean(BA_network)
	Strategy_Initialization(BA_network)

def Perform_a_trans(BA_network, requester, provider): #变化
	strategy_requester = BA_network.node[requester]['strategy']
	strategy_provider = BA_network.node[provider]['strategy']
	#print "requester %d is %s" % (requester, strategy_requester)
	#print "provider %d is %s" % (provider, strategy_provider)
	if strategy_provider == 'ALLC':
		#print "provider is ALLC"
		#print "cooperation happen!"
		BA_network.node[requester]['utility'] += alpha
		BA_network.node[provider]['utility'] -= beta
		BA_network.node[provider]['last_behavior'] = 'Cooperation'
	elif strategy_provider == 'ALLD':
		#print "provider is ALLD"
		#print "defection happen!"
		BA_network.node[requester]['utility'] += 0
		BA_network.node[provider]['utility'] -= 0
		BA_network.node[provider]['last_behavior'] = 'Defection'
	elif strategy_provider == 'TFT': #需要就行修改
		# if the last behavior of requester is cooperation
		last_behavior = BA_network.node[requester]['last_behavior']
		if last_behavior == 'Cooperation':
			#print "cooperation happen!"
			BA_network.node[requester]['utility'] += alpha
			BA_network.node[provider]['utility'] -= beta
			BA_network.node[provider]['last_behavior'] = 'Cooperation'
		elif last_behavior == 'Defection':
			#print "defection happen!"
			BA_network.node[requester]['utility'] += 0
			BA_network.node[provider]['utility'] -= 0
			BA_network.node[provider]['last_behavior'] = 'Defection'
	#print BA_network.node[requester]
	#print BA_network.node[provider]
	
def Rounds(num, BA_network): #不用变化
	file = open(filename, 'w')
	for i in xrange(0, num):
		fc, fd, fr = Fractions(BA_network)
		text = "%d %f %f %f \n" % (i, fc/1000, fd/1000, fr/1000)
		file.write(text)
		print 'ALLC: ' + str(fc) + ", ALLD: " + str(fd) + ", TFT: " + str(fr)
		Transaction(BA_network)
		CBLM(BA_network)
		Utility_clean(BA_network)	
	file.close()
	
def Strategy_Initialization(BA_network): #改变
	# for i in BA_network.nodes():
		# BA_network.node[i]['last_behavior'] = 'Cooperation'
		# rand = random.random()
		# if rand < 1/3:
			# BA_network.node[i]['strategy'] = 'ALLC'
		# elif rand < 2/3:
			# BA_network.node[i]['strategy'] = 'ALLD'
		# else:
			# BA_network.node[i]['strategy'] = 'TFT'	
	for i in BA_network.nodes():
		BA_network.node[i]['last_behavior'] = 'Cooperation'
		for i in xrange(0,333):
			BA_network.node[i]['strategy'] = 'ALLC'
		for i in xrange(333, 666):
			BA_network.node[i]['strategy'] = 'ALLD'
		for i in xrange(666,1000):
			BA_network.node[i]['strategy'] = 'TFT'

# def Strategy_update(BA_network):
	# for i in BA_network.nodes():
		# print "***********************"
		# print 'agent ' + str(i)
		# utility = BA_network.node[i]['utility']
		# #print 'agent %d is %d' % (i, utility)
		# neighbors = CBLM(BA_network, i)
		# print 'the best neighbors is ' + str(neighbors)
		
	
def Transaction(BA_network): #需要改变
	for i in BA_network.nodes():
		#print "#######################"
		#print "agent " + str(i)
		#print BA_network.node[i]
		requester = i
		neighbors = BA_network.neighbors(i)
		neighbors_list = []
		for user in neighbors:
			neighbors_list.append(user)
		#print neighbors_list
		index = random.randint(0, len(neighbors_list)-1)
		provider = neighbors_list[index]
		#print "requester " + str(requester) + " will interact with provider " + str(provider)
		Perform_a_trans(BA_network, requester, provider)
		
def Utility_clean(BA_network):
	for i in BA_network.nodes():
		BA_network.node[i]['utility'] = 0

if __name__ == '__main__':
	G=nx.complete_graph(1000)
	#pos  = nx.spring_layout(G)
	#nx.draw(G,pos)
	#plt.show()
	G.nodes() #显示BA图的所有点
	#设置节点0的策略
	Initialization(G)
	timeslots = 30000
	Rounds(timeslots, G)
	