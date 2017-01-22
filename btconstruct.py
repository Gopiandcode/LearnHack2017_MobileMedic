import json
from collections import Counter
import interface

class Illness:
    def __init__(self, name, symptoms, cure):
        self.name = name
        self.symptoms = symptoms
        self.cure = cure


class Question:
    def __init__(self, symptom, left, right):
        self.symptom = symptom
        self.true = right
        self.false = left


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
        symptoms = (symptom for illness in self.illnesses for symptom in illness.symptoms)
        symptoms_count = Counter(symptoms)
        symptoms = set(symptoms)
        for i in symptoms:
            print(i)
        symptoms_list = list(sorted(set(symptoms), key=lambda i:symptoms_count[i]))
        for i in symptoms_list:
            print("item: ",i)

        def question_consumer(sorted_symptoms, illnesses):
            if len(illnesses) == 1:
                return Question(illnesses[0], None, None)
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
        current = self.root
        def dict_from_data(question):
            if question.false is None and question.true is None:
                return {
                    "type" : "message",
                    "header" : "** #illness result **",
                    "description" : "You have the illness {}, the cure is {}".format(question.symptom.name, question.symptom.cure)
                }
            right = dict_from_data(question.true)
            left = dict_from_data(question.false)

            return {
                "type" : "input",
                "header" : "** #Symptom **",
                "content": {
                    "type" : "string",
                    "description": "Do you have the symptom {}?".format(question.symptom.name),
                    # TODO Add CORRECT SYSTAX FOR TRUE AND FALSE
                    "left" : left,
                    "right" : right
                }
            }
        return json.dumps(dict_from_data(self.root))
def getIllness():
    illness_name, symptoms, cure = interface.inputNode()
    return Illness(illness_name, symptoms, cure)


if __name__ == '__main__':
    decision_tree = Tree()
    for i in range(2):
        decision_tree.add_illness(getIllness())
    decision_tree.balance_tree();
    print(decision_tree.serialize())