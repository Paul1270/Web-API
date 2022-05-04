from lxml import etree as ET
from bottle import *
import re
import json
from collections import OrderedDict
import os
from pathlib import *

publications = ['</article>', '</inproceedings>', '</proceedings>', '</book>', '</incollection>', '</phdthesis>',
                '</mastersthesis>']
publications2 = ['<article', '<inproceedings', '<proceedings', '<book', '<incollection', '<phdthesis', '<mastersthesis']
end = ['</dblp>']
entete = ['<?xml version="1.0" encoding="ISO-8859-1"?>\n', '<!DOCTYPE dblp SYSTEM "dblp.dtd">\n', '<dblp>\n']
path1 = Path("dblp.xml")


def word_in(line, publi):
    for p in publi:
        for l in range(len(line) - len(p) + 1):
            if (line[l:l + len(p)] == p):
                return [True, len(p)]
    return [False, 0]


with open(path1, "r") as file:
    fin = False
    num = 0
    numerofolder = str(num)
    lignesuiv = ''
    while (fin == False):
        folder = "folder" + numerofolder
        path = Path(folder + ".xml")
        with open(path, "a") as folder1:
            cpt = 0
            folder1.write('<?xml version="1.0" encoding="ISO-8859-1"?>' + '\n')
            folder1.write('<!DOCTYPE dblp SYSTEM "dblp.dtd">' + '\n')
            folder1.write('<dblp>' + '\n')
            if (lignesuiv != ''):
                folder1.write(lignesuiv)
            while (cpt < 1000000):
                line = file.readline()
                print(line)
                if line not in entete:
                    word0 = word_in(line, end)
                    if (line == '</dblp>'):
                        folder1.write(line)
                        fin = True
                        break
                    if (word0[0] == True):
                        folder1.write(line[:len(line) - word0[1]])
                        folder1.write('\n</dblp>')
                        fin = True
                        break
                    word = word_in(line, publications)
                    word2 = word_in(line, publications2)
                    if (word[0] == True):
                        cpt += 1
                    if (cpt == 500000):
                        if (word2[0] == True):
                            folder1.write(line[0:word[1]])
                            folder1.write('\n</dblp>')
                            lignesuiv = line[word[1]:]
                        else:
                            folder1.write(line)
                            folder1.write('</dblp>')
                            break

                    else:
                        lignesuiv = ''
                        folder1.write(line)
            num += 1
            numerofolder = str(num)

    cpt1 = 0
    with open(path, "r") as folder2:
        while (True):
            line = folder2.readline()
            cpt1 += 1
            if line == '</dblp>':
                break
    print(cpt1, str(path))
    if cpt1 == 4:
        try:
            os.remove(path)
        except OSError as e:
            print(e)
        else:
            print("File is deleted successfully")

local_input = "folder1.xml"
p = ET.XMLParser(recover=True)
tree = ET.parse(local_input, parser=p)
root = tree.getroot()
print(f"XML File loaded and parsed, root is {root.tag}")


@route('/authors/<name>')
def info_auth(name):
    publications = []
    co_authors = []
    s = ''
    for child in root:
        for i in range(len(child)):
            if child[i].tag == "author":
                if child[i].text == name:
                    for j in range(len(child)):
                        if child[j].tag == "author":
                            if (child[j].text != name) and (child[j].text not in co_authors):
                                co_authors.append(child[j].text)
                        if child[j].tag == "title":
                            if child[j].text not in publications:
                                publications.append(child[j].text)
    if (len(publications) == 0 & len(co_authors) == 0):
        abort(404, "Not found: '/authors/" + name + "'")
        return 0
    s += "Name of the author : " + str(name) + "<br/><br/>"
    s += "Number of publications : " + str(len(publications)) + "<br/><br/>"
    for i in range(len(publications)):
        s += str(publications[i]) + "<br/>"

    s += "<br/>" + "number of coauthors : " + str(len(co_authors)) + "<br/><br/>"
    for i in range(len(co_authors)):
        s += co_authors[i] + "<br/>"
    return s


# http://localhost:8080/authors/Indira%20Nair


