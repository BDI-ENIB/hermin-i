import Windows
import Widgets
import Graph
import os.path
import Config
import Sensors
import csv
import time
import shutil
import Error
import os

count=0 # current line in CSV
state_communication=False #if True => start decoding

def currentTime(): # return the current time
    return str(time.strftime('%H.' '%M.' '%S'))

def currentDate():
    return str(time.strftime('%Y_' '%m_' '%d_'))

def decodingCSV(): #open and decoding CSV file
    global count
    filename = open(Config.CSV, 'r', encoding='latin1')          
    reader = csv.reader(filename, delimiter=';') #import csv
    
    lines = [line for line in reader] #import list of CSV lines
    filename.close()
    # add and find the CSV line to decode
    if lines==[[]] and count==0:
        return

    if lines !=[]:       
            
        if lines[count]!=['stop']:     
            #find time
            for j in range(0,len(lines[count])-1):            
                        
                if str(lines[count][j])=='0' and str(lines[count][j+1])=='time (s)': # time sensor detected    
                    
                    if str(lines[count][j+2])!="": # if time data not empty
                        print(str(float(lines[count][j+2])))
                        for sensor in Config.sensors_list_set_time:
                            sensor.x.append(float(lines[count][j+2]))
            
            #decoding current line 
            for sensor in Config.sensors:
                    sensor.decoding(lines[count])

            #verifing if all sensors has been treated
            for sensor in Config.sensors:
                    sensor.verifing()   
                
            #update line        
            count+=1
        else:

            state_set_communication(Config.start_button,Config.stop_button,False,Config.currentMode,Config.frame,False)
    else :
        return

def fileExist(fileToTest): # detect if file in folder exist

    try:
        with open(fileToTest,'r',encoding='latin1') as filename:            
            return  True

    except: 
        Config.Log.InfoSaveLog("warning",str(fileToTest + "not exist"))       
        return False # return error file no found


def updateOffline(i,start_button,stop_button): # decoding csv and updating graph in Offline mode
    global state_communication
    print(i)
    #Widgets.TextToPrint(Config.fire__offline_interface,Dolmen.currentTime(),Config.colorFont,Config.colorText,3,4)
    if(state_communication==True and fileExist(Config.figure.file)==True): #if you click on the start button of fire_interface windows and csv name exist
        decodingCSV() # decoding csv
        if(state_communication==True and fileExist(Config.figure.file)==True): 
            for sensor in Config.sensors:
                sensor.graph.animate()# update graph   
    else :
        if fileExist(Config.figure.file)==False :
            Windows.messageShowwarning("Open Filename", "Corrupted CSV file or not found")
            Config.Log.InfoSaveLog("info",'Corrupted CSV file or not found')
    

def updateOnline(i,start_button,stop_button): # decoding csv and updating graph in Online mode
    global state_communication
    if(state_communication==True ): #if you click on the start button of fire_interface windows and csv name exist
        decodingCSV() # decoding csv
        
        for sensor in Config.sensors:
            sensor.graph.animate()# update graph          
    else :

        if fileExist(Config.figure.file)==False :

            Windows.messageShowwarning("Open Filename", "Corrupted CSV file or not found")
            Config.Log.InfoSaveLog("info",'Corrupted CSV file or not found')
    
                           
def initFigure(): #init and reset figure
    global count,state_communication

    state_communication = False
    count=0
    os.remove(Config.CSV)
    filename = open(Config.CSV, 'w')
    filename.close()

    for sensor in Config.sensors:
        sensor.graph.initGraph()
                
def report_Function(): #report generation
    global state_communication

    if (state_communication == False): # if decoding is stopped

        #check if is save folder exist       
        if not os.path.exists(Config.SAVE_REPORT_FOLDER):
            Config.Log.InfoSaveLog("error",str(Config.SAVE_REPORT_FOLDER + "folder not found => creation"))            
            os.makedirs(Config.SAVE_REPORT_FOLDER)

        if not os.path.exists(Config.SAVE_REPORT_FOLDER + '/'+ str(Config.NAME_SAVE_FOLDER)):
            Config.Log.InfoSaveLog("error",str(Config.NAME_SAVE_FOLDER + "folder not found => creation"))
            os.makedirs(Config.SAVE_REPORT_FOLDER + '/'+ str(Config.NAME_SAVE_FOLDER))

        #save report
        shutil.copy(Config.figure.file,Config.SAVE_REPORT_FOLDER + '/'+ str(Config.NAME_SAVE_FOLDER) + '/' ) #copy csv file in save report folder        
        Config.figure.saveFig(Config.SAVE_REPORT_FOLDER,Config.NAME_SAVE_FOLDER,Config.NAME_SAVE_FIGURE) #save figure in save report folder
        Windows.messageShowinfo("Report generation","Report generation successfully created.")

        #print and save in log
        Config.Log.InfoSaveLog("info",str("report generation in " + Config.SAVE_REPORT_FOLDER + "/" + Config.NAME_SAVE_FOLDER))
        print("report generation in   " + Config.SAVE_REPORT_FOLDER + "/" + Config.NAME_SAVE_FOLDER)

    else : # if decoding is not stopped 
        #print and save in log 
        Windows.messageShowwarning("Report generation warning","Warning : please stop the data receive before to generate the report.")
        Config.Log.InfoSaveLog("info",str("trying to generate report before stopping decoding"))


