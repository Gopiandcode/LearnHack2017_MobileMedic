def inputNode():
    illness = input("Please type in Illness\n").lower()
    print(illness)
    symptoms = input("Please type in symptoms, separated by commas\n").split(",")
    symptoms = [symptom.strip().lower() for symptom in symptoms]
    print(symptoms)
    cure = input("Please type in cure\n").lower()
    print(cure)
    return illness, symptoms, cure
