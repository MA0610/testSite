import json
from models import db, Conflict

def handler(event, context):
    data = json.loads(event['body'])
    class_id = data.get('class_id')
    conflict_class_id = data.get('conflict_class_id')

    conflict = Conflict.query.filter_by(class_id=class_id, conflict_class_id=conflict_class_id).first()
    if conflict:
        db.session.delete(conflict)
        db.session.commit()
        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "message": "Conflict removed successfully."})
        }

    return {
        "statusCode": 404,
        "body": json.dumps({"success": False, "message": "Conflict not found."})
    }
