# Test generating stamps


# def generate_stamps(seconds):
#     """Creating stamps"""
#
#     hours, seconds = divmod(seconds, 3600)
#     minutes, seconds = divmod(seconds, 60)
#
#     if hours > 0:
#         return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
#     else:
#         return f"{int(minutes):02d}:{int(seconds):02d}"
#
#
# print(generate_stamps(3600))

import environ
import google.generativeai as genai
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown




# from openai import OpenAI
# import os
# import environ
#
# env = environ.Env()
# environ.Env.read_env()
#
# client = OpenAI(
#     api_key=env("OPENAI_API_KEY")
# )
#
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )
#
#
# print(completion.choices[0].message)
