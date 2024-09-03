
options = {
    'steak':    {"keywords":['steak'], "response":'order steak'},
    'eggs':     {"keywords":['eggs'], "response":'order eggs'},
    'potato':   {"keywords":['potato'], "response":'order potato'}
}

print(list(options.values())[0:-1:1])


print(', '.join([options[option]["response"] for option in list(options.values())[0:-1:1]]))
print(options[list(options.values())[-1]]["response"])