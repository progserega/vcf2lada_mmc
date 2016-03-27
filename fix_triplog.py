#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import re
import time
import datetime

#DEBUG=True
DEBUG=False
#Дата;Время;Пробег;Длительность;Средняя скорость;Расход, Л/100;Расход, Л;Стоимость 

def check_dubl(record1, record2):
	if record1["date"]==record2["date"] and \
	record1["time"]==record2["time"] and \
	record1["probeg"]==record2["probeg"] and \
	record1["dlit"]==record2["dlit"] and \
	record1["speed_average"]==record2["speed_average"] and \
	record1["rashod_lit_na_100km"]==record2["rashod_lit_na_100km"] and \
	record1["rashod_lit"]==record2["rashod_lit"] and \
	record1["price"]==record2["price"]:
		if DEBUG:
			print("duble found")
		return True
	return False

def pars_triplog(file_name):
	num_in_lines=0
	full_probeg=0
	full_fuel=0
	triplog=[]
	skip=False
	for line in open(file_name):
		num_in_lines+=1
		record={}
		if DEBUG:
			print("line: %s" % line)
		if re.search(r'^[0-9].*', line) is None:
			if DEBUG:
				print("Skip line: %s" % line)
			continue
		data=line.split(';')
		record["date"]=data[0]
		record["time"]=data[1]
		record["probeg"]=data[2]
		record["dlit"]=data[3]
		record["speed_average"]=data[4]
		record["rashod_lit_na_100km"]=data[5]
		record["rashod_lit"]=data[6]
		record["price"]=data[7]
		record["struct_time"]=time.strptime("%s %s"%(record["date"],record["time"]), "%d.%m.%y %H:%M")
		if DEBUG:
			print("%s %s" % (record["date"],record["time"]))
	    # ищем место, куда вставить по дате:
		skip=False
		for index in range(0,len(triplog)):
			if DEBUG:
				print("index=%d"%index)
			if time.mktime(triplog[index]["struct_time"])==time.mktime(record["struct_time"]):
				if check_dubl(triplog[index],record):
					# пропуск дубля
					skip=True
					break
			if time.mktime(triplog[index]["struct_time"])<time.mktime(record["struct_time"]):
				if DEBUG:
					print("insert line: %s" % line)
				triplog.insert(index,record)
				full_probeg+=float(record["probeg"].replace(",","."))
				full_fuel+=float(record["rashod_lit"].replace(",","."))
				skip=True
				break
		if not skip:
			if DEBUG:
				print("append line: %s" % line)
			triplog.append(record)
			full_probeg+=float(record["probeg"].replace(",","."))
			full_fuel+=float(record["rashod_lit"].replace(",","."))
	print("num_in_lines=%d, triplog.len=%d"%(num_in_lines,len(triplog)))
	print("Статистика:")
	print("Полный пробег: %d км\nИзрасходованно топлива: %d л"%(full_probeg,full_fuel))
	return triplog


# ================ Начало ==============
if len(sys.argv) < 3:
	print("Скрипт убирает дубли из файла статистики поездок Лады и сортирует по дате выходной файл.")
	print("Нужно два параметра - входной файл TripLog.csv и выходной файл.")
	print("Использование:")
	print("%s входной_TripLog.csv выходной_TripLog.csv" % sys.argv[0])
	raise SystemExit(1)

triplog=pars_triplog(sys.argv[1])
#sys.exit(0)

out=open(sys.argv[2], "w+")

# Выводим имена и телефоны:
for record in triplog:
	res="%s;%s;%s;%s;%s;%s;%s;%s"%(\
			record["date"],\
			record["time"],\
			record["probeg"],\
			record["dlit"],\
			record["speed_average"],\
			record["rashod_lit_na_100km"],\
			record["rashod_lit"],\
			record["price"]\
			)
	out.write(res.decode('utf-8').encode('cp1251')  )
#out.write("\n")
out.close()
	
