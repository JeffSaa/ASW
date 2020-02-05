#Import Libraries needed for managing the data
#¿Why not split code into classes? and we can automate testing units

import pandas as pd
import numpy
import os

from models import provider as provider_model
from models import purchase_process as pp_model
from models import quotation as quotation_model
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--providers", dest="providers_file")
parser.add_argument("--purchase", dest="purchase_file")
parser.add_argument("--quotations", dest="quotations_file")
parser.add_argument("--scoring", dest="scoring_file")

def Price(pp,Quotations,Scoring):
	dic={'ordered_list':[],'id_provider':[],'Purchase_P':[]}
	data = pd.DataFrame(columns=('ordered_list', 'id_provider', 'Purchase_P'))
	for x in range(0,len(Quotations)):
		if pp == Quotations[x].Purchase_Process:
			dic['ordered_list'].append(Quotations[x].Unit_Price)
			dic['id_provider'].append(Quotations[x].Provider_Code)
			dic['Purchase_P'].append(Quotations[x].Purchase_Process)
	data= pd.DataFrame(dic, columns=dic.keys())								
	data = data.sort_values('ordered_list')
	pos=0
	for x in range(0,data.shape[0]):
		for y in range(0,len(Quotations)):			
			if Quotations[y].Provider_Code==data.iloc[x][1] and Quotations[y].Purchase_Process==data.iloc[x][2]:
				if x==1:					
					if data.iloc[x][0]==data.iloc[x-1][0]:	
						pos=pos-1	
				Quotations[y].Total_Points=Quotations[y].Total_Points+Scoring[pos][2]	
				pos=pos+1		

def Time(pp,Quotations,Scoring):
	dic={'ordered_list':[],'id_provider':[],'Purchase_P':[]}
	data = pd.DataFrame(columns=('ordered_list', 'id_provider', 'Purchase_P'))
	for x in range(0,len(Quotations)):
		if pp == Quotations[x].Purchase_Process:
			dic['ordered_list'].append(Quotations[x].Delivery_Time)
			dic['id_provider'].append(Quotations[x].Provider_Code)
			dic['Purchase_P'].append(Quotations[x].Purchase_Process)
	data= pd.DataFrame(dic, columns=dic.keys())								
	data = data.sort_values('ordered_list')
	pos=0
	for x in range(0,data.shape[0]):
		for y in range(0,len(Quotations)):			
			if Quotations[y].Provider_Code==data.iloc[x][1] and Quotations[y].Purchase_Process==data.iloc[x][2]:
				if x==1:					
					if data.iloc[x][0]==data.iloc[x-1][0]:	
						pos=pos-1	
				Quotations[y].Total_Points=Quotations[y].Total_Points+Scoring[pos][3]	
				pos=pos+1

def Quality_c(Providers,Quotations,Scoring):

	#"""This scores if has or not quality certification. Quality, lcompany and Vkey functions do not depend on purchase
	#process (they are or not independently), but price and time score must be compared with the rest of quotations from
	#the purchase process"""

	for x in range(0,len(Providers)):
		if Providers[x].Quality_Cert==True:
			for y in range(0,len(Quotations)):
				if Quotations[y].Provider_Code==Providers[x].Provider_ID:
					Quotations[y].Total_Points=Quotations[y].Total_Points+Scoring[0][4]

def Lcompany(Providers,Quotations,Scoring):
	for x in range(0,len(Providers)):
		if Providers[x].Local_Company==True:
			for y in range(0,len(Quotations)):
				if Quotations[y].Provider_Code==Providers[x].Provider_ID:
					Quotations[y].Total_Points=Quotations[y].Total_Points+Scoring[0][5]

def Valid_Key(Providers,Quotations,Scoring):
	for x in range(0,len(Providers)):
		for y in range(0,len(Quotations)):
			if Quotations[y].Provider_Code==Providers[x].Provider_ID:
				Quotations[y].Total_Points=Quotations[y].Total_Points+Scoring[0][1]