@route('/authors/<name>/publications')
def publi(name):
    limit = 100
    start = request.query.start
    count = request.query.count
    order = request.query.order
    if (start == ""):
        start = 0
    if (count != "") and (int(count) <= 100):
        limit = int(count)
    if (order == ""):
        order = 0
    s = ""
    cpt = 0
    publications = []
    dico_pour_ranger = {}
    if (order == 0):
        for child in root:
            for i in range(len(child)):
                if child[i].tag == "author":
                    if child[i].text == name:
                        for j in range(len(child)):
                            if child[j].tag == "title":
                                if child[j].text not in publications:
                                    publications.append(child[j].text)
    else:
        for child in root:
            for i in range(len(child)):
                if child[i].tag == "author":
                    if child[i].text == name:
                        for j in range(len(child)):
                            if child[j].tag == order:
                                for l in range(len(child)):
                                    if (child[l].tag == "title"):
                                        if child[j].text not in dico_pour_ranger:
                                            dico_pour_ranger[child[j].text] = child[l].text
    if (len(dico_pour_ranger) != 0):
        dico_range = OrderedDict(sorted(dico_pour_ranger.items(), key=lambda t: t[0]))
        for keys in dico_range:
            publications.append(dico_range[keys])
    if (len(publications) == 0 or len(publications) <= int(start)):
        abort(404, "Not found: '/authors/" + name + "/publications'")
        return 0
    s = "Publications of the author " + str(name) + " :<br/><br/>"
    for k in range(int(start), len(publications)):
        if (cpt < int(limit)):
            s += publications[k] + "<br/>"
            cpt += 1
    return s


# http://localhost:8080/authors/Indira%20Nair/publications


@route('/authors/<name>/coauthors')
def co_auth(name):
    limit = 100
    start = request.query.start
    count = request.query.count
    order = request.query.order
    if (start == ""):
        start = 0
    if (count != "") and (int(count) <= 100):
        limit = int(count)
    if (order == ""):
        order = 0
    s = ""
    cpt = 0
    co_authors = []
    dico_pour_ranger = {}
    if (order == 0):
        for child in root:
            for i in range(len(child)):
                if child[i].tag == "author":
                    if child[i].text == name:
                        for j in range(len(child)):
                            if child[j].tag == "author":
                                if (child[j].text != name) and (child[j].text not in co_authors):
                                    co_authors.append(child[j].text)
    else:
        for child in root:
            for i in range(len(child)):
                if child[i].tag == "author":
                    if child[i].text == name:
                        for j in range(len(child)):
                            if (child[j].tag == "author"):
                                if (child[j].text != name and child[j].text not in dico_pour_ranger):
                                    for l in range(len(child)):
                                        if child[l].tag == order:
                                            if order == "author":
                                                if (child[l].text == child[j].text):
                                                    dico_pour_ranger[child[j].text] = child[j].text
                                            else:
                                                dico_pour_ranger[child[j].text] = child[l].text
    if (len(dico_pour_ranger) != 0):
        dico_range = OrderedDict(sorted(dico_pour_ranger.items(), key=lambda t: t[1]))
        for keys in dico_range:
            co_authors.append(keys)
    if len(co_authors) == 0:
        return "coauthor not found"

    if (int(start) >= len(co_authors)):
        abort(404, "Not found: '/authors/" + name + "/coauthors'")
        return 0
    s = "Author's coauthor " + str(name) + " :<br/><br/>"
    for i in range(int(start), len(co_authors)):
        if (cpt < limit):
            s += co_authors[i] + "<br/>"
            cpt += 1
    return s


# http://localhost:8080/authors/Indira%20Nair/coauthors

def word_in(line, word):
    line = line.lower()
    word = word.lower()
    for l in range(len(line) - len(word) + 1):
        if (line[l:l + len(word)] == word):
            return True
    return False


