import json, os

if not os.path.exists("./data.json"):
    with open('names.list', 'r') as fs:
        content = fs.readlines()[1].rstrip();
        names = content.split(", ")

        data_json = {}
        for i, obj in enumerate(names):
            gen_pay_list = {}
            for j, sub_obj in enumerate(names):
                if sub_obj != obj:
                    # Set default pay value to 0, obviously ;)
                    gen_pay_list[sub_obj] = 0
            gen_pay_list['earned'] = 0
            data_json[obj] = gen_pay_list
        
        # Write to data.json
        with open('data.json', 'w') as outfile:
            outfile.write(json.dumps(data_json, indent=4))
            print("Debt data file created!")



with open('data.json', 'r') as fs:
    data_json = json.load(fs)


def dn():
    print(data_json)
    print()
    print(data_json['ben'])
    print("keys:")
    tmp = "Exclude, out of: "
    for field in data_json.keys():
        tmp += field + ", "
    tmp = tmp[:-2]
    print(tmp)
dn()
