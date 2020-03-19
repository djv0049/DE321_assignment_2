import json
import sqlite3
# connect to database
with open('config.json') as config:
    print("opening file")
    data = json.load(config)
    # con = sqlite3.connect(data['mysql']['host'],
    #                     data['mysql']['user'], data['mysql']['password'])

    con = sqlite3.connect(data['mysql']['db'])
    print('established connection' + con.__str__())
    con.execute("drop table Classname")

    con.execute(data['SQLCommands']['create'] +
                "Classname(att1 text, att2 real)")
    con.execute(data['SQLCommands']['insert'] + " ClassName Values ('hey', 1)")
    print(con.execute('select * from className').__str__())
    print('done')
