from datetime import date
import json
import todoCalendar


todoList = {}
listLen = 0

today = str(date.today())
today = int(today[5:7]+today[8:10]+today[0:4])

#color class for printing 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#item class
class newItem:
    def __init__(self,task,date,active,completed):
        self.task = task
        self.date = date
        self.active = active
        self.completed = completed

#read in json file
with open("todolist.json", 'r') as jsonFile:
    todoList = json.load(jsonFile)
    #listLen = len(todoList)
    jsonFile.close()

#start user prompts
user = ""
while user != "exit":
    user = input("\n[list | new | remove | exit]: ")
    cont = True
    if user == "new":
        
        while cont:
            #add to json object
            tempTask = newItem(input("Task: "),input("Date Due[mm/dd/yyyy]: "),False,False)
            todoList.append({
                "task": tempTask.task,
                "date": int(tempTask.date),
                "active": tempTask.active,
                "completed": tempTask.completed
            })
            
            year = tempTask.date[4:8]
            month = tempTask.date[0:2]
            day = tempTask.date[2:4]
            googleDate = '%s-%s-%s' % (year,month,day)

            #create new event on Google Calendar            
            todoCalendar.createNewEvent(tempTask.task,googleDate,googleDate)

            #prompt for new task
            """contPrompt = input("New Task[y/n]: ")
            if contPrompt == 'n'.casefold() or contPrompt == 'no'.casefold():
                """
            cont = False
            
        #write to json file
        jsonFile = open("todoList.json", 'w+')
        jsonFile.write(json.dumps(todoList, indent=4))
        jsonFile.close()
    
    elif user == "list":

        #read in json file
        jsonFile = open('todoList.json', 'r+')
        data = json.load(jsonFile)
        print("\nTodo:\n")
        if data == []:
            print('Nothing to do today!\n')

        #todoCalendar.listEvents()
        
        for i in data:
            #if(i.get('date') == today):
            if i.get('completed') == True:
                print(bcolors.OKBLUE + i.get('task') + bcolors.ENDC)
            elif i .get('active') == True:
                print(bcolors.OKGREEN + i.get('task') + bcolors.ENDC)
            else:
                print(i.get('task'))
        print()
        jsonFile.close()
             
    
    elif "rem".casefold() in user or "del".casefold() in user:
        jsonFile = open('todoList.json', 'r+')
        data = json.load(jsonFile)
        jsonFile.close()
      
        strToRemove = user.split(" ")[1]

        for i in data:
            for key,val in i.items():
                if strToRemove in str(val):
                    #print('Item Found\nRemoving Item')
                    data.remove(i)
                    jsonFile = open("todoList.json", 'w+')
                    jsonFile.write(json.dumps(data, indent=4))
                    jsonFile.close()

                    todoCalendar.removeEvent(i['task'])

                    #print(str(i['task']))
                    #todoCalendar.removeEvent(str(i['task']))

    elif 'track' in user:
        jsonFile = open('todoList.json', 'r+')
        data = json.load(jsonFile)
        jsonFile.close()

        strToFind = user.split(" ")[1]

        for i in data:
            for key,val in i.items():
                if strToFind in str(val):
                    i['active'] = True
                    print(i['active'])

        jsonFile = open("todoList.json", 'w+')
        jsonFile.write(json.dumps(data, indent=4))
        jsonFile.close()

    elif 'stop' in user:
        jsonFile = open('todoList.json', 'r+')
        data = json.load(jsonFile)
        jsonFile.close()

        strToFind = user.split(" ")[1]

        for i in data:
            for key,val in i.items():
                if strToFind in str(val):
                    i['active'] = False
                    print(i['active'])

        jsonFile = open("todoList.json", 'w+')
        jsonFile.write(json.dumps(data, indent=4))
        jsonFile.close()

    elif 'done' in user:

        jsonFile = open('todoList.json', 'r+')
        data = json.load(jsonFile)
        jsonFile.close()

        strToFind = user.split(" ")[1]

        for i in data:
            for key,val in i.items():
                if strToFind in str(val):
                    i['active'] = False
                    i['completed'] = True
                    print(i['active'])

        jsonFile = open("todoList.json", 'w+')
        jsonFile.write(json.dumps(data, indent=4))
        jsonFile.close()


