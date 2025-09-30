from datetime import datetime, timedelta
import requests
import subprocess
import os
from PyPDF2 import PdfReader  # pip install PyPDF2

s_date = datetime(2020, 1, 1)
e_date = datetime(2021, 12, 31)

content_file = "pdf_contents.txt"
creator_file = "creators.txt"

with open(content_file, "w", encoding="utf-8") as content_out, \
     open(creator_file, "w", encoding="utf-8") as creator_out:

    while s_date <= e_date:
        url = s_date.strftime("http://10.10.10.248/documents/%Y-%m-%d-upload.pdf")
        resp = requests.get(url, timeout=10)
        
        if resp.status_code == 200:
            print("[200] Bulundu:", url)

            # PDF'i geçici olarak kaydet
            temp_file = "temp.pdf"
            with open(temp_file, "wb") as f:
                f.write(resp.content)

            # Exiftool ile Creator bilgisini al
            result = subprocess.run(
                ["exiftool", "-Creator", temp_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            creator = None
            for line in result.stdout.splitlines():
                if line.startswith("Creator"):
                    creator = line.split(":", 1)[1].strip()
                    break

            # Creator bilgisini ayrı dosyaya yaz
            if creator:
                creator_out.write(f"{url} -> {creator}\n")
                print(f"    Creator: {creator}")
            else:
                creator_out.write(f"{url} -> Bulunamadı\n")

            # PDF içeriğini oku ve içerik dosyasına yaz
            try:
                reader = PdfReader(temp_file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                content_out.write(f"URL: {url}\n")
                content_out.write("İçerik:\n")
                content_out.write(text + "\n")
                content_out.write("-" * 50 + "\n")  # Ayırıcı
            except Exception as e:
                content_out.write(f"URL: {url}\nİçerik okunamadı: {e}\n")
                content_out.write("-" * 50 + "\n")

            # geçici dosyayı sil
            os.remove(temp_file)

        # bir gün ileri
        s_date += timedelta(days=1)

print(f"Tüm PDF içerikleri '{content_file}' dosyasına, Creator bilgileri '{creator_file}' dosyasına yazıldı.")

