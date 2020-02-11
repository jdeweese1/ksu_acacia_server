import httpx
from flask_restful import Resource, reqparse

from acacia_server import utils
from slack import WebClient
from acacia_server import settings
import json
from flask import request
import threading

user_ids_that_can_post_cleaning_duties = []  # TODO Add the Ids of the people that can post cleaning duties


class InfoBot(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('challenge')
        self.parser.add_argument('event')

    def post(self):
        args = self.parser.parse_args()

        event = json.loads(args['event'].replace("'", '"'))
        assert event['channel_type'] == 'im'

        if 'user' in event.keys():
            client = WebClient(token=settings.SLACK_TOKEN)
            message_text = '''ADD IMPORTANT LINKS HERE FOR YOUR ORGANIZATION'''
            print(args)
            print(request.headers)
            def target():
                return client.\
                    chat_postMessage(channel=event['channel'], text=message_text)
            t1 = threading.Thread(group=None, target=target)
            t1.start()
        return {'status': 'ok'}, 200, {'X-Slack-No-Retry': 1}


class CleaningDuties(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id')
        self.parser.add_argument('command')
        self.parser.add_argument('response_url')

    def post(self):
        args = self.parser.parse_args()
        user_id = args['user_id']
        response_url = args.get('response_url', None)
        resp_msg = ''
        rtn_val = ()

        try:

            if user_id in user_ids_that_can_post_cleaning_duties:
                utils.post_duties()
                resp_msg = 'duties posted'
                rtn_val = {'status': 'ok'}, 200
            else:
                rtn_val = {'status': 'bad', 'reason': 'you are not authorized to post cleaning duties'}
                resp_msg = 'you are not authorized'
        except:  # noqa E722
            rtn_val = {'status': 'bad', 'reason': 'could not post duties'}, 500
            resp_msg = 'an error occurred when posting'
        finally:
            data = {'text': resp_msg}
            if response_url:
                httpx.post(response_url, data=data, headers={'Content-type': 'application/json'})
            return rtn_val
