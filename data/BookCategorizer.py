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
    
    keywords = pd.DataFrame({"sayısal": [[], [], [], [], [], []],
                        "matematik": [["mantık", "kümeler", "eşitsizlikler", "üçgenler", "üslü", "köklü"], ["olasılık", "fonksiyonlar", "polinomlar", "ikinci dereceden denklemler", "dörtgenler", "çokgenler"], ["trigonometri", "analitik", "çember", "daire", "olasılık"], ["üstel", "logaritma", "dizi", "limit", "süreklilik", "türev", "integral"], ["problem", "geometri"], ["geometri"]],
                        "fen": [[], [], [], [], [], []],
                        "fizik": [["madde ve özellikleri", "hareket", "kuvvet", "enerji", "ısı", "sıcaklık", "elektrostatik"], ["elektrik akımı", "direnç", "elektromotor", "elektrik", "manyetizma", "basınç", "kaldırma", "dalga", "ayna"], ["vektör", "hareket", "atışlar", "itme", "momentum", "tork", "denge", "makine", "manyetik alan", ], ["çembersel hareket", "açısal momentum", "kepler", "harmonik", "doppler", "atom fiziği", "radyoaktivite", "kuantum fiziği"], [], []],
                        "kimya": [["atom", "periyodik", "kimyasal", "maddenin halleri"], ["mol", "karışımlar", "asit", "baz", ], ["gazlar", "çözeltiler", "çözünürlük", "tepkimelerde enerji", "tepkimelerde hız", "tepkimelerde denge"], ["karbon", "organik", ], [], []],
                        "biyoloji": [["hücre", "canlılar"], ["hücre bölünme", "kalıtım", "ekosistem"], ["fizyoloji", "sistemler", "komünite", "popülasyon"], ["enerji dönüşüm", "bitki"], [], []],
                        "sözel": [[], [], [], [], [], []],
                        "türkçe": [[], [], [], [], ["sözcük", "cümle", "imla", "yazım", "paragraf", "dil bilgisi", "noktalama"], ["paragraf", "dil bilgisi"]],
                        "edebiyat": [[], [], [], [], [], []],
                        "sosyal": [[], [], [], [], [], []],
                        "tarih": [[], [], [], [], [], []],
                        "coğrafya": [[], [], [], [], [], []],
                        "felsefe": [[], [], [], [], [], []],
                        "din": [[], [], [], [], [], []],
                        "genel": [[], [], [], [], [], []]
                        }, index=["9.", "10.", "11.", "12.", "tyt", "ayt"])
