import json
import datetime

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
    self.date = datetime.datetime.now()


p1 = Person("John", 36)


#p1_json = json.dumps(p1.__dict__)
#print(p1_json)


# https://code-maven.com/serialize-datetime-object-as-json-in-python
#
def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    #if isinstance(obj, datetime.datetime):
    #    return obj.__str__()
    if isinstance(obj, datetime.datetime):
        # datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return obj.__str__()
    else:
        return obj.__dict__


dump = json.dumps(p1, default=serialize)
print(dump)
