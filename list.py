import json
import os
import random
import requests
import argparse

from dotenv import load_dotenv

load_dotenv()

def printStandupList(dryRun):
    standup_list = os.getenv("STANDUP_LIST").split(',')

    random.shuffle(standup_list)

    nice_list = '\n'.join(standup_list)

    standup_order = '*Todays Standup Order* \n {}'.format(nice_list)

    webhook_url = os.getenv('WEBHOOK_URL')
    meets_url = os.getenv('MEETS_URL')

    postBody = json.dumps({
            "text": ":star: Gooood morning! Time for our daily standup! :star:",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":star: Gooood morning! Time for our daily standup! :star:"
                    }
                },
                {
                    "type": "section",
                    "block_id": "section567",
                    "text": {
                        "type": "mrkdwn",
                        "text": "<{}|Google Meets>".format(meets_url)
                    }
                },
                {
                    "type": "section",
                    "block_id": "section789",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "{}".format(standup_order)
                        }
                    ]
                }
            ]
        })
    if (dryRun == True):
       print(postBody)
    else:
        requests.post(webhook_url,
            headers={"Content-Type": "application/json"},
            data = postBody)
        

def runScript():
    parser = argparse.ArgumentParser(description='Python Slack Standup List Generator.')

    run_option = parser.add_mutually_exclusive_group()
    run_option.add_argument('--dryRun', action='store_true', help='If set, this will prevent the script from posting to slack')

    args = vars(parser.parse_args())

    dryRun = args['dryRun']
    
    printStandupList(dryRun)

runScript()