# bajablasting

                                                        Welcome to our Project!
We have built a Network Management Chatbot, which has the following configurations:

The bot is set up where we have our list of routers (routers.txt) and whenever the user types a command for the bot it asks which router from the list, they would like to run the command for (with an option to select all of them). The paramiko skill will be applying ospf configs, restconf will be retrieving show ip route from whatever router is chosen.

At least 1 Ansible skill.

The current issue (the monitor) is that due to the dynamic IP address that is applied to the company branch location changes every three hours. This breaks the VPN tunnel, and a network engineer is forced to manually input commands to get the tunnel back up and running. A script has been made that all you need to do is run it, and it reapplies the correct IP address for the branch router, reestablishing a connection to the company headquarters.

 
