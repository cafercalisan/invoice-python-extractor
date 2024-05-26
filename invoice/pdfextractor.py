import pdfplumber
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Veri modeli
class ExtractedData(BaseModel):
    text: str
    tables: list

# FastAPI uygulaması oluştur
app = FastAPI()

# PDF'den veri çıkarma işlevi
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

# Ana Sayfa
@app.get("/")
def read_root():
    return {"message": "Hoş geldiniz! PDF dosyasını işlemek için /extract endpoint'ini kullanın."}

# PDF'den veri çıkarma endpoint'i
@app.get("/extract/")
def extract_from_pdf(pdf_path: str):
    # PDF'den verileri çıkar
    extracted_text, extracted_tables = extract_data_from_pdf(pdf_path)
    extracted_data = ExtractedData(text=extracted_text, tables=extracted_tables)
    return extracted_data.dict()

# JSON olarak kaydetme işlevi
def save_to_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file)

# Ana uygulama döngüsü
if __name__ == "__main__":
    import uvicorn
    import json
    
    # PDF dosya yolu
    pdf_path = 'C:/Invoice/fatura3.pdf'
    
    # PDF'den verileri çıkar
    extracted_text, extracted_tables = extract_data_from_pdf(pdf_path)
    
    # JSON olarak kaydet
    data_to_save = {"text": extracted_text, "tables": [table.to_dict() for table in extracted_tables]}
    json_path = 'extracted_data.json'
    save_to_json(data_to_save, json_path)
    
    # FastAPI'yi başlat
    uvicorn.run(app, host="127.0.0.1", port=8001)
