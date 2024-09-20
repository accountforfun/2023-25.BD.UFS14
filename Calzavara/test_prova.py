from jsonschema import validate
#lezione 3
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}

validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

def bool_validate(instance, schema):
    try:
        validate(instance = instance, schema = schema)
        return True
    except:
        return False
def test_json():
    assert bool_validate(instance={"name" : "Eggs", "price" : "Invalid"}, schema=schema) == False

def test_success():
    validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

#Lezione 2
def func(x):
    return x+1

def test_answer():
    assert func(3) == 4


