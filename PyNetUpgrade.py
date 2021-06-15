from netmiko import ConnectHandler
import pandas as pd
import getpass
from datetime import datetime

#Start overall time for script (shows time for all switches ran)
start_timeall = datetime.now()

#################################################################
#Finds switch firmware version and check suggested firmware
#If outdated push new firmware, and upgrade switch
#State current version and chassis type
#################################################################

def NetUpgrade():

    #Active inventory sheet for all switches
    df = pd.read_csv('inventory.csv')

    #choose site
    site = input("Enter site: ")

    #Choose layer 
    layer = input("Enter layer (L2/L3): ")

    #amends both site and layer (Title of each column)
    iplist = (site.lower()+layer.upper())

    #Gathers all switches from specific column
    x = (df[iplist])

    #Username and Password of for switch SSH connection
    usr = input("Enter Username: ")
    PassWD = getpass.getpass()

    for n in (x):
        try:
            if '10' in n:

                #Turn each IP into variable from inventory
                ip = n

                #Start time calculation for individual switch
                start_time = datetime.now()

                #Turn each switch into separte log
                log = ip + '.txt'

                #Connection handler into variable
                net_connect = ConnectHandler(device_type='hp_procurve', ip= ip, username= usr, password= PassWD, fast_cli=True, session_log = log)
            
                #Show commands that will be ran on switch (Prompt to find hostname)
                model = net_connect.send_command("show dhcp client vendor-specific | inc Vendor Class")
                version = net_connect.send_command("show flash | inc Primary Image")
                prompt = net_connect.find_prompt()

                if '2930M' in model:
                    modelID = ("Model: 2930M")
                    if 'WC.16.10.0011' in version:
                        versionID = ("Version: Updated")
                    else:
                        versionID = ("Executing Upgrade")
                        upgrade = ["copy tftp flash 10.2.32.139 WC_16_10_0011.swi primary", "y"]
                        reboot = ["reboot", "y"]
                        net_connect.save_config()
                        net_connect.send_config_set(upgrade)
                        net_connect.send_config_set(reboot)
                elif '3810M' in model:
                    modelID = ("Model: 38100M")
                    if 'KB.16.10.0011' in version:
                        versionID = ("Version: Updated")
                    else:
                        versionID = ("Executing Upgrade")
                        upgrade = ["copy tftp flash 10.2.32.139 KB_16_10_0011.swi primary", "y"]
                        reboot = ["reboot", "y"]
                        net_connect.save_config()
                        net_connect.send_config_set(upgrade)
                        net_connect.send_config_set(reboot)
                elif '2530' in model:
                    modelID = ("Model: 2530M")
                    versionID = ("Ignore")
                elif '2920' in model:
                    modelID = ("Model: 2920M")
                    versionID = ("Ignore")
                else:
                    modelID = ("Model Not Found")
                    versionID = ("Ignore")

                #End time for individual switch
                end_time = datetime.now()

                #Notifies user of completion
                hostname = prompt[:-1]
                print("\n")
                print("#" * 30)
                print (hostname + " " + "-" + " " + "Complete")
                print(modelID)
                print(versionID)
                print('Duration: {}'.format(end_time - start_time))
                print("#" * 30)
        
        #If there is an error go to next switch
        except TypeError:
            continue
        except:
            print("\n")
            print("#" * 30)
            print ('Failed to connect to ' + ip)
            print("#" * 30)

NetUpgrade()

#End overall time for script (shows time for all switches ran)
end_timeall = datetime.now()

#Prints overall time of script
print("\n")
print("#" * 30)
print ("Script" + " " + "Complete")
print('Duration: {}'.format(end_timeall - start_timeall))
print("#" * 30)