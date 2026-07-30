#load modules-------
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
import langchain_community
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np

#keys
#STEP3
TAVILY_API_KEY = "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"
GOOGLE_API_KEY = " AQ.Ab8RN6J4bQ3XriAiGANyx52sDu_e2pZYDqIPBDfdl6sLMOSI7w"
GROQ_API_KEY = "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"
print("done")

#
model =  ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)
response = model.invoke("hello buddy!")
response.content[-1]['text']

#

def search_latest_news_jobs(query):
  """this function helps to fetch latest
  news or jobs related article using
  tavily"""

  client = TavilyClient(
      api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response

  #agent creation
agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs])
agent

#
def main_agent(agent,query):
  """this is main agent or leader agent
  orchestrate sub agent"""

  #giving prompt to create detailed prompt
  #for code generation
  prompt = """you are AI assistant and
  below given is a prompt,your task is to give detailed prompt for
  this.
  You are a Professional Resume generator
  where user will give their personal info,
  you have to create detailed resume
  for students or professional one,
  it must be with dynamic UI and UX and,
  with advanced CSS professional designing
  give in rainbow colour
  make sure to give output in HTML format only
  no markdowns allowed
  """

  response =  agent.invoke({'messages':[{'role':'user',
                                         'content':prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']

  #save prompt using file handling

  with open('prompt.txt','w') as f:
    f.write(detailed_prompt)

  user_details = f"""below given is a user details
  generate resume based on that,if not
  given keep: default resume: Python Developer
  user details: {query}"""

  final_prompt = prompt + detailed_prompt + user_details
  #code generation
  response = agent.invoke({'messages':[{'role':'user',
                                      'content':final_prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code

  #
  code = main_agent(agent,"Sukhmani kaur,GenAI Expert")
from IPython import display as DISPLAY
DISPLAY.HTML(code)

#
#fetch latest domain related jobs using tavily

#fetch latest domain related jobs using tavily
def get_jobs(agent,
             Location = "Noida,Delhi",
             Profile = "Data Analysts, AI Engineer"):
  Location = "Noida,Delhi"
  Profile = "data analysts ,AI Engineer"
  prompt = f"""based on use given job profile,
  fetch latest jobs or job apply article
  using Naukri,Linkedin,Indeed,or all popular
  Job apply platforms,show results with JOB PROFILE NAME,LOCATION,SALARY,
  COMPANY NAME,SHOW jobs only related to given {Location} and {Profile}.
  Output must be in professional HTML Naukri theme cards with dynamic design,show atleast
  top 10-20 results with directly apply link"""
  response = agent.invoke({'messages':[{'role':'user',
                                          'content':prompt}]})

  code = response['messages'][-1].content[-1]['text']

  return code

  code = get_jobs(agent)
  DISPLAY.HTML(code)

