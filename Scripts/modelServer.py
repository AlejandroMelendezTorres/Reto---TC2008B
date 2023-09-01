# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python server to interact with Unity
# Sergio. Julio 2021

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

import numpy as np
from agents import Cross

# Size of the board:
widht = 24
height = 24  
tiempo = 0.5

tl = [(12,10),(10,11),(11,13),(13,12)]
model = Cross(widht, height, tl)
    
contador = 0
while (contador < 200):
    model.step()
    contador += 1

AgentsDF= model.datacollector.get_agent_vars_dataframe()
    #print(positions.loc[1])#get everything from one step
    #print(positions.loc[1]["Position"].tolist())#get a list of all positions in one step

positions=[]

for i in range (1,201):
    tempPos=[] 
    pos=AgentsDF.loc[i]["Position"].tolist()
    type=AgentsDF.loc[i]["Type"].tolist()
    state=AgentsDF.loc[i]["State"].tolist()
    for j in range(len(pos)):
        x,y=pos[j]
        if type[j]=="Car":
            tempPos.append((float(x),float(y),0.0,0,5))
        elif type[j]=="TrafficLight":
            if state[j]==0:
                tempPos.append((float(x),float(y),0.0,1,0))
            elif state[j]==1:
                tempPos.append((float(x),float(y),0.0,1,1))
            elif state[j]==2:
                tempPos.append((float(x),float(y),0.0,1,2))
        elif type[j]=="lightsController":
            tempPos.append((float(x),float(y),0.0,2,5))
    positions.append(tempPos)


def positionsToJSON(ps,step):
    posDICT = []
    for p in ps[step]:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2],
            "type" : p[3], # 0 = car, 1 = traffic light, 2 = controller
            "color" : p[4] # 0 = red, 1 = yellow, 2 = green

        }
        posDICT.append(pos)
    return json.dumps(posDICT)
step=1

class Server(BaseHTTPRequestHandler):

    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        global step
        content_length = int(self.headers['Content-Length'])
        #post_data = self.rfile.read(content_length)
        post_data = json.loads(self.rfile.read(content_length))
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     #str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))
        
        '''
        x = post_data['x'] * 2
        y = post_data['y'] * 2
        z = post_data['z'] * 2
        
        position = {
            "x" : x,
            "y" : y,
            "z" : z
        }

        self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(str(position).encode('utf-8'))
        '''
        
        step+=1
        self._set_response()
        resp = "{\"data\":" + positionsToJSON(positions,step) + "}"
        #print(resp)
        self.wfile.write(resp.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
