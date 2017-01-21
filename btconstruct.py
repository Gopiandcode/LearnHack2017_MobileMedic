import json


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
        self.root = Question()

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
        pass

    def serialize(self):
        pass
