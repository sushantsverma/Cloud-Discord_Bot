import json
import string
import random 
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import numpy as np

bobo = ChatBot(name='Bobo',
                logic_adapters = [
                    'chatterbot.logic.MathematicalEvaluation',
                    'chatterbot.logic.TimeLogicAdapter',
                    'chatterbot.logic.BestMatch'
                ])
trainer = ChatterBotCorpusTrainer(bobo)
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)
train_bot = ListTrainer(bobo)

train_bot.train([
    "Hi",
    "Hello",
    "How are you?",
    "I'm good, thanks for asking. How are you?",
    "I'm good too, thanks for asking!",
    "How is life?",
    "It's good, nothing much lately.",
    "Ohh, good to hear everything's alright."
])
while True:
    try:
        print(bobo.get_response(input("User: ")))
    except KeyboardInterrupt:
        break
