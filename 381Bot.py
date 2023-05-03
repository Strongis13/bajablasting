### teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
### Utilities Libraries
import useful_skills as useful
import openaiapi as openapi
import os

# RESTCONF Setup
port = '443'
headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}

# Bot Details
bot_email = 'bajablast@webex.bot'
teamskey = open(os.path.join(os.path.dirname(__file__), "teamskey.txt"), "r")
teams_token = teamskey.read()
bot_url = "https://c5f9-144-13-254-51.ngrok.io"
bot_app_name = 'Baja Blasting Network Auto Chat Bot'

# Create a Bot Object
#   Note: debug mode prints out more details about processing to terminal
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},],
)

# Create a function to respond to messages that lack any specific command
# The greeting will be friendly and suggest how folks can get started.
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I'm a friendly CSR1100v assistant .  ".format(
        sender.firstName
    )
    response.markdown += "\n\nSee what I can do by asking for **/help**."
    return response

def listen_int_ips(incoming_msg):
    response = Response()
    try:
        routers = useful.m.get_list_from_file('routers.txt')
    except:
        routers = []
    #select target routers
    target = bot.extract_message("show int", incoming_msg.text).strip()

    if target == 'all':
        try:
            #loop through all
            for i in range(len(routers)):
                #
                get_int_ips(incoming_msg,routers[i])
        
        except:
            response.markdown = 'An error has occured on at least one device! Check the connection and try again.'
    else:
        try:
            target = int(target)
            if (target > 0) and (target <= len(routers)):
                #run with specific router
                try:
                    return get_int_ips(incoming_msg,routers[target-1])
                except:
                    response.markdown = 'An error has occured! Check the connection and try again.'
    
            else:
                #error, not valid input
                return list_available_routers(routers)

        except:
            #non-number input
            return list_available_routers(routers)

    return response

def get_int_ips(incoming_msg,router):
    device_name = router.get("ip")
    device_username = router.get("username")
    device_password = router.get("password")
    url_base = "https://{h}/restconf".format(h=device_name)

    response = Response()
    intf_list = useful.get_configured_interfaces(url_base, headers,device_username,device_password)

    if len(intf_list) == 0:
        response.markdown = "I don't have any information of this device"
    else:
        response.markdown = "Here is the list of interfaces with IPs I know for device **{name}**: \n\n".format(name=device_name)
    for intf in intf_list:
        response.markdown +="*Name:{}\n" .format(intf["name"])
        try:
            response.markdown +="IP Address:{}\{}\n".format(intf["ietf-ip:ipv4"]["address"][0]["ip"],
                                intf["ietf-ip:ipv4"]["address"][0]["netmask"])
        except KeyError:
            response.markdown +="IP Address: UNCONFIGURED\n"
    return response

def listen_conf(incoming_msg):
    response = Response()
    try:
        routers = useful.m.get_list_from_file('routers.txt')
    except:
        routers = []
    #select target routers
    target = bot.extract_message("applyconf", incoming_msg.text).strip()
    
    if target == 'all':
        try:
            #loop through all
            for i in range(len(routers)):
                useful.apply_custom_config(routers[i])
        
            response.markdown = 'Configuration has been applied to all devices.'
        except:
            response.markdown = 'An error has occured on at least one device! Check the connection and try again.'
    else:
        try:
            target = int(target)
            if (target > 0) and (target <= len(routers)):
                #run with specific router
                try:
                    useful.apply_custom_config(routers[target-1])
                    response.markdown = 'Configuration has been applied to the device.'
                except:
                    response.markdown = 'An error has occured! Check the connection and try again.'
    
            else:
                #error, not valid input
                return list_available_routers(routers)

        except:
            #non-number input
            return list_available_routers(routers)


    #convert .txt format to restconf format
    return response

def list_available_routers(routers):
    reply = Response()
    reply.markdown = "The selected option was invalid."
    reply.markdown += "\n\nAvailable selections are:\n"
    if len(routers) >= 1:
        for i in range(len(routers)):
            reply.markdown += "**[{i}]** - {hostname}\n".format(i=i+1,hostname=routers[i].get("ip"))
        reply.markdown += "**[all]** - All devices in list"
    else:
        reply.markdown += "*No devices found! Verify data in routers.txt file!*"

    return reply

def save_config(incoming_msg):
    response = Response()
    os.system("ansible-playbook backup_cisco_router_playbook.yaml -i hosts")
    response.markdown = "Router's running-config has been saved to the backups directory on host machine!"

    return response

def gptconf(incoming_msg):
    response = Response()
    prompt = bot.extract_message("ciscogpt", incoming_msg.text).strip()
    #new ai instance
    ai = openapi.OpenAI()
    ai.context_prompt = "Generate the following config in cisco ios code, without any comments or details, and do not add any notes to your response. It should only contain code."
    #make request
    reply = ai.analyze(prompt)
    
    #save reply to file
    file = open(os.getcwd() + "/cmd.txt", "w+")
    file.write(reply.choices[0].text)
    file.close()

    response.markdown = "Response from OpenAI has been saved to cmd.txt!\nOpenAI Response:\n```"
    response.markdown += reply.choices[0].text
    response.markdown += "\n```\nTo apply this config, use the \"applyconf\" command."

    return response

def gpt(incoming_msg):
    response = Response()
    prompt = bot.extract_message("newgpt", incoming_msg.text).strip()
    print(prompt)
    file = open(os.getcwd() + "/gptoutput.txt", "w+")
    file.write(prompt)

    #new ai instance
    ai = openapi.OpenAI()
    ai.context_prompt = ""
    #make request
    reply = ai.analyze(prompt)

    response.markdown = "ChatGPT Response:\n"
    response.markdown += reply.choices[0].text
    response.markdown += "\n```"

    file.write(reply.choices[0].text)
    file.close()

    return response

def replygpt(incoming_msg):
    response = Response()
    prompt = bot.extract_message("replygpt", incoming_msg.text).strip()

    file = open(os.getcwd() + "/gptoutput.txt", "a+")

    #new ai instance
    ai = openapi.OpenAI()
    ai.context_prompt = file.read()
    file.write(prompt)
    #make request
    reply = ai.analyze(prompt)

    response.markdown = "ChatGPT Response:\n```"
    response.markdown += reply.choices[0].text

    response.markdown += "\n```"
    file.write(reply.choices[0].text)

    return response

# Set the bot greeting.
bot.set_greeting(greeting)

# Add Bot's Commmands
bot.add_command("show int", "List all interfaces and their IP addresses", listen_int_ips)
bot.add_command("applyconf", "Apply arbitrary configuration from file", listen_conf)
bot.add_command("backup", "Backs up the running config of a device and saves it to a file", save_config)
bot.add_command("ciscogpt", "Request Cisco configuration from OpenAI's GPT-3 model", gptconf)
bot.add_command("newgpt", "Start new conversation with OpenAI's GPT model", gpt)
bot.add_command("replygpt", "Continue existing conversation with OpenAI's GPT model", replygpt)
# Every bot includes a default "/echo" command.  You can remove it, or any
bot.remove_command("/echo")

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)
