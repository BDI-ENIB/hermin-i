import Dolmen
import Config
import Graph
class Sensors():

    def __init__(self,name,nameX,nameY,nameZ,idSensor,idGraph,typeGraph,graph,label,color):
        self.name=name
        self.nameX=nameX
        self.nameY=nameY
        self.nameZ=nameZ
        self.idSensor=idSensor
        self.idGraph=idGraph
        self.processed=False
        self.typeGraph=typeGraph
        self.graph=graph

        #update graph sensor with label and color
        if self.typeGraph=="2d":
            if(label !=""): # if label
                self.graph.label.append(label)
            self.graph.color.append(color)
            self.graph.numberGraph+=1 # update number sensor in graph

        if self.typeGraph=="gps":
            if(label !=""): # if label
                self.graph.label.append(label)
            self.graph.color.append(color)
            self.graph.numberGraph+=1 # update number sensor in graph
            
        elif self.typeGraph=="3d":
            self.graph.marker=label
            self.graph.color=color       

    def decoding(self,line_split):

        for j in range(0,len(line_split)):  

            if self.typeGraph =="2d" : # if graph 2D

                if line_split[j]==str(self.idSensor) and line_split[j+1]==self.nameY: #if sensor is detected

                    if str(line_split[j+2]) !="": # if there are sensors's data
                        self.graph.y[self.idGraph].append(float(line_split[j+2])) # adding sensors's data in graph
                        if len(self.graph.y[self.idGraph])==len(self.graph.x)+1:
                            self.graph.y[self.idGraph].pop()
                            Config.Log.InfoSaveLog("warning",str('no time found ' + str(self.name) + "  " + str(self.idSensor)))
                            print("no time found " + str(self.name) + "  " + str(self.idSensor))

                    else : # if there are not sensors's data
                        Config.Log.InfoSaveLog("warning",str('no data in sensors ' + str(self.name) + str(self.idSensor)))
                        self.graph.y[self.idGraph].append(0) # adding 0 in y axe of sensor graph
                        print(' no data in sensors ' + str(self.name) + " " + str(self.idSensor))
                        if len(self.graph.y[self.idGraph])==len(self.graph.x)+1:
                            self.graph.y[self.idGraph].pop()
                            Config.Log.InfoSaveLog("warning",str('no time found ' + str(self.name) + " " + str(self.idSensor)))
                            print("no time found " + str(self.name) + "  " + str(self.idSensor))

                    self.processed = True # sensors data is processed

            elif self.typeGraph =="3d" : # if graph 3D   

                if line_split[j]==str(self.idSensor) and line_split[j+1]==self.nameX and line_split[j+3]==self.nameY and line_split[j+5]==self.nameZ: #if sensor is detected
                    
                    if str(line_split[j+2])!="" and str(line_split[j+4])!="" and str(line_split[j+6])!="": # if x, y, z sensors's data are not empty
                        # adding sensors's data in graph
                        self.graph.x.append(float(line_split[j+2]))
                        self.graph.y.append(float(line_split[j+4]))
                        self.graph.z.append(float(line_split[j+6]))

                    else: # if x or y or z sensors's data are empty
                        # adding 0 in graph  
                        Config.Log.InfoSaveLog("warning",str('no data in sensors ' + str(self.name) + str(self.idSensor)))
                        self.graph.x.append(0) # adding data 0 in x axe of sensor graph
                        self.graph.y.append(0) # adding data 0 in y axe of sensor graph
                        self.graph.z.append(0) # adding data 0 in z axe of sensor graph
                        print(' no data in sensors ' + str(self.name) + " " + str(self.idSensor))

                    self.processed = True # sensors data is processed

            elif self.typeGraph =="gps":

                if line_split[j]==str(self.idSensor) and line_split[j+1]==self.nameX and line_split[j+7]==self.nameY: #if sensor is detected

                    if str(line_split[j+2]) !="" and str(line_split[j+8]) !="": # if there are sensors's data
                        self.graph.x[self.idGraph].append(float(line_split[j+2])) # adding sensors's data in graph
                        self.graph.y[self.idGraph].append(float(line_split[j+8])) # adding sensors's data in graph

                    else : # if there are not sensors's data
                        Config.Log.InfoSaveLog("warning",str('no data in sensors ' + str(self.name) + str(self.idSensor)))
                        self.graph.x[self.idGraph].append(0) # adding data 0 in x axe of sensor graph
                        self.graph.y[self.idGraph].append(0) # adding data 0 in y axe of sensor graph
                        print(' no data in sensors ' + str(self.name) + " " + str(self.idSensor))

                    self.processed = True # sensors data is processed

    def verifing(self):

        if self.processed==False : # if sensor is not processed

            if self.typeGraph =="2d" : # if graph 2D:
                Config.Log.InfoSaveLog("warning",str('no sensors ' + str(self.name) + " " + str(self.idSensor)))
                print("no sensors " + str(self.name) + " " + str(self.idSensor))
                self.graph.y[self.idGraph].append(0) # adding data 0 in y axe of sensor graph
                if len(self.graph.y[self.idGraph])==len(self.graph.x)+1:
                        self.graph.y[self.idGraph].pop()
                        Config.Log.InfoSaveLog("warning",str('no time found ' + str(self.name) + " " + str(self.idSensor)))
                        print("no time found " + str(self.name) + " " + str(self.idSensor))
                
            elif self.typeGraph =="3d" : # if graph 3D
                Config.Log.InfoSaveLog("warning",str('no sensors ' + str(self.name) + " " + str(self.idSensor)))
                print("no sensors " + str(self.name) + " " + str(self.idSensor))
                self.graph.x.append(0) # adding data 0 in x axe of sensor graph
                self.graph.y.append(0) # adding data 0 in y axe of sensor graph
                self.graph.z.append(0) # adding data 0 in z axe of sensor graph
            
            elif self.typeGraph =="gps" : # if graph gps
                Config.Log.InfoSaveLog("warning",str('no sensors ' + str(self.name) + " " + str(self.idSensor)))
                print("no sensors " + str(self.name) + " " + str(self.idSensor))                
                self.graph.x[self.idGraph].append(0) # adding data 0 in x axe of sensor graph
                self.graph.y[self.idGraph].append(0) # adding data 0 in y axe of sensor graph
                
        else: # Reseting if sensors was processed
            self.processed =False
