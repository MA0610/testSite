import json
from models import db, Conflict, ScheduledClass
from sqlalchemy import or_

def handler(event, context):
    data = json.loads(event['body'])
    class_id = data.get('class_id')
    conflict_class_id = data.get('conflict_class_id')

    if not class_id or not conflict_class_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"success": False, "message": "Both class IDs are required."})
        }

    existing_conflict = Conflict.query.filter(
        or_(
            (Conflict.class_id == class_id) & (Conflict.conflict_class_id == conflict_class_id),
            (Conflict.class_id == conflict_class_id) & (Conflict.conflict_class_id == class_id)
        )
    ).first()

    if existing_conflict:
        return {
            "statusCode": 400,
            "body": json.dumps({"success": False, "message": "This conflict already exists."})
        }

    conflict = Conflict(class_id=class_id, conflict_class_id=conflict_class_id)
    db.session.add(conflict)
    db.session.commit()

    return {
        "statusCode": 200,
        "body": json.dumps({"success": True, "message": "Conflict marked successfully."})
    }
