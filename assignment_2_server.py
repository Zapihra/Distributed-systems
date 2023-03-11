from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

def addElement(inputTopic, inputNote, inputText):

    now = datetime.now()
    timestamp = now.strftime("%m/%d/%y - %H:%M:%S")

    tree = ET.parse('db.xml')
    root = tree.getroot()

    findThis = ".//*[@name='{}']".format(inputTopic)

    value = root.find(findThis)
    if value != None: #If found topic
        
        note = ET.Element('note')
        note.set('name', inputNote)

        textS = ET.SubElement(note, 'text')
        textS.text = inputText

        timest = ET.SubElement(note, 'timestamp')
        timest.text = str(timestamp)
        
        value.append(note)
        tree.write('db.xml')

        return "added new note"
    else:
        topic = ET.Element('topic')
        topic.set('name', inputTopic)

        note = ET.SubElement(topic, 'note')
        note.set('name', inputNote)

        textS = ET.SubElement(note, 'text')
        textS.text = inputText

        timest = ET.SubElement(note, 'timestamp')
        timest.text = str(timestamp)

        root.append(topic)
        tree.write('db.xml')

        return "added new topic"
    
def printElement(inputTopic):

    tree = ET.parse('db.xml')
    root = tree.getroot()

    return_list = []
    
    for note in root.findall(".//*[@name='{}']/note".format(inputTopic)):
        
        temp_list = []

        noteName = note.get('name')
        text = note.find('text').text
        timest = note.find('timestamp').text

        temp_list.append(noteName)
        temp_list.append(text)
        temp_list.append(timest)
        
        return_list.append(temp_list)

    return return_list

def wikiServer(topic, note):
    session = requests.Session()
    print
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {"action": "opensearch",
              "namespace": "0",
              "search": note,
              "limit": "5",
              "format": "json"
              }
    
    req = session.get(url=URL, params= PARAMS)
    data = req.json()[3]
    info = ""
    for i in data:

        info += ", " + i

    addElement(topic, note, info)

    return "Added to note or topic"


server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(addElement, "addElement")
server.register_function(printElement, "printElement")
server.register_function(wikiServer, "wikiServer")
server.serve_forever()