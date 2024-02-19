from bs4 import BeautifulSoup

def class_empty(in_class):
	return (in_class == "") or (in_class == "bg_rot_20") or  (in_class == "bg_gelb_20")

f = open("leistungsdetails.html", "r")
parsed_content = BeautifulSoup(f, 'html.parser')

for tr in parsed_content.find_all('tr',class_=class_empty):
	print("----new match----")
	current = tr.td
	temp = current.a["href"]
	comp = temp[1:temp[1:].find('/')+1]
	#competition
	print("competition: "+comp)
	current = current.find_next('td')
	#date
	print("date: "+str(current.string))
	current = current.find_next('td')
	#Location
	print("location: "+str(current.string))
	current = current.find_next('td')
	#own team
	temp = current.a["href"]
	own_team = temp[1:temp[1:].find('/')+1]
	print("own team: " + own_team)
	current = current.find_next('td', class_="zentriert no-border-rechts")
	#opponent team
	temp = current.a["href"]
	opponent_team = temp[1:temp[1:].find('/')+1]
	print("opponent team: " + opponent_team)
	current = current.find_next('td')
	current = current.find_next('td')
	print("match id: " + current.a["id"])
	current = current.find_next('span')
	#result
	print("result: " + str(current.string))
	current = current.find_next('td')
	if "colspan" in current.attrs.keys():
		#status 
		if current.span:
			print("status: " + str(current.span["title"]))
		else:
			print("status: " + str(current.string))
	else:
		#position
		print("position: " + str(current.a.string))