def Position(pp,Quotations):

	#"""Assign the position or Ranking (attribute from Quotation) of the Quotation"""

	dic={'ordered_list':[],'id_provider':[],'Purchase_P':[]}
	data = pd.DataFrame(columns=('ordered_list', 'id_provider', 'Purchase_P'))
	for x in range(0,len(Quotations)):
		if pp == Quotations[x].Purchase_Process:
			dic['ordered_list'].append(Quotations[x].Total_Points)
			dic['id_provider'].append(Quotations[x].Provider_Code)
			dic['Purchase_P'].append(Quotations[x].Purchase_Process)
	data= pd.DataFrame(dic, columns=dic.keys())								
	data = data.sort_values('ordered_list',ascending=False)
	pos=1  	
	for x in range(0,data.shape[0]):
		for y in range(0,len(Quotations)):			
			if Quotations[y].Provider_Code==data.iloc[x][1] and Quotations[y].Purchase_Process==data.iloc[x][2]:
				if x==1:					
					if data.iloc[x][0]==data.iloc[x-1][0]:	
						pos=pos-1				
				Quotations[y].Rank=pos
				pos=pos+1

def Show(pp,Quotations):

	#"""Show every quotations of the respective purchase process, but it sorts them first and then shows them """

	dic={'ordered_list':[],'pos':[]}
	data = pd.DataFrame(columns=('ordered_list', 'id_provider', 'Purchase_P'))
	for x in range(0,len(Quotations)):
		if pp == Quotations[x].Purchase_Process:
			dic['ordered_list'].append(Quotations[x].Rank)
			dic['pos'].append(x)			
	data= pd.DataFrame(dic, columns=dic.keys())								
	data = data.sort_values('ordered_list')
	print("Process with code "+str(pp))
	for x in range(0,data.shape[0]):
		if x==6:
			break
		print(str(Quotations[data.iloc[x][1]].Provider_Code)+" with score of " +str(Quotations[data.iloc[x][1]].Total_Points)+" and position "+str(Quotations[data.iloc[x][1]].Rank))		
	if data.shape[0]==0:
		print("There is no purchase process or no quotes")	

def Allpp(Purchase_items):
	for x in range(0,len(Purchase_items)):
		print("Code "+str(Purchase_items[x].Purchase_Process)+" name "+str(Purchase_items[x].Product_Name))

