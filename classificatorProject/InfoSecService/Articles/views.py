from django.shortcuts import render
from lxml import etree
import os

textClasses = ['career',\
               'cryptography',\
               'development',\
               'finance',\
               'information_security',\
               'interviews',\
               'law',\
               'machine_learning',\
               'network',\
               'various']
textClassesRus = ['Карьера',\
                  'Криптография',\
                  'Разработка',\
                  'Финансы',\
                  'ИБ и уязвимости',\
                  'Интервью',\
                  'Законодательство',\
                  'Машинное обучение',\
                  'Сетевые технологии',\
                  'Разное']
textClassesList = []
for index in range(len(textClasses)):
    textClassesList.append({"eng": textClasses[index],\
                            "rus": textClassesRus[index]})

def classes(request):
    articleAmount = 0
    for textClass in textClasses:
        articlesFiles = os.listdir("Articles//articles//" + textClass + "//")
        articleAmount = articleAmount + len(articlesFiles)
    
    return render(request, "TextClassesList.html",\
                  context={"text_classes": textClassesList, "article_amount": articleAmount})

def articles(request, class_name):
    if class_name in textClasses:
        textClass = textClassesList[textClasses.index(class_name)]
    else:
        return render(request, "page404.html")

    articlesFiles = os.listdir("Articles//articles//" + class_name + "//")
    articles = []
    for article in articlesFiles:
        try:
            tree = etree.parse("Articles//articles//" + class_name + "//" + article)
        except Exception:
            continue
        title = tree.xpath('//title')[0].text
        articles.append({"title": title,\
                         "name": article})

    return render(request, "ArticlesList.html",\
                  context={"text_class": textClass, "articles": articles})

def article(request, class_name, article_name):
    print(class_name)
    print(article_name)
    try:
        tree = etree.parse("Articles//articles//" + class_name + "//" + article_name)
    except Exception:
        return render(request, "page404.html")
    
    title = tree.xpath('//title')[0].text
    text = tree.xpath('//text')[0].text
    
    return render(request, "Article.html",\
                  context={"title": title, "text": text})

