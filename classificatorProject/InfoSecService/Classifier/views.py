from django.shortcuts import render
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pickle
import re

# Инициализация классификатора и словаря слов
classifier = pickle.load(open("Classifier/classifier model.dat", 'rb'))
classifierDictionary = []
file = open("Classifier/classifier dictionary.txt", encoding='utf-8')
for line in file:
    classifierDictionary.append(line[:-1])
file.close()

textClasses = ['career',\
               'cryptography',\
               'development',\
               'finance',\
               'information_security',\
               'interviews',\
               'law',\
               'machine_learning',\
               'network',\
               'various',]
textClassesRus = ['Карьера',\
                  'Криптография',\
                  'Разработка',\
                  'Финансы',\
                  'ИБ и уязвимости',\
                  'Интервью',\
                  'Законодательство',\
                  'Машинное обучение',\
                  'Сетевые технологии',\
                  'Разное',]

def makeVector(text):
    vector = [0] * len(classifierDictionary)
    for word in text.split():
        normalizedWord = re.sub(r'[.,\/#!\?$%\^&\*;:{}=_`~()]', '', word.lower()).strip()
        if normalizedWord:
            if normalizedWord in classifierDictionary:
                index = classifierDictionary.index(normalizedWord)
                vector[index] = vector[index] + 1
    return np.array([vector], int)

def getTextClass(text):
    result = classifier.predict(makeVector(text))
    return textClassesRus[int(result[0]) - 1]


def classify(request):
    if request.method == "POST":
        text = request.POST.get("text")

        textClass = getTextClass(text)
        
        return render(request, "ClassifyResult.html",\
                      context={"textClass": textClass})
    else:
        return render(request, "ClassifyForm.html")

