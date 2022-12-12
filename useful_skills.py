import os
import sys
import myparamiko as m
### For RESTCONF
import requests
import json
import routers

# Function to retrieve the list of interfaces on a device
def get_configured_interfaces(url_base,headers,username,password):
    url = url_base + "/data/ietf-interfaces:interfaces"

    # this statement performs a GET on the specified url
    response = requests.get(url,
                            auth=(username, password),
                            headers=headers,
                            verify=False
                            )
    return response.json()["ietf-interfaces:interfaces"]["interface"]

def apply_custom_config(router):
    #routers = m.get_list_from_file('routers.txt')

    #for router in routers:
    ssh_client = m.connect(**router)
    shell = m.get_shell(ssh_client)

    with open("cmd.txt") as file:
        for command in file:
            #print (command)
            m.send_command(shell, command.rstrip())
            m.time.sleep(0.1)

    m.close(ssh_client)


if __name__ == "__main__":
    import routers
    # Router Info 
    device_address = routers.router['host']
    device_username = routers.router['username']
    device_password = routers.router['password']
    # RESTCONF Setup
    port = '443'
    url_base = "https://{h}/restconf".format(h=device_address)
    headers = {'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json'}

    intf_list = get_configured_interfaces(url_base, headers,device_username,device_password)
    for intf in intf_list:
        print("Name:{}" .format(intf["name"]))
        try:
            print("IP Address:{}\{}\n".format(intf["ietf-ip:ipv4"]["address"][0]["ip"],
                                intf["ietf-ip:ipv4"]["address"][0]["netmask"]))
        except KeyError:
            print("IP Address: UNCONFIGURED\n")