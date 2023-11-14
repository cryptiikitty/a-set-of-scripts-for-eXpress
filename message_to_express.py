#!/usr/bin/python
# coding: utf-8
 
 
import hashlib
import hmac
import logging
 
import base64
import json
import requests
import datetime
import argparse
 
# Bot ID and URLs
bot_id = ''
bot_url = ''
secret = ""
sendto = ""
 
def parse_args():
    parser = argparse.ArgumentParser(description='Express bot')
    parser.add_argument('--p', type=str, help='path to picture')
    parser.add_argument('--t', type=str, help='message')
    args = parser.parse_args()
 
    return args
 
 
# Token
def get_token():
    token_url = '/api/v2/botx/bots/' + bot_id + '/token'
    h = hmac.new(secret.encode('utf-8'), bot_id.encode('utf-8'), hashlib.sha256)
    signature = base64.b16encode(h.digest())
    r = requests.get(bot_url + token_url, params={'signature': signature})
    return r.json()['result']
 
 
# API authorization
token = get_token()
if token:
    headers = {
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
    }
else:
    logging.info(datetime.datetime.now(), 'token not received', token)
 
# Message URL
msg_url = '/api/v3/botx/notification/callback/direct'
 
 
# Main function for sending messages to chat
def send_express(message):

    msg = message
    data = {
        "group_chat_id": sendto,
        "notification": {
            "status": "ok",
            "body": msg,
 
        }
    }
    try:
        requests.post(bot_url + msg_url, headers=headers, data=json.dumps(data))
    except Exception as ex:
        logging.info(repr(ex))
 
 
 
 
if __name__ == '__main__':
 
    args = parse_args()
    args.t = 'hi'
    if args.t:
        message = args.t
        send_express(message)
