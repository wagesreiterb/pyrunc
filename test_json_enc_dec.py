import json

# https://www.seanjohnsen.com/2016/11/23/pydeserialization.html

class Structure(object):

    _fields = []

    def _init_arg(self, expected_type, value):
        if isinstance(value, expected_type):
            return value
        else:
            return expected_type(**value)

    def __init__(self, **kwargs):
        field_names, field_types = zip(*self._fields)
        assert([isinstance(name, str) for name in field_names])
        assert([isinstance(type_, type) for type_ in field_types])

        for name, field_type in self._fields:
            setattr(self, name, self._init_arg(field_type, kwargs.pop(name)))

        # Check for any remaining unknown arguments
        if kwargs:
            raise TypeError('Invalid arguments(s): {}'.format(','.join(kwargs)))


class House(Structure):
    _fields = [('name', str), ('age', int), ('colors', list), ('words', str), ('seat', str)]

    def fly_banner(self):
        print('flying banner')


class Tyrion(Structure):
    _fields = [('name', str), ('house', House), ('age', int), ('sibling_names', list)]

    def drink(liters, alcohol):
        print('drinking %d liters of %s' % (liters, alcohol,))


house = House(
    name = "Lannister",
    age = 700,
    colors = ["Red", "Gold"],
    words = "Hear Me Roar!",
    seat = "Casterly Rock"
)

tyrion = Tyrion(name = "Tyrion", house = house, age = 23, sibling_names = ["Jaime", "Joffrey", "Cersei"])


#print(my_tyrion.drink("Wodka"))
print(tyrion.house.age)
print(tyrion.name)
print(tyrion)
print(type(tyrion))
a_dict = {
    'name': "Tyrion_1",
    'house': {
        'name': 'Lannister_1',
        'age': 700,
        'colors': ['Red', 'Gold'],
        'words': 'Hear Me Roar!',
        'seat': 'Casterly Rock'
    },
    'age': 15,
    'sibling_names': ['Jaime', 'Joffrey', 'Cersei']
}

print(a_dict)

tyrion = Tyrion(**a_dict)
print(tyrion.name)
#json.dumps(tyrion)