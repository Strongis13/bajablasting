# bajablasting

                                                        Welcome to our Project!
We have built a Network Management Chatbot, which has the following configurations:

The bot is set up to read our list of routers `routers.txt` and prompt the user to select one of the routers from the list when running a given command. For example, if the user types the `show int` command without specifying a device, the bot will respond with:
`The selected option was invalid.

Available selections are:
[1] - x.x.x.x
[2] - x.x.x.x
[x] - x.x.x.x
[all] - All devices in list`
Where the list will expand to include all items in the list of `routers.txt`.

Using paramiko, we are able to apply an arbitrary list of commands to an individual or list of routers. The commands are entered in `cmd.txt`, with one command per line, then when the `applyconf` command is ran with an accompanying selector option (1, 2, all, etc) the commands specified in `cmd.txt` will be ran on the selected device(s).

Using restconf, we are able to retrieve the configured IP address of all interfaces on a specified device or list of devices. The `show int` chat command, when followed by an accompanying selector option (1, 2, all, etc), effectively retrieves the show ip int brief results for the selected device.

Using Ansible, we are able to backup the running configuration of a device and save it to a file for later use. The command `backup` will run the playbook for backing up the running config of the primary router.

The current issue (the monitor) is that due to the dynamic IP address that is applied to the company branch location changes every three hours. This breaks the VPN tunnel, and a network engineer is forced to manually input commands to get the tunnel back up and running. A script has been made that all you need to do is run it, and it reapplies the correct IP address for the branch router, reestablishing a connection to the company headquarters.

 
