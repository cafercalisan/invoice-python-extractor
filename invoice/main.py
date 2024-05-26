import pdfplumber
import pandas as pd

def extract_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ''
        all_tables = []
        
        for page in pdf.pages:
            # Metni çıkar
            text = page.extract_text()
            if text:
                all_text += text + "\n"
            
            # Tablo çıkar (eğer varsa)
            table = page.extract_table()
            if table:
                # Tabloyu bir pandas DataFrame'e dönüştür
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)
        
        return all_text, all_tables

# PDF dosya yolu
pdf_path = 'C:/Invoice/fatura3.pdf'

# PDF'den verileri çıkar
extracted_text, extracted_tables = extract_data_from_pdf(pdf_path)

# Çıkarılan metni yazdır
print("Çıkarılan Metin:\n", extracted_text)

# Çıkarılan tabloları yazdır (eğer varsa)
for i, table in enumerate(extracted_tables, start=1):
    print(f"Tablo {i}:\n", table)