@route('/search/authors/<searchString>')
def search_aut(searchString):
    limit = 100
    start = request.query.start
    count = request.query.count
    order = request.query.order
    if (start == ""):
        start = 0
    if (count != "") and (int(count) <= 100):
        limit = int(count)
    if (order == ""):
        order = 0
    s = ""
    cpt = 0
    authors = []
    dico_pour_ranger = {}
    if (order == 0):
        for child in root:
            for i in range(len(child)):
                if child[i].tag == "author":
                    if (word_in(str(child[i].text), str(searchString))) and (child[i].text not in authors):
                        authors.append(child[i].text)
    else:
        for child in root:
            for i in range(len(child)):
                if child[i].tag == "author":
                    if (word_in(str(child[i].text), str(searchString)) and child[i].text not in dico_pour_ranger):
                        for j in range(len(child)):
                            if child[j].tag == order:
                                if order == "author":
                                    if (child[j].text == child[i].text):
                                        dico_pour_ranger[child[i].text] = child[i].text
                                else:
                                    dico_pour_ranger[child[i].text] = child[j].text
    if (len(dico_pour_ranger) != 0):
        dico_range = OrderedDict(sorted(dico_pour_ranger.items(), key=lambda t: t[1]))
        for keys in dico_range:
            authors.append(keys)
    if len(authors) == 0:
        return "Authors not found"
    if (len(authors) <= int(start)):
        abort(404, "Not found: '/authors/" + searchString + "'")
        return 0
    s = "Authors containing chains of characters : " + str(searchString) + "<br/><br/>"
    for k in range(int(start), len(authors)):
        if (cpt < int(limit)):
            s += "<author>"
            s += authors[k] + "<br/>"
            s += "</author>"
            cpt += 1
    return s


# http://localhost:8080/search/authors/alex


def minimal(dic):
    mini_v = float("inf")
    mini_k = ''
    for cle, valeur in dic.items():
        if valeur[0] < mini_v:
            mini_v = valeur[0]
            mini_k = cle
    if (mini_v == float("inf")):
        return (mini_v, '')
    else:
        return (mini_v, dic[mini_k][1])


def distance(name_origin, name_destination, d, l, co_auth, cpt):
    l_copy = l.copy()
    l_copy.append(name_origin)
    co_auth_copy = co_auth.copy()
    co_authors = []
    # on récupère la liste des co-auteurs de name_origin
    for child in root:
        for i in range(len(child)):
            if child[i].tag == "author":
                if child[i].text == name_origin:
                    for j in range(len(child)):
                        if child[j].tag == "author":
                            if (child[j].text != name_origin) and (child[j].text not in co_authors) and (
                                    child[j].text not in l) and (child[j].text not in co_auth_copy) and (
                                    child[j].text not in d.keys()):
                                co_authors.append(child[j].text)
    co_auth_copy = co_authors
    if len(co_authors) == 0:
        return [float("inf"), ""]
    else:
        if (name_destination in co_authors) and (len(l) == 0):
            return [1, l_copy]
        else:
            if name_destination in co_authors:
                if len(l_copy) < cpt:
                    cpt = len(l_copy)
                return [1, l_copy]
            else:
                if (len(l_copy) < cpt):
                    if ((len(co_authors) > 1) and (name_origin not in d.keys())):
                        d[name_origin] = l_copy
                        dic = {}
                        for auth in co_authors:
                            dic[auth] = [1, ""]
                        for auth in co_authors:
                            res = distance(auth, name_destination, d, d[name_origin], co_auth_copy, cpt)
                            dic[auth][0] += res[0]
                            dic[auth][1] = res[1]
                        return minimal(dic)
                    else:
                        dic = {}
                        for auth in co_authors:
                            dic[auth] = [1, ""]
                        for auth in co_authors:
                            res = distance(auth, name_destination, d, l_copy, co_auth_copy, cpt)
                            dic[auth][0] += res[0]
                            dic[auth][1] = res[1]
                        return minimal(dic)
                else:
                    return [float("inf"), ""]


@route('/authors/<name_origin>/distance/<name_destination>')
def dist(name_origin, name_destination):
    distance_mini, chemin_mini = distance(name_origin, name_destination, {}, [], [], float("inf"))
    if distance_mini == float("inf"):
        return "No distance from the author " + str(name_origin) + " to the author " + str(name_destination) + "."
    else:
        return "the distance of the minimal road " + str(chemin_mini) + " between the author " + str(
            name_origin) + " and the author " + str(name_destination) + " is " + str(distance_mini) + "."


# http://localhost:8080/authors/Ming%20Shan/distance/Amos%20Darko (result : distance = 2)
# http://localhost:8080/authors/Ming%20Shan/distance/Peter%20Rasche (result : no result)


run(host='localhost', port=8080)