# in this project we're going to use regular expression and JSON format, so the relevant modules are included (re and "json" modules).
# Moreover in the code Abstract Syntax Trees (ast) has been called to change a string to a dictionary
# Finally to connect and run ios command the code employe netmiko module.
import re
import json
import ast
from netmiko import ConnectHandler
DeviceList=[] #for keeping the list of devices' ip address
AllDevices=dict() # all devices' information 

#This function is aimed to connect to devices and run "show cdp neighbor detail" command
#the result of the command will be returned in string format
def Connect(device_info):
    shell=ConnectHandler(**device_info) # connect via ssh protocol
    result=shell.send_command("show cdp neighbor detail") # send command to the device
    shell.disconnect() #close the ssh session
    return result # return the result of command

#This function is used to find the device id  and device ip address from the cdp result
def Convert_CDP_To_Dict(text):
    test=False
    strDevices=""
    for line in text:
        if(re.search("Device ID:",line)): # call search() method from regular expression class to find the device ID
           data=re.split("Device ID:",line) 
           DevID=data[1].strip("\n") #store the device ID in DevID variable
        elif(re.search("IP address:",line)): #call search() method from regular expression class to find the IP address of the device
             data=re.split("IP address:",line) 
             DevIP=data[1].strip("\n") #store the device's IP in DevIP variable
             test=True  # a check variable
        if(test and DevIP not in DeviceList):  #Check if this device has not already been met   
            strTemp='{"Name":"'+DevID+'",'
            strTemp+='"IP":"'+DevIP+'"},'             
            strDevices+=strTemp
            strTemp=""
            DeviceList.append(DevIP) #append the node IP into the end of the Not_Meet_Yet devices list
            test=False
    return strDevices #return the resault

def main(RootName,RootIP):
    #Add the root point information into the parse list
    myDict='{"Name":"'+RootName+'","IP":"'+RootIP+'"},'
    DeviceList=[RootIP]
    for device in DeviceList: 
        #make a dictionary of the connecting information 
        device_info={"device_type":"cisco_ios","host":device,"username":"admin","password":"linux"}
        #Call connect function
        cdp_info=Connect(device_info)
        #parse the return result by connect() function and extract the desired information form it
        myDict+=Convert_CDP_To_Dict(cdp_info)  
    
    #convert the string of information into a dictionary     
    myDict=myDict[:-1] #remove the last extra comma 
    myDict='{"Devices":['+myDict+']}' #assign a name to the main key
    AllDevices=ast.literal_eval(myDict) 
    
    #save the information of devices in a json file format
    with open("cdp1.txt","w") as fp: 
        json.dump(AllDevices,fp)
        fp.close()
    #Show all devices in json format  
    print(AllDevices)    
    
if __name__=="__main__": 
    main("CSR1000v","192.168.153.129") #Call the main function with root point device information
    #the root device is a point where the script starts to walk through the network




