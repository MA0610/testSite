import json
from flask import render_template
from models import db, Day, TimeSlot, ScheduledClass, Conflict

def handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Welcome to the Scheduling Website!"})
    }
