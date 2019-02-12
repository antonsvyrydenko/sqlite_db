# https://sqliteonline.com/

import sqlite3
import sys

def get_artist_id(artist):
	decision=''
	connection=sqlite3.connect('database.db')
	cursor=connection.cursor()
	cursor.execute("select id from artist where name like '%"+artist+"%'")
	results = cursor.fetchall()
	if len(results)==1:
		for val in results:
			return val[0]
	elif len(results)>1:
		while not decision:
			decision=raw_input("Seems like we have a problem here.\nChoose which one artist u want to use:\n")
		if decision:
			return decision

	connection.commit()
	connection.close()

def insert_exec(op):
	connection=sqlite3.connect('database.db')
	cursor=connection.cursor()
	cursor.execute(op)
	connection.commit()
	connection.close()

def select_exec(op,type_):
	action=''
	connection=sqlite3.connect('database.db')
	cursor=connection.cursor()
	cursor.execute(op)
	results = cursor.fetchall()
	print "="*40
	print "This is "+str(type_)+" select query."
	print "="*40
	if results:
		print "\nHere's band(s) in DB with specified name:\n"
		for val in results:
			print val[0],"\t",val[1],"\t",val[2],"\n"
		while not action:
			global action
			action=raw_input("What to do? 1 - ignore/confirm and add anyway; 0 - abandon and exit.\n")
		if action=='1':
			print "Inserting..."
			return action
		else:
			print "Insert "+str(type_)+" aborted."
			sys.exit(1)
	else:
		print "\nHere's no band in DB with specified name.\n"
		while not action:
			global action
			action=raw_input("What to do? 2 - add band; 0 - abandon and exit.\n")
		if action=='2':
			print "Inserting..."
			return action
		else:
			print "Insert "+str(type_)+" aborted."
			sys.exit(1)

	connection.commit()
	connection.close()
	
operation=''
valid=['artist','cd','cd-artist']
name=''
country=''
title=''
year=''
type_=''
art=''
genres=''
rate=''
artist=''
try:
	print "="*40
	if len(sys.argv)<2:
		while not operation:
			operation=raw_input("Enter type of insertion (artist,cd,cd-artist): ")
	else:
		operation=sys.argv[1]

	if operation not in valid:
		print "Invalid operation."
		sys.exit(1)
	
	if operation=='artist':
		while not name or not country:
			name=raw_input("Artist name: ")
			country=raw_input("Artist country:")

		query='select * from artist where name like "%'+name+'%"'
	
		ret=select_exec(query,operation)
		if ret=='2' or ret=='1':
			query="insert into artist(name,country) values ('"+name+"','"+country+"')"
			insert_exec(query)
			print "Insertion (artist) completed."

	elif operation=='cd':
		confirm=''
		while not artist or not title or not year or not type_ or not art or not genres or not rate:
			artist=raw_input("Artist CD: ")
			title=raw_input("CD title: ")
			year=raw_input("CD year: ")
			type_=raw_input("CD type: ")
			art=raw_input("CD art link: ")
			genres=raw_input("CD genres: ")
			rate=raw_input("CD rate: ")

		query='select * from artist where name like "%'+artist+'%"'
	
		ret=select_exec(query,operation)
		if ret=='1':
			query="insert into cd(title,year,type,art,genres,rate) values ('"+title+"',"+year+",'"+type_+"','"+art+"','"+genres+"',"+rate+")"
			insert_exec(query)
			print "Insertion (cd) completed."

			while not confirm:
				art_id=get_artist_id(artist)
				confirm=raw_input("Now I'll link "+artist+"("+str(art_id)+") with last cd entry ("+title+").\nContinue? Y/n\n")
				if confirm=='Y' or confirm=='y':		
					query="insert into cd_artist values ("+str(art_id)+",(SELECT id FROM cd ORDER BY id DESC LIMIT 1))"
					insert_exec(query)
					print "cd-artist insert completed."
				elif confirm=='n' or confirm=='N':
					print "cd-artist link abandoned."

		if ret=='2':
			while not country:
				country=raw_input("Specify country for "+str(artist)+": ")

			query="insert into artist(name,country) values ('"+artist+"','"+country+"')"
			insert_exec(query)

			query="insert into cd(title,year,type,art,genres,rate) values ('"+title+"',"+year+",'"+type_+"','"+art+"','"+genres+"',"+rate+")"
			insert_exec(query)

			print "Insertion (artist+cd) completed."
			
			while not confirm:
				confirm=raw_input("Now I'll link last artist entry ("+artist+") with last cd entry ("+title+").\nContinue? Y/n\n")
				if confirm=='Y' or confirm=='y':
					query="insert into cd_artist values ((SELECT id FROM artist ORDER BY id DESC LIMIT 1),(SELECT id FROM cd ORDER BY id DESC LIMIT 1))"
					insert_exec(query)
					print "cd-artist insert completed."
				elif confirm=='n' or confirm=='N':
					print "cd-artist link abandoned."

	elif operation=='cd-artist':
		print "Seems like it's deprecated. Use artist or cd insertions."

except Exception as e:
	print e
	sys.exit(1)
