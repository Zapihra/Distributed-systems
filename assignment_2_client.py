import xmlrpc.client

def makeTopic():
    inputTopic = input("give a topic: ")
    inputNote = input("give a note: ")
    inputText = input("give text about the topic: ")
    
    try:
        with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
            print("%s" % proxy.addElement(inputTopic, inputNote, inputText))
    except:
        print("error has occurred in server")

    return

def printTopic():
     
    inputTopic = input("What topic do you want to see? ")

    try:
        with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
            returned_list = proxy.printElement(inputTopic)
    except:
        print("error has occurred in server")
        return

    print("In topic of " + inputTopic)
    for lists in returned_list:
        print("note:", lists[0],  "made at a time of", lists[2])
        print("The text:", lists[1])

    return

def addWiki():
    topic = input("Give the topic where to deposit: ")
    note = input("Give the note you want to search in wikipedia: ")
    
    try:
        with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
            text = proxy.wikiServer(topic, note)
    except:
        print("error has occurred in server")
        return

    print(text)

    return

def main():

    while(True):
        print("0: exit")
        print("1: append or make a topic")
        print("2: print a topic")
        print("3: search wiki and add to topic")

        nmb = input("what do you wanna do? ")

        if nmb == "0":
            break
        elif nmb == "1":
            makeTopic()
        elif nmb == "2":
            printTopic()
        elif nmb == "3":
            addWiki()
        else:
            print("wrong input try again")
    
    return
        


main()    