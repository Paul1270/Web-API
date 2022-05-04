from requests import *
from json import *
import unittest

def error(url, research):
    s = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN"><html><head><title>Error: 404 Not Found</title><style type="text/css">html {background-color: #eee; font-family: sans-serif;}body {background-color: #fff; border: 1px solid #ddd;padding: 15px; margin: 15px;}pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}</style></head><body<h1>Error: 404 Not Found</h1><p>Sorry, the requested URL <tt>&#039;'
    s+=url
    s+= ';</tt>caused an error:</p><pre>Not found: &#039;'
    s+=research
    s+= '&#039;</pre></body></html>'
    return s

class TestAPIMethods(unittest.TestCase):
    server_ip = "127.0.0.1"
    server_port = 8080


    def test_1_authors(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/mj")
        data = str(r1)
        l = "<Response [404]>"
        self.assertEqual(data,l)
    
    def test_2_authors(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/")
        data = str(r1)
        l = "<Response [404]>"
        self.assertEqual(data,l)
                  
        
    def test_1_coauthors(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/notfound/coauthors")
        data = r1.text
        l = "no co_auteurs"
        self.assertEqual(data,l)


    def test_1_search_authors(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/alex")
        data =r1.text
        cpt=0
        for l in range (len(data)):
            if(data[l:l+8]=="<author>"):
                cpt+=1
        self.assertEqual(cpt,100)

    def test_2_search_authors(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Chistos")
        data = r1.text
        l = "no author found"
        self.assertEqual(data,l)


    def test_3_search_authors(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Pauline?start=50")
        data = str(r1)
        l = "<Response [404]>"
        self.assertEqual(data,l)


    def test_1_error(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/")
        data1 = str(r1)
        r2 = get(f"http://{self.server_ip}:{self.server_port}/publications/mj")
        data2 = str(r2)
        self.assertEqual(data1,data2)

    def test_2_error(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/smsmsms")
        data1 = str(r1)
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/smsmsms")
        data2 = str(r2)
        r3 = get(f"http://{self.server_ip}:{self.server_port}/authors/Ming%20Shan/distance/Peter%20Rasche")
        data3 = str(r3)
        self.assertEqual(data1,data2)
        self.assertEqual(data1,data3)

if __name__ == '__main__':
    unittest.main()