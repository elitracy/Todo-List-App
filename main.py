from datetime import date
import json
import todoCalendar


todoList = {}
listLen = 0

today = str(date.today())
today = int(today[5:7]+today[8:10]+today[0:4])

#item class
class newItem:
    def __init__(self,task,date):
        self.task = task
        self.date = date

#read in json file
with open("todolist.json", 'r') as jsonFile:
    todoList = json.load(jsonFile)
    #listLen = len(todoList)
    jsonFile.close()

#start user prompts
user = ""
while user != "exit":
    user = input("")
    cont = True
    if user == "new":
        
        while cont:
            #add to json object
            tempTask = newItem(input("Task: "),input("Date Due[mm/dd/yyyy]: "))
            todoList.append({
                "task": tempTask.task,
                "date": int(tempTask.date)
            })
            
            year = tempTask.date[4:8]
            month = tempTask.date[0:2]
            day = tempTask.date[2:4]
            googleDate = '%s-%s-%s' % (year,month,day)

            #create new event on Google Calendar            
            todoCalendar.createNewEvent(tempTask.task,googleDate,googleDate)

            #prompt for new task
            contPrompt = input("New Task[y/n]: ")
            if contPrompt == 'n'.casefold() or contPrompt == 'no'.casefold():
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

        todoCalendar.listEvents()
        """
        for i in data:
            #if(i.get('date') == today):
            print(i.get('task'))
        print()
        jsonFile.close()
        """      
    
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

        
      