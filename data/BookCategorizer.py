import pandas as pd

class BookCategorizer():
    
    @staticmethod
    def determine_category(text):
        """
        Kitap isminde anahtar kelimeleri arayarak ait olduğu dersi ve sınıfı bulur.
        """
        possible_subjects = []
        possible_grades = []

        final_subject = None
        final_grade = None

        # Ders odaklı bir kitap ise
        for subject in BookCategorizer.keywords.columns:
            if text.lower().find(subject) != -1:
                possible_subjects.append(subject)
        
        for grade in BookCategorizer.keywords.index:
            if text.lower().find(grade) != -1:
                possible_grades.append(grade) 

        # Konu odaklı bir kitap ise
        for subject, grades in BookCategorizer.keywords.items():
            for grade, topics in grades.items():
                for topic in topics:
                    if text.lower().find(topic) != -1:
                        possible_subjects.append(subject)
                        possible_grades.append(grade)   

        print("Possible Subjects: ", possible_subjects)
        print("Possible Grades: ", possible_grades)

        if len(set(possible_subjects)) == 1:
            final_subject = possible_subjects[0]

        if len(set(possible_grades)) == 1:
            final_grade = possible_grades[0]
        
        return final_subject, final_grade
    
    # Henüz tam değil.
    keywords = pd.DataFrame({"sayısal": [[], [], [], [], [], []],
                        "matematik": [["mantık", "kümeler"], ["olasılık", "fonksiyonlar"], ["trigonometri", "eşitsizlik"], ["limit", "süreklilik"], [], []],
                        "fen": [[], [], [], [], [], []],
                        "fizik": [[], [], [], [], [], []],
                        "kimya": [[], [], [], [], [], []],
                        "biyoloji": [[], [], [], [], [], []],
                        "sözel": [[], [], [], [], [], []],
                        "türkçe": [[], [], [], [], [], []],
                        "edebiyat": [[], [], [], [], [], []],
                        "sosyal": [[], [], [], [], [], []],
                        "tarih": [[], [], [], [], [], []],
                        "coğrafya": [[], [], [], [], [], []],
                        "felsefe": [[], [], [], [], [], []],
                        "din": [[], [], [], [], [], []],
                        "genel": [[], [], [], [], [], []]
                        }, index=["9.", "10.", "11.", "12.", "tyt", "ayt"])
