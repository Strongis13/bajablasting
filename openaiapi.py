import openai
import os
class OpenAI:
  context_prompt = "Respond with a possible fix or cause for the following errors"
  context = []
  max_generation = 500
  model_lookup = {0: "text-davinci-003", 1: "ada", 2: "davinci"}
  model = 0
  def __init__(self):
    keyfile = open(os.path.join(os.path.dirname(__file__), "key.txt"), "r")
    openai.api_key = keyfile.read()

  def resetContext(self):
    self.context = [{"role": "system", "content": self.context_prompt}]

  def analyze(self, incident_prompt):
    self.resetContext()
    try:
      self.context.append({"role":"user", "content": incident_prompt})
      output = openai.Completion.create(
        model=self.model_lookup[self.model],
        prompt= self.context_prompt + incident_prompt,
        max_tokens= self.max_generation #max tokens to generate
      )
      self.context.append({"role":"assistant", "content": output.choices[0].text})
    except:
      output = "Error in settings"
    return output
  
  def configGenerate(self, config_prompt):
    try:
      prompt_file = open(os.getcwd() + "/prompts/Cisco-Config-Generation.txt")
      context_prompt = prompt_file.readline()
      output = openai.Completion.create(
        model=self.model_lookup[self.model],
        prompt= context_prompt + "\n" + config_prompt,
        max_tokens= self.max_generation, #max tokens to generate
        temperature= 0 #randomness, between 0 and 2, higher values will make output more random
      )
    except:
      output = "Error in settings"
    return output
  def chatGenerate(self, message):
    self.context.append({"role":"user", "content": message})
    output = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=self.context
    )
    self.context.append(output.choices[0]["message"])
    print(output)
    return output.choices[0]["message"]["content"]