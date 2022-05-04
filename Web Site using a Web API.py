from bottle import route, request, run
from json import *
from requests import get

server_ip = "127.0.0.1"
server_port = 8080

@route("/author")
def auth():
	
	return '''
	 <form action="/author" method="post">
	 Search for an author that contains the sub-sequence : <input name="seq" type="text" /></br></br>
	 Apply an order : <input name="order" type="text" />
	 <input value="Submit" type="submit" />
	 </form> </br></br>
	 or</br></br>
	 <form action="/doauthor" method="post">
	 Search for the author : <input name="aut" type="text" />
	 <input value="Submit" type="submit" />
	 </form>
	 '''


@route("/author", method='POST')
def do_input():
	s = request.forms['seq']
	order=request.forms['order']
	r = get(f"http://{server_ip}:{server_port}/search/authors/{s}?order={order}")
	l = r.text
	return '''
	 <form action="/doauthor" method="post">
	 Search for the author : <input name="aut" type="text" />
	 <input value="Submit" type="submit" />
	 </form>
	 </br>
	 </br>
	 ''', l
	 
@route("/doauthor", method='POST')
def do_input():
	#liste complète des publications et des co-auteurs d'un auteur
	s = request.forms['aut']
	r = get(f"http://{server_ip}:{server_port}/authors/{s}/coauthors")
	r1= get(f"http://{server_ip}:{server_port}/authors/{s}/publications")
	l = r.text
	l1=r1.text
	return l, '''</br></br>''',l1

@route("/dist")
def input_dist():
	return '''
	 <form action="/dist" method="post">
	 Search for the first author that contains the sub-sequence : <input name="s1" type="text" /></br></br>
	 Search for the second author that contains the sub-sequence : <input name="s2" type="text" />
	 <input value="Submit" type="submit" />
	 </form></br></br>
	 or</br></br>
	 <form action="/doinputdist" method="post">
	 First author: <input name="s3" type="text" /></br></br>
	 Second author: <input name="s4" type="text" />
	 <input value="Submit" type="submit" />
	 </form>
	 '''
	

@route("/dist", method='POST')
def do_input_dist():
	s1 = request.forms['s1']
	s2 = request.forms['s2']
	r = get(f"http://{server_ip}:{server_port}/search/authors/{s1}")
	r1 = get(f"http://{server_ip}:{server_port}/search/authors/{s2}")
	l = r.text
	l1=r1.text
	return '''
	 <form action="/doinputdist" method="post">
	 First author: <input name="s3" type="text" /></br></br>
	 Second author: <input name="s4" type="text" />
	 <input value="Submit" type="submit" />
	 </form>
	 </br>
	 </br>
	 ''', l, '''</br></br>''', l1
	 
@route("/doinputdist", method='POST')
def do_input_dist():
	s1 = request.forms['s3']
	s2 = request.forms['s4']
	r = get(f"http://{server_ip}:{server_port}/authors/{s1}/distance/{s2}")
	l = r.text
	return l


run(host='localhost', port=8081)