import json
from models import db, Day, TimeSlot, ScheduledClass

def handler(event, context):
    schedules_3d = [[[] for _ in range(20)] for _ in range(5)]  # Example data
    return {
        "statusCode": 200,
        "body": json.dumps(schedules_3d)
    }
