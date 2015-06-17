#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import re

#DEBUG=True
DEBUG=False

def get_users(file_name):
	users=[]
	user={}
	new_user=False
	for line in open(file_name):
		if DEBUG:
			print("line: %s" % line)
		if "BEGIN:VCARD" in line:
			new_user=True
			user={}
			user["tel"]=[]
			user["email"]=[]
			if DEBUG:
				print("new_user set True")
		if "END:VCARD" in line:
			new_user=False
			users.append(user)
		if new_user:
			if re.search(r'^FN:.*', line) is not None:
				user["name"]=line.split(":")[1].strip('\n').strip('\r')
			elif re.search(r'^EMAIL.*', line) is not None:
				user["email"].append(line.split(":")[1].strip('\n').strip('\r'))
#user["email"].append(line.split(":")[1].strip('\n').replace(r'\r',''))
			elif re.search(r'^TEL.*', line) is not None:
				user["tel"].append(line.split(":")[1].strip('\n').strip('\r'))
	return users


# ================ Начало ==============
if len(sys.argv) < 3:
	print("Необходимо два параметра: входной файл vcf и выходной файл csv")
	print("Пример:")
	print("%s contacts.csv book.csv:" % sys.argv[0])
	print("Выход")
	raise SystemExit(1)

users=get_users(sys.argv[1])

out=open(sys.argv[2], "w+")

# Выводим имена и телефоны:
for user in users:
	if "name" in user:
		if len(user["name"]):
			if "tel" in user:
				if len(user["tel"]):
					out.write(user["name"].decode('utf-8').encode('cp1251')  )
					for num_tel in [0,1,2]:
						# ';' необходимо писать вне зависимости от наличия телефонов:
						out.write(";")
						if len(user["tel"])>num_tel:
							out.write("%s" % user["tel"][num_tel])
					#	print("Имя: %s, тел: %s" % (user["name"],user["tel"][0]) )
					out.write("\n")
out.close()
	
