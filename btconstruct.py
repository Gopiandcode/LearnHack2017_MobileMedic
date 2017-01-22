import json
from collections import Counter
import interface
root = "medic"
class Illness:
    def __init__(self, name, symptoms, cure):
        self.name = name
        self.symptoms = symptoms
        self.cure = cure

    def serialize(self, parent):
        content = {
            "ref": root + "/" + self.name + ".json",
            "menuRef" : parent,
            "type": "menu",
            "header": "**Your Diagnosis**\nYou might have " + self.name + ", a possible cure would be " + self.cure,
            "content": []
        }
        end = {
            "type": "end",
            "ref": "#diagnosis"
        }
        output = {"content": [content, end]}
        output_name = root + "/" + self.name + ".json"
        with open("./" + output_name, 'w') as file:
            json.dump(output, file)

        return output_name


class Question:
    def __init__(self, symptom, left, right):
        self.symptom = symptom
        self.true = right
        self.false = left

    def serialize(self, path=None):
        output_name = root + "/" + self.symptom + ".json"
        left = {
            "ref": self.true.serialize(output_name),
            "type": "linkStatic",
            "description": "yes"
            }
        right = {
            "ref": self.false.serialize(output_name),
            "type": "linkStatic",
            "description": "no"
            }
        content = {
            "type": "menu",
            "header": "Do you have the symptom {}?".format(self.symptom),
            "content": [left, right]
        }
        end = {
            "type": "end",
            "ref": "#diagnosis"
        }
        if path is not None:
            content["menuRef"] = path
        output = {"content":[content, end]}
        with open("./" + output_name, 'w') as file:
            json.dump(output, file)
        return output_name


class Tree:
    def __init__(self):
        self.illnesses = []
        self.root = None #initially nothing

    def add_illness(self, node):
        assert isinstance(node, Illness), "node must be of type Illness"
        self.illnesses.append(node)

    def add_illnesses(self, illnesses):
        for illness in illnesses:
            self.add_illness(illness)

    def remove_illness(self, node):
        assert isinstance(node, Illness), "node must be of type Illness"
        del self.illnesses[self.illnesses.index(node)]

    def balance_tree(self):
        symptoms = list(symptom for illness in self.illnesses for symptom in illness.symptoms)
        symptoms_count = Counter(symptoms)
        symptoms = set(symptoms)

        symptoms_list = list(sorted(symptoms, key=lambda i:symptoms_count[i]))

        def question_consumer(sorted_symptoms, illnesses):
            if len(illnesses) == 1 or len(sorted_symptoms) == 0:
                return illnesses[0]
            current_symptom = sorted_symptoms[0]
            yes_illnesses = []
            no_illnesses = []

            for illness in illnesses:
                if current_symptom in illness.symptoms:
                    yes_illnesses.append(illness)
                else:
                    no_illnesses.append(illness)

            yes_question = question_consumer(sorted_symptoms[1:], yes_illnesses)
            no_question = question_consumer(sorted_symptoms[1:], no_illnesses)

            return Question(current_symptom, no_question, yes_question)

        self.root = question_consumer(symptoms_list, self.illnesses)

    def serialize(self):
        return self.root.serialize()
def getIllness():
    illness_name, symptoms, cure = interface.inputNode()
    return Illness(illness_name, symptoms, cure)

def serializeTree(tree):
    parent_ref = tree.serialize()
    print(parent_ref)
    begin = {
        "ref" : parent_ref,
        "type" : "linkStatic",
        "description" : "#Begin Diagnosis"
    }
    content = {
        "menuRef" : root + "/index.json",
        "type" : "menu",
        "header" : "** #medic menu **",
        "content" : [begin]
    }
    end = {
        "type": "end",
        "ref": "#medic"
    }
    output = {"content" : [content, end]}
    output_file = "./" + root + "/index.json"
    with open(output_file, 'w') as file:
        json.dump(output, file)
    return



if __name__ == '__main__':
    decision_tree = Tree()
    get_data = True
    while get_data:
        decision_tree.add_illness(getIllness())
        get_data = input("Enter more data?(y/n):") == "y"
    decision_tree.balance_tree();
    serializeTree(decision_tree)