def state_set_communication(start_button,stop_button,state,currentMode,frame,mode): # mode => true :ask to and start stop decoding, False : start and stop with no ask 
    global state_communication
    
    #if the user click on the start button
    if(state==True):
        #initFigure()
        #enable decoding
        state_communication=True
        Config.Log.InfoSaveLog("info",'start decoding') 

        #communication with cpp
        config=open(Config.CONFIG_TXT, "w")
        config.write("true")
        config.write("\n")
        config.write(str(currentMode))
        config.write("\n")
        config.write(frame)
        config.close()  

        #set button start ans stop state
        #disable start button
        start_button.disable()
        #enable stop button
        stop_button.enable()      

    elif(state==False):

        #check if ask stop decoding
        if mode== True:
            if (Windows.messageAskyesno("End of data receive", "Do you want to stop the data receive ?")):
                Config.Log.InfoSaveLog("info",'stop decoding')
                start_button.enable()
                #disable stop button
                stop_button.disable()

        #disable decoding
        state_communication=False

        #communication with cpp
        config=open(Config.CONFIG_TXT, "w")
        config.write("false")
        config.write("\n")
        config.write(str(currentMode))

        if mode==False :
            print("end CSV file")
            Config.Log.InfoSaveLog("info",'end CSV file')

            #disable start button
            start_button.disable()
            #disable stop button
            stop_button.disable()

            Windows.messageShowinfo("","End CSV file")
        
def add_sensor_save_Function(add_sensor_interface,sensor_add_name):
    
    save_condition = True

    if(sensor_add_name.getEntry()==""):
        Config.Log.InfoSaveLog("warning",'add new sensor : no name given')
        Windows.messageShowerror("Name error","Please enter the sensor's name")
        save_condition=False

    #check that the sensor does not already exist
    if(os.path.isfile(sensor_add_name.getEntry().lower() + ".hpp") or os.path.isfile(sensor_add_name.getEntry().lower() + ".cpp")):
        Config.Log.InfoSaveLog("warning",str('sensor name ' + sensor_add_name.getEntry().lower() +' already exit'))
        Windows.messageShowerror("Name error",sensor_add_name.getEntry().lower() + " sensor already exist. Please change the sensor's name")
        save_condition=False
    
    
    #if no error, create the hpp and the cpp    
    if(save_condition==True):
        # Creation of sensor.hpp
        hpp = open(sensor_add_name.getEntry().lower() + ".hpp", "x")            
        hpp.write("#ifndef DOLMEN_"+ sensor_add_name.getEntry().upper() +"_HPP")
        hpp.write("\n#define DOLMEN_" + sensor_add_name.getEntry().upper() +"_HPP 1")
        hpp.write("\n#include <string>")
        hpp.write("""\nnamespace dolmen
{
""")
        hpp.write("\n   class " + sensor_add_name.getEntry().capitalize())
        hpp.write(""": public Sensor \n  {
    public : """)                   
        hpp.write(sensor_add_name.getEntry().capitalize() + " (int id, std::string name);")
        hpp.write("""
            
    void decoding(const std::string data) override;

    std::string getColumnIdentifiers() override
    {
    """)
        hpp.write("      return "  + '"' + sensor_add_name.getEntry().capitalize() + '";')
        hpp.write("""
    }""")
        hpp.write("""
                
    int getNbAttr() override
    {
      return 1;
    }
  };
}

#endif""")            
        hpp.close()
        
        # Creation of sensor.cpp
        cpp = open(sensor_add_name.getEntry().lower() + ".cpp", "x")
        cpp.write('#include "' + sensor_add_name.getEntry().lower() + '.hpp"')
        cpp.write("""
            
namespace dolmen
{
""")
        cpp.write("  " + sensor_add_name.getEntry().capitalize() + "::" + sensor_add_name.getEntry().capitalize() + " (int id, std::string name):Sensor{id,name}{}")
        cpp.write("""
            
  void """ + sensor_add_name.getEntry().capitalize() +"""::decoding(const std::string data)
  {
    //insert here the decoding method of your sensor
  }
} /* dolmen */""")
        cpp.close()
        #print save in log and return
        Config.Log.InfoSaveLog("info",str(' sensor ' + str(sensor_add_name.getEntry()).lower() +"generated"))
        Windows.messageShowinfo("Sensor generation",sensor_add_name.getEntry().lower() + " sensor generation successfully created. Do not forget to complete the decoding function of this class")
        Config.sensors_management_Function(add_sensor_interface)


