import os, random, pprint, pickle, json
from flask import Flask, render_template

objectTemplates = ['Character', 'Class', 'Location', 'Item', 'Skill']
idCounter=0

def generateId():
    global idCounter
    idCounter+=1
    return idCounter

class dice():
    """A simple random object with range, current value and history."""
    def __init__(self, min, max, n=1):
        self.min = min
        self.max = max
        self.n = n
        self.current = None
        self.history=[]
    def roll(self):
        for die in range(0, self.n):
            if self.current and len(self.history) > 10:
                self.history.pop(0)
            self.current = random.randint(self.min, self.max)
            self.history.append(self.current)

class counter():
    """A simple range with minimum, maximum and current value."""
    def __init__(self, min, max, current=None):
        self.min = min
        self.max = max
        if current:
            self.current = current
        else:
            self.current = self.max
    def update(self, n):
        self.current=n

class rpgObject():
    """This is the generic object for trpgEngine"""
    def __init__(self, objectTemplate=None, tags=[]):
        self.id=generateId()
        self.objectTemplate=objectTemplate # This is the primary namespace for loaded Attributes and GUI styling.
        self.color='6996afff'
        self.tags=tags
        self.attributes={}
        self.children=[]
        self.rules=[] # Rules are just children objects, I think.
        if objectTemplate:
            # importTemplate(objectTemplate)
            pass
    def addAttribute(self, name, attribute=None):
        self.attributes[name]=attribute
    def addChild(self, object):
        self.children.append(object)
    def printObject(self, indent=0):
        output=""""""
        # for key, value in self.attributes.items():
        #     print(key, value)
        output+=('  ' * indent) + 'id: {0}\n'.format(self.id)
        output +=('  ' * indent) + 'template: {0}\n'.format(self.objectTemplate)
        output +=('  ' * indent) + 'color: {0}\n'.format(self.color)
        output +=('  ' * indent) + 'tags({1}): {0}\n'.format(self.tags, len(self.tags))
        output +=('  ' * indent) + 'rules({1}): {0}\n'.format(self.rules, len(self.rules))
        output +=('  ' * indent) + 'Attributes({1}):\n'.format(self.attributes, len(self.attributes))
        for key, value in self.attributes.items():
            if type(value) == type(rpgObject):
                output +=('  ' * (indent + 1)) + key + ':\n'
                value.printObject(indent + 2)
            elif type(value) == type(counter(0, 0, 0)):
                output +=('  ' * (indent + 1)) + key + ': ' + str(value.current) + '\n'
            else:
                output +=('  ' * (indent + 1)) + key + ': ' + str(value) + '\n'
        output +=('  ' * indent) + 'Children({1}):\n'.format(self.children, len(self.children))
        for object in self.children:
                object.printObject(indent + 1)
        # print(output)
        return output

app = Flask(__name__)

@app.route("/")
def hello():
    with open('scene.json', 'r') as f:
        data=json.load(f)
    return render_template("engine.html", data=json.dumps(data), globalId=idCounter)
    myScene = rpgObject('Scene')
    # myScene.addAttribute('entityType', 'Scene')
    myScene.color = '00000020'
    myScene.addAttribute('Title', 'Scene')
    myScene.addChild(rpgObject('Character'))
    myScene.children[0].addAttribute('Title', 'Hansel')
    myScene.children[0].color="7b0025ff"
    myScene.children[0].addAttribute('Gender', 'Male')
    # myScene.children[0].addAttribute('HP', counter(0, 10, 8))
    myScene.children[0].addChild(rpgObject('HP'))
    myScene.children[0].children[0].addAttribute('Title', 'HP')
    myScene.children[0].children[0].addAttribute('Base', 10)
    myScene.children[0].children[0].addAttribute('Current', 4)
    myScene.children[0].children[0].addAttribute('Temporary', 4)
    myScene.children[0].children[0].addAttribute('Total', 0)
    myScene.children[0].children[0].rules.append("Total=SUM(Current Temporary)")
    # myScene.children[0].addAttribute('Skills', rpgObject('SkillBook'))
    # myScene.children[0].attributes['Skills'].addChild(rpgObject('Skill'))
    myScene.children[0].addChild(rpgObject('Skill'))
    myScene.children[0].children[1].addAttribute('Title', 'Sprint')
    myScene.children[0].children[1].addAttribute('Description', 'Run twice your movement speed. Consumes your action.')
    myScene.children[0].addChild(rpgObject('Skill'))
    myScene.children[0].children[2].addAttribute('Title', 'Ready')
    myScene.children[0].children[2].addAttribute('Description', 'Prepare for a condition with advantage. Consumes your action.')
    myScene.addChild(rpgObject('Character'))
    myScene.children[1].addAttribute('Title', 'Gretel')
    myScene.children[1].addAttribute('Gender', 'Female')
    myScene.children[1].addAttribute('HP', counter(0, 8, 7))
    # sceneOutput=myScene.printObject()
    # sceneOutput=json.loads(myScene, default=lambda o: o.__dict__)
    sceneOutput=json.dumps(myScene, default=lambda o: o.__dict__)
    # print('Scene Output: {0}'.format(sceneOutput))
    return render_template("engine.html", data=sceneOutput, globalId=idCounter)

#
# if __name__ == '__main__':
#     # myDice = dice(1, 20, 4)
#     # myDice.roll()
#     # print(myDice.history)
#     # print(myDice.current)
#
#     myScene = rpgObject('Scene')
#     # myScene.addAttribute('entityType', 'Scene')
#     myScene.addChild(rpgObject('Character'))
#     myScene.children[0].addAttribute('Name', 'Hansel')
#     myScene.children[0].addAttribute('Gender', 'Male')
#     # myScene.children[0].addAttribute('HP', counter(0, 10, 8))
#     myScene.children[0].addChild(rpgObject('HP'))
#     myScene.children[0].children[0].addAttribute('Base', 10)
#     myScene.children[0].children[0].addAttribute('Current', 4)
#     myScene.children[0].children[0].addAttribute('Mod: Temporary', 4)
#     # myScene.children[0].addAttribute('Skills', rpgObject('SkillBook'))
#     # myScene.children[0].attributes['Skills'].addChild(rpgObject('Skill'))
#     myScene.children[0].addChild(rpgObject('Skill'))
#     myScene.children[0].children[0].addAttribute('Title', 'Sprint')
#     myScene.children[0].children[0].addAttribute('Description', 'Run twice your movement speed. Consumes your action.')
#     myScene.children[0].addChild(rpgObject('Skill'))
#     myScene.children[0].children[1].addAttribute('Title', 'Ready')
#     myScene.children[0].children[1].addAttribute('Description', 'Prepare for a condition with advantage. Consumes your action.')
#     myScene.addChild(rpgObject('Character'))
#     myScene.children[1].addAttribute('Name', 'Gretel')
#     myScene.children[1].addAttribute('Gender', 'Female')
#     myScene.children[1].addAttribute('HP', counter(0, 8, 7))
#     # pickle.dumps(myScene, -1)
#     myScene.printObject()
#     # myScene.children[1].printObject()
