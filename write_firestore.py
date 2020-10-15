import json
import pprint
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("english-vocabulary-exercises-firebase-adminsdk-mjz1s-4edbb83978.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client(app)

PARENT = '0zwuF8q0eHklNDFZJAH9'


if __name__ == '__main__':
    subcategories = db.collection('subcategories')


    with open('data/artsentlit.json') as f:
        data = json.load(f)

    for category, groups in data.items():
        doc = subcategories.document()
        doc.create({'name': category+' Trial', 'parent': PARENT, 'createdAt': datetime.datetime.now()})
        col = doc.collection('groups')
        for number in sorted(groups.keys(), key=lambda x: int(x)):
            current = groups[number]
            group_doc = col.document()
            group_doc.create({'words': current['words'], 'createdAt': datetime.datetime.now()})
            exercises = group_doc.collection('exercises')

            current_exercises = current['exercises']
            for exercise in sorted(current_exercises.keys(), key=lambda x: int(x)):
                exercise_document = exercises.document()
                exercise_document.create(
                    {'questions': current_exercises[exercise]['questions'], 'createdAt': datetime.datetime.now()}
                )
