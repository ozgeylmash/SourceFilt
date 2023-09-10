from utils.lower_title import lower
import pandas as pd

class BookCategorizer():
    """
    Kitap Kategorileştirici V4
    """
    
    @staticmethod
    def determine_category(name, publisher):
        """
        Kitap isminde anahtar kelimeleri arayarak ait olduğu dersi, sınıfı ve yılı bulur.
        """
        possible_subjects = []
        possible_grades = []
        possible_years = []
        possible_types = []

        text = lower(name)
        publisher = lower(publisher)

        text_list = text.split()
        publisher_list = publisher.split()  
        result_list  = [word for word in text_list if word not in publisher_list]
        text = ' '.join(result_list)

        # Ders odaklı bir kitap ise
        for subject in BookCategorizer.keywords.columns:
            if text.find(subject) != -1:
                possible_subjects.append(subject)
        
        for grade in BookCategorizer.keywords.index:
            if text.find(grade) != -1:
                possible_grades.append(grade) 

        # Konu odaklı bir kitap ise
        for subject, grades in BookCategorizer.keywords.items():
            for grade, topics in grades.items():
                for topic in topics:
                    if text.find(topic) != -1:
                        if not possible_subjects:
                            possible_subjects.append(subject)
                        if not possible_grades:
                            possible_grades.append(grade)   

        # Çıkış yılı bulma
        years = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]

        for year in years:
            if year in text:
                possible_years.append(year)

        # Tür kategorisi bulma
        type_categories = {
            "soru bankası": ["soru bankası", "soru kitabı"],
            "deneme": ["deneme"]
        }

        for key, types in type_categories.items():
            for type in types:
                if type in lower(text):
                    possible_types.append(key)


        print("****************************************")
        print("Book:", name)
        print("Possible Subjects: ", possible_subjects)
        print("Possible Grades: ", possible_grades)
        print("Possible Years: ", possible_years)
        print("Possible Types: ", possible_types)
        print("****************************************")

        try: final_subject = max(set(possible_subjects), key=possible_subjects.count)
        except: final_subject = "genel"
        try: final_grade = max(set(possible_grades), key=possible_grades.count)
        except: final_grade = "lise"
        try: final_year = max(possible_years)
        except: final_year = None
        try: final_type = max(set(possible_types), key=possible_types.count)
        except: final_type = None

        if len(list(set(possible_subjects).intersection(["fizik", "kimya", "biyoloji"]))) >= 2:
            final_subject = "fen"

        if len(list(set(possible_subjects).intersection(["tarih", "coğrafya", "felsefe", "din"]))) >= 2:
            final_subject = "sosyal"

        if final_grade == "ydt":
            final_subject = "ingilizce"

        if final_grade == "ingilizce":
            final_subject = "ydt"

        if "sayısal" in possible_subjects and "sözel" in possible_subjects:
            final_grade = "genel"

        if "tyt" in possible_grades and "ayt" in possible_grades:
            final_grade = "lise"

        return final_subject, final_grade, final_year, final_type
    

    keywords = pd.DataFrame({"sayısal": [[], [], [], [], [], [], []],
                        "matematik": [["mantık", "kümeler", "eşitsizlikler", "üçgenler", "üslü", "köklü"], ["olasılık", "fonksiyonlar", "polinomlar", "ikinci dereceden denklemler", "dörtgenler", "çokgenler"], ["trigonometri", "analitik", "çember", "daire", "olasılık"], ["üstel", "logaritma", "dizi", "limit", "süreklilik", "türev", "integral"], ["problem", "geometri"], ["geometri"], []],
                        "fen": [[], [], [], [], [], [], []],
                        "fizik": [["madde ve özellikleri", "hareket", "kuvvet", "enerji", "ısı", "sıcaklık", "elektrostatik"], ["elektrik akımı", "direnç", "elektromotor", "elektrik", "manyetizma", "basınç", "kaldırma", "dalga", "ayna"], ["vektör", "hareket", "atışlar", "itme", "momentum", "tork", "denge", "makine", "manyetik alan", ], ["çembersel hareket", "açısal momentum", "kepler", "harmonik", "doppler", "atom fiziği", "radyoaktivite", "kuantum fiziği"], [], [], []],
                        "kimya": [["atom", "periyodik", "kimyasal", "maddenin halleri"], ["mol", "karışımlar", "asit", "baz", ], ["gazlar", "çözeltiler", "çözünürlük", "tepkimelerde enerji", "tepkimelerde hız", "tepkimelerde denge"], ["karbon", "organik", ], [], [], []],
                        "biyoloji": [["hücre", "canlılar"], ["hücre bölünme", "kalıtım", "ekosistem"], ["fizyoloji", "sistemler", "komünite", "popülasyon"], ["enerji dönüşüm", "bitki"], [], [], []],
                        "sözel": [[], [], [], [], [], [], []],
                        "türkçe": [[], [], [], [], ["sözcük", "cümle", "imla", "yazım", "paragraf", "dil bilgisi", "noktalama"], ["paragraf", "dil bilgisi"], []],
                        "edebiyat": [[], [], [], [], [], [], []],
                        "sosyal": [[], [], [], [], [], [], []],
                        "tarih": [[], [], [], [], [], [], []],
                        "coğrafya": [[], [], [], [], [], [], []],
                        "felsefe": [[], [], [], [], [], [], []],
                        "din": [[], [], [], [], [], [], []],
                        "ingilizce": [[], [], [], [], [], [], ["yksdil"]],
                        "genel": [[], [], [], [], [], [], []]
                        }, index=["9.", "10.", "11.", "12.", "tyt", "ayt", "ydt"])
