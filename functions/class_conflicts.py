import json
from models import db, ScheduledClass, Conflict
from sqlalchemy import or_

def handler(event, context):
    all_classes = ScheduledClass.query.all()
    conflicts = Conflict.query.all()

    conflict_pairs = set()
    for conflict in conflicts:
        class_1 = ScheduledClass.query.get(conflict.class_id)
        class_2 = ScheduledClass.query.get(conflict.conflict_class_id)
        if class_1 and class_2:
            conflict_pairs.add((class_1.name, class_2.name))

    detailed_classes = []
    for scheduled_class in all_classes:
        time_slot = TimeSlot.query.get(scheduled_class.time_slot_id)
        day = Day.query.get(time_slot.day_id) if time_slot else None
        detailed_classes.append({
            "id": scheduled_class.id,
            "name": scheduled_class.name,
            "professor_name": scheduled_class.professor_name,
            "class_section": scheduled_class.class_section,
            "time_slot": time_slot.time if time_slot else "Unknown",
            "day": day.name if day else "Unknown"
        })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "all_classes": detailed_classes,
            "conflict_pairs": list(conflict_pairs)
        })
    }
