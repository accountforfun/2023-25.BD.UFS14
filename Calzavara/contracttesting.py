print('hello world')
from jsonschema import validate

# A sample schema, like what we'd get from json.load()
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}

# If no exception is raised by validate(), the instance is valid.
validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)

#validate(
#    instance={"name" : "Eggs", "price" : "Invalid"}, schema=schema,
# )      non funziona perché il price vuole un numero e non una stringa

def bool_validate(instance, schema):
    try:
        validate(instance = instance, schema = schema)
        return True
    except:
        return False
print(bool_validate(instance={"name" : "Eggs", "price" : "Invalid"}, schema=schema))