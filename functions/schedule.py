import json
from flask import request, jsonify
from models import db, Day, TimeSlot, ScheduledClass, Conflict
from sqlalchemy import or_

def handler(event, context):
    data = json.loads(event['body'])
    new_schedule = data.get('schedule')
    dayBlocks = data.get('set')
    timeBlock = data.get('time')
    profName = data.get('professor')
    sectionNumber = data.get('section')

    if new_schedule and len(new_schedule) == 5 and all(len(day) == 20 for day in new_schedule):
        for day_index, day in enumerate(new_schedule):
            for time_slot_index, class_names in enumerate(day):
                if class_names:
                    day_name = list(day_to_index.keys())[day_index]
                    day_obj = Day.query.filter_by(name=day_name).first()

                    if not day_obj:
                        day_obj = Day(name=day_name)
                        db.session.add(day_obj)
                        db.session.commit()

                    time_slot_obj = TimeSlot.query.filter_by(day_id=day_obj.id, time=timeBlock).first()
                    if not time_slot_obj:
                        time_slot_obj = TimeSlot(day_id=day_obj.id, time=timeBlock)
                        db.session.add(time_slot_obj)
                        db.session.commit()

                    for class_name in class_names:
                        existing_class = ScheduledClass.query.filter_by(
                            name=class_name,
                            time_slot_id=time_slot_obj.id,
                            class_section=sectionNumber
                        ).first()

                        if not existing_class:
                            class_obj = ScheduledClass(
                                name=class_name,
                                professor_name=profName,
                                time_slot_id=time_slot_obj.id,
                                day_blocks="".join(dayBlocks),
                                class_section=sectionNumber
                            )
                            db.session.add(class_obj)

                    db.session.commit()
        
        # Copy classes to paired days
        copy_classes(dayBlocks, sectionNumber)

        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "message": "Schedule added successfully"})
        }
    
    return {
        "statusCode": 400,
        "body": json.dumps({"success": False, "message": "Invalid input"})
    }

def copy_classes(dayBlocks, sectionNumber):
    # Copying logic (same as your original code)
    pass
