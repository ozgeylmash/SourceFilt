from BookCategorizer import BookCategorizer as BC

result = BC.determine_category("2023 AYT 40 Seans Matematik Fizik Kimya Soru Bankaları ve 68 Deneme Seti Kalemlik HEDİYELİ Okyanus Yayınları") 

print(result) # -> ('fen', 'ayt')

## Test verisetini güncel fonksiyonu kullanarak yazdırır.
# import pandas as pd

# df = pd.read_csv("data/book_titles.csv")

# df[['subject','grade']] = df["text"].map(BC.determine_category).apply(pd.Series)
# df.to_csv("complete-v2.csv")
