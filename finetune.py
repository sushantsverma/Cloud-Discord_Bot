import requests
import openai
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()
openai.organization = os.getenv('ORG')
openai.api_key = os.getenv('API-KEY')
open_ai_api_key = "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"


def file_upload(filename, purpose='fine-tune'):
    resp = openai.File.create(purpose=purpose, file=open(filename))
    pprint(resp)
    return resp


def file_list():
    resp = openai.File.list()
    pprint(resp)



def finetune_model(fileid, suffix, model='davinci'):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    payload = {'training_file': fileid, 'model': model, 'suffix': suffix}
    resp = requests.request(method='POST', url='https://api.openai.com/v1/fine-tunes', json=payload, headers=header, timeout=45)
    pprint(resp.json())


def finetune_list():
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes', headers=header, timeout=45)
    pprint(resp.json())


def finetune_events(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s/events' % ftid, headers=header, timeout=45)    
    pprint(resp.json())


def finetune_get(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s' % ftid, headers=header, timeout=45)    
    pprint(resp.json())



resp = file_upload('eve.jsonl')
finetune_model(resp['id'], 'Companion_Model', 'davinci')
finetune_list()