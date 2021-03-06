#! /usr/bin/env python3

import json
import math
import sys

def result():
	x = input('Choose the sub_slot number\n')
	#of = open('result.txt','w')
	#for x in list_cipher:
		#if len(x) != 0:
	for i in list_funcUI[x]:
		for j in list_cipher[x]:
			distance = int(i) - int(j)
			print ('FU=', i, 'C=', j,'\n','The distance =' ,distance )
			if  0 <  distance < 200:
				print ('The packet Func UI ', i,  ' apperead after Cipher Packet\n') 
				#of.write(i+'\n')
			elif  -200 < distance < 0:
				print ('The packet Func UI ', i, '  apperead before Cipher Packet\n') 
				#of.write(i+'\n')
			else:
				print ('too much range\n')	
	#of.close()

def files(namefile):
#	if par == 1:
#		namefile = 'jsonBCCH'
#	elif par == 2:
#		namefile = 'jsonSDCCH8'	
	try:
		of = open(namefile,'r')
		text = of.read()
		of.close()
		text  = json.loads(text)
		return text
	except FileNotFoundError:
		print ('No file in the folder ./\n')




def mainparse(text):
	for i in text:
		try:
			msg_type = i['_source']['layers']['gsm_a.ccch']['gsm_a.dtap.msg_rr_type']
		except KeyError:
				msg_type = 'empty'
		if msg_type == '0x0000003f':
			if 'Channel Description' in i['_source']['layers']['gsm_a.ccch']:
				timeslot = (i['_source']['layers']['gsm_a.ccch']['Channel Description']['gsm_a.rr.timeslot'])
				if timeslot in list_timeslots:
					pass
				else:
					list_timeslots.append(timeslot)

	print (' The list of timselots', list_timeslots)
	if len(list_timeslots) == 1:

		print ("There is only one timeslot\n")
	elif len(list_timeslots) > 1:
		print ("There are several timeslots\n")
	else:
		print ("There are no timeslots\n")

		
def testparse(text):
	for i in text:
		try:
			subtimeslot =  i['_source']['layers']['gsmtap']['gsmtap.sub_slot']

		except KeyError:
			subtimeslot = 'empty'

		if subtimeslot != 'empty':

			try:
				LengthField = i['_source']['layers']['lapdm']['lapdm.length_field']
			except KeyError:
				LengthField = 'empty'

			try:
				type_packet = i['_source']['layers']['gsm_a.dtap']['gsm_a.dtap.msg_rr_type']
			except KeyError:
				type_packet = 'empty'	

			if LengthField =='0x00000001':
				print ('SUB_slot =' ,subtimeslot)
				print ('Length Field =' ,LengthField)
				gsmNumber = i['_source']['layers']['gsmtap']['gsmtap.frame_nr']
				print ('GSM Number =',gsmNumber)
				print ('\n')
				list_funcUI[subtimeslot].append(gsmNumber)
			else:
				pass

			if type_packet == '0x00000035':
				gsmNumber = i['_source']['layers']['gsmtap']['gsmtap.frame_nr']
				print ('type packet =',type_packet)
				print ('GSM Number =',gsmNumber)
				print ('\n')
				list_cipher[subtimeslot].append(gsmNumber)
			else:
				pass
		else:
			pass


list_funcUI = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[]}
list_cipher = {'0':[],'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[]}
list_timeslots = []


arg = sys.argv[1]
if arg == '0C':
#	text_bcch = files(1)
	try:
		namefile = sys.argv[2]
		#text_bcch  = json.loads(text)
		text_bcch = files(namefile)
		mainparse(text_bcch)
	except IndexError:
		print ('No file\n')
elif arg == 'XS':
#	text_dcch8 = files(2)
	try:
		namefile = sys.argv[2]
	#	text = sys.argv[2]
		text_dcch8 = files(namefile)
		testparse(text_dcch8)
		print ('Func UI ',list_funcUI,'\n')
		print ('Cipher Packets ',list_cipher,'\n')
		result()
	except IndexError:
		print ('No file\n')
else:
	print ('Wrong argument\n, please type 1 for BCCH or type 2 for SDCCH8\n')