def Generate(Purchase_items,Quotations,Providers):

	#"""This is the function to show the menu for the user"""

	print("")
	print("1. Show purchase processes(code and name")
	print("2. Create CSV file and exit")
	print("3. Show  purchase process(complete)")
	print("4. Show Provider(individual)")
	print("5. Show Purchase_Process(individual)")
	print("6. Show Quotation(individual")
	print("7. Exit and not save")
	while True:
		try:
			print("")
			print("insert a value from 1-7")
			print("")
			elec=str(input())
			break        
		except TypeError:
			print("")
			print("invalid value")
	
	if elec=="1":
		print("")
		print("You chose option 1")
		print("")
		Allpp(Purchase_items)		
		Generate(Purchase_items,Quotations,Providers)
		
	elif elec=="2":
		while True:
			print("")
			print("Type name for the document")		
			print("")
			Name=input()	
			if Name=="":
				print("")
							
				print("type a valid name")
			
			else:
				break	

		File=Name+".csv"
		csv=open(File,"w")
		Title="Purchase_Process\n"
		csv.write(Title)
		for x in range(0,len(Purchase_items)):
			pp=Purchase_items[x].Purchase_Process
			Dic={'ordered_list':[],'pos':[]}
			Data = pd.DataFrame(columns=('ordered_list', 'pos'))
			for x in range(0,len(Quotations)):
				if pp == Quotations[x].Purchase_Process:
					Dic['ordered_list'].append(Quotations[x].Rank)
					Dic['pos'].append(x)			
			Data= pd.DataFrame(Dic, columns=Dic.keys())								
			Data = Data.sort_values('ordered_list')
			csv.write("Process with code"+str(pp)+"\n")			
			for x in range(0,Data.shape[0]):
				csv.write(str(Quotations[Data.iloc[x][1]].Provider_Code)+","+" with score of "+","+str(Quotations[Data.iloc[x][1]].Total_Points)+","+" and position "+","+str(Quotations[Data.iloc[x][1]].Rank)+"\n")

		csv.close()		
		print("File created")
		print("File created in the following path:"+str(os.getcwd()))

	elif elec=="3":
		
		while True:
			try:
				print("")
				print("Type purchase process")
				print("")
				proce=int(input())
				break        
			except ValueError:
				print("")
				print("invalid value")
		
		Show(proce,Quotations)
		Generate(Purchase_items,Quotations,Providers)		
		
	elif elec=="4":
		
		while True:
			try:
				print("")
				print("Type provider code")
				print("")
				cod=int(input())
				break        
			except ValueError:
				print("")
				print("invalid value")
		
		ver=False
		for x in range(0,len(Providers)):
			if Providers[x].Provider_ID==cod:
				Providers[x].Show_data()
				ver=True

		if ver==False:			
			print("Provider not found")
		Generate(Purchase_items,Quotations,Providers)
	elif elec=="5":
		
		while True:
			try:
				print("")
				print("Type Purchase_Process code")
				print("")
				cod=int(input())
				break        
			except ValueError:
				print("")
				print("invalid value")
		
		ver=False
		for x in range(0,len(Purchase_items)):
			if Purchase_items[x].Purchase_Process==cod:
				Purchase_items[x].Show_data()
				ver=True
		if ver==False:	
			print("")
				
			print("Purchase_Process not found")
		print("")
		Generate(Purchase_items,Quotations,Providers)
	elif elec=="6":
		print("Type Purchase_Process(quotation)")
		while True:
			try:
				print("")
				print("Type Purchase_Process(quotation)")
				print("")
				cod_pp=int(input())
				break        
			except ValueError:
				print("")
				print("invalid value")

		while True:
			try:
				print("")
				print("Type provider(quotation")
				print("")
				cod_provider=int(input())
				break        
			except ValueError:
				print("")
				print("invalid value")
		
		ver=False
		for x in range(0,len(Quotations)):
			if Quotations[x].Purchase_Process==cod_pp and Quotations[x].Provider_Code==cod_provider:
				Quotations[x].Show_data()
				ver=True
		if ver==False:
			print("Quotation not found")
		Generate(Purchase_items,Quotations,Providers)
	elif elec=="7":
		print("You are leaving")
	else:
		print("You have selected an incorrect option")
		Generate(Purchase_items,Quotations,Providers)

def Execute(Providers,Purchase_Items,Quotations,Scoring):

	#"""This executes the code
	#Quality, Lcompany y Valid_key do not depend on purchase process (they are or not independently), but price and time
	#score must be compared with the rest of quotations from the purchase process"""

	Quality_c(Providers,Quotations,Scoring)
	Lcompany(Providers,Quotations,Scoring)
	Valid_Key(Providers,Quotations,Scoring)
	for x in range(0,len(Purchase_Items)):
		Price(Purchase_Items[x].Purchase_Process,Quotations,Scoring)
		Time(Purchase_Items[x].Purchase_Process,Quotations,Scoring)
		Position(Purchase_Items[x].Purchase_Process,Quotations)
		#show(Purchase_Items[x].Purchase_Process,Quotations)

#"""These are the Sequential Steps to get information (tables) and start executing analysis"""

#"""I create 3 lists which contain providers, purchase processes and quotations, these lists have the same name
#as classes but in plural. They are initialized as empty lists, for storing information related to providers,
#purchase_items and quotations"""

Providers=[]
Purchase_Items=[]
Quotations=[]

arg = parser.parse_args()

File=pd.read_csv(arg.providers_file)

for x in File.values:
	Providers.append(provider_model.Provider(x[0],x[1],x[2],x[3],x[4]))

Scoring=pd.read_csv(arg.scoring_file).to_numpy()

Purchase_Request=pd.read_csv(arg.purchase_file)
for x in Purchase_Request.values:
	Purchase_Items.append(pp_model.Purchase_Process(x[0],x[1],x[2]))

Quotation_file=pd.read_csv(arg.quotations_file)
for x in Quotation_file.values:
	Quotations.append(quotation_model.Quotation(x[0],x[1],x[2],x[3],x[4],x[5]))

Execute(Providers,Purchase_Items,Quotations,Scoring)
Generate(Purchase_Items,Quotations,Providers)
