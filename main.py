# coding=UTF-8
from bs4 import BeautifulSoup
import requests
import re
import time
import os

def cls():
		os.system('cls' if os.name=='nt' else 'clear')

def printPrice(i, row):
	if currency_id[i] != 4:
		txtbuffer = ['']
		if len(i) < 7:
			for x in range(5 - len(i)):
				txtbuffer.append(' ')

		newprice = getPrice(currency_id[i], row)

		try:
			profit = calculateProfit(newprice[0],newprice[1])

			return (i + ": " + ''.join(txtbuffer) + str(newprice[0])  + " → " + str(newprice[1]) + "(" + str(newprice[2]) + ")" +" Profit: " + str(profit) + "\n")
		except:
			return i + ": " + "No profit.\n"

def rawToFloat(xstring):
	out = []
	for ind, i in enumerate(xstring):
		out.append([])
		for y in i:
			if y in "1234567890.":
				out[ind].append(y)

		out[ind] = float(''.join(out[ind]))

	return out

def getPrice(itemname, row='4'):
	if row.isdigit():
		row = int(row)
	else:
		row = 4

	trade_page = 'http://currency.poe.trade/search?league=' + league + '&online=x&stock=&want=4&have=' + str(itemname)
	trade_page2 = 'http://currency.poe.trade/search?league=' + league + '&online=x&stock=&want=' + str(itemname) + '&have=4'

	page = requests.get(trade_page)
	page2 = requests.get(trade_page2)

	soup = BeautifulSoup(page.content, "html.parser")
	soup2 = BeautifulSoup(page2.content, "html.parser")

	orbtoc = soup.find_all(string=re.compile('←'))
	ctoorb = soup2.find_all(string=re.compile('→'))
	ctoorb2 = soup2.find_all(string=re.compile('←'))

	prices = [[],[],[]]
	prices[0] = rawToFloat(orbtoc[1:])
	prices[1] = rawToFloat(ctoorb)
	prices[2] = rawToFloat(ctoorb2[1:])

	try:
		return [prices[0][int(row)], prices[1][int(row)], prices[2][int(row)]]
	except IndexError:
		return "Not enough results to calculate price."

def calculateProfit(buy, sell):
	difference = buy - sell
	profit = difference / sell
	return str(round(profit*100,2)) + "%"

currency_list = ['alt', 'fuse', 'alch', 'chaos', 'gcp', 'ex', 'chrom', 'jew', 'chance',
				'chis', 'scour', 'bless', 'regret', 'regal', 'divine', 'vaal', 'wis',
				'port']

currency_id   = {i : ind + 1 for ind, i in enumerate(currency_list)}

currency_rate = {i : 'Loading...\n' for i in currency_list}

#commands =       ""
count = 0
league = raw_input("Enter league(Case sensitive):")
while True:
#	command = ['' for i in range(5)]
#	for ind, i in enumerate(input().split()):
#		command[ind] = i
#
#	if command[0] == 'price' and command[1] in currency_list:
#		print(printPrice(command[1], command[2]))
#
#	if command[0] == 'price' and command[1] == 'all':
#		for i in currency_list:
#			if currency_id[i] != 4:
#				print(printPrice(i, command[2]))
#
#	if command[0] == 'quit':
#		break
	count += 1
	for i in currency_list:
		if currency_id[i] == count and currency_id[i] != 4:
			try:
				currency_rate[i] = printPrice(i, '5')
			except TypeError:
				currency_rate[i] = 'Not enough prices to calculate.\n'
	cls()
	for i in currency_rate:
		print(currency_rate[i])
	if count == len(currency_list) + 1:
		count = 0
	time.sleep(1)
