import json
from collections import Counter
import interface

class Illness:
    def __init__(self, name, symptoms, cure):
        self.name = name
        self.symptoms = symptoms
        self.cure = cure
    def serialize(self):
        return {
                    "type" : "message",
                    "header" : "** #illness result **",
                    "description" : "You have the illness {}, the cure is {}".format(self.name, self.cure)
                }

class Question:
    def __init__(self, symptom, left, right):
        self.symptom = symptom
        self.true = right
        self.false = left
    def serialize(self):
        return {
            "type": "input",
            "header": "** #Symptom **",
            "content": {
                "type": "string",
                "description": "Do you have the symptom {}?".format(self.symptom),
                # TODO Add CORRECT SYSTAX FOR TRUE AND FALSE
                "no": self.false.serialize(),
                "yes": self.true.serialize()
        }}


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
        return json.dumps(self.root.serialize())
def getIllness():
    illness_name, symptoms, cure = interface.inputNode()
    return Illness(illness_name, symptoms, cure)


if __name__ == '__main__':
    decision_tree = Tree()
    for i in range(2):
        decision_tree.add_illness(getIllness())
    decision_tree.balance_tree();
    print(decision_tree.serialize())