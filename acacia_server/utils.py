# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import random

import slack
from flask import flash

from acacia_server import settings

CLEANING_DUTIES = [
    "Clean mirrors with 41, clean counter and sinks with 49 in upstairs bathroom twice a week",
    "Sweep and mop floor and shower in downstairs bathroom twice a week",
    "vacuum couches and floor, pick up dirty dishes in rec room twice a week",
    "Vacuum and organize Library once a week",
    "Clean toilets and urinals inside and out in upstairs bathroom twice a week",
    "Collect, wash, dry kitchen rags twice a week",
    "Restock stalls with toilet paper, refill paper towels and soap, in downstairs bathroom once a week",
    "Clean counter with 49, Clean mirror with 41, take out trash in foyer/powder room once a week",
    "Clean mirrors with 41, clean counter and sinks with 49 in downstairs bathroom once a week",
    "Sweep and mop floor and shower in upstairs bathroom twice a week",
    "Restock stalls with toilet paper, refill paper towels and soap, in upstairs bathroom once a week",
    "take out trash, put new trashbag in trash can in downstairs bathroom three times a week",
    "Clean windows inside and out in library and on Main Deck once a week",
    "Sweep basketball court and pick up trash in the parking lot once a week",
    "Clean toilet inside and out, replace toilet paper and paper towels in powder room once a week",
    "sweep and mop main deck once a week",
    "Organize couches, pillows, remotes, blankets in rec room twice a week",
    "Dust off all pictures, around windows, and fan in dining room once a week",
    "Wipe down table with 49 in library twice a week",
    "Clean windows inside and out in dinning room and kitchen once a week",
    "Vacuum mail room once a week and take out trash by Pogo's room three times a week",
    "Vacuum furniture and carpet on main deck twice a week",
    "Organize shelves, clean out lint trays, pick up clothes on the floor in laundry room once a week",
    "Clean toilets and urinals inside and out in downstairs bathroom twice a week",
    "Vacuum floor and furniture and tidy up Purple & Gold room once a week",
    "Sweep and mop title and stairs with 48, take rugs out and shake them off, dust furniture in foyer/powder room once a week",
    "Vacuum upper hall once a week",
    "Vacuum Pogo's room with the Shark Vacuum once a week",
    "Vacuum lower hall once a week",
    "Sweep floor, clean shelves, washer, dryer, refrigerator, and freezer in laundry room once a week",
    "Clean windows inside and out in rec room once a week",
    "sweep and mop Dining room once a week",
    "Dust all furniture and pictures on main deck once a week",
    "take out trash, put new trashbag in trash can in upstairs bathroom three times a week",
    "Clean up trash around outside trash can once a week",
    "Sweep steps by kitchen door, Basketball court door once a week",
]


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def post_duties():
    '''
    Gives a cleaning duty to all members of the settings.CLEANING_DUTIES_CHANNEL
    :return:
    '''
    client = slack.WebClient(token=settings.SLACK_TOKEN)
    resp = client.channels_info(channel=settings.CLEANING_DUTIES_CHANNEL)
    members_id_list = resp.data['channel']['members']
    random.shuffle(CLEANING_DUTIES)

    duties_text_list = list(zip(members_id_list, CLEANING_DUTIES))
    duties_text = '\n'.join([f'<@{handle}> - {duty}' for handle, duty in duties_text_list])

    client.chat_postMessage(channel=settings.CLEANING_DUTIES_CHANNEL, **{'text': duties_text})


if __name__ == '__main__':
    post_duties()
