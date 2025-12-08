import os
import csv

def clean_text(s):
    if not s:
        return ""
    #unicode cleanup
    try:
        s = s.encode("latin1").decode("utf-8")
    except:
        pass

    return " ".join(s.split())

def getcsvdata(csv_file_path):
    data = []

    # filename without extension
    base = os.path.splitext(os.path.basename(csv_file_path))[0]

    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for idx, row in enumerate(reader, start=1):
            # Clean all values
            cleaned_values = [clean_text(v) for v in row.values()]
            # print(cleaned_values)

            # Combine into one text string
            if 'faq' in base:
                text = cleaned_values[1].strip()
                metadata = cleaned_values[0].strip()
                entry = {
                    "_id": f"{base}_{idx}",
                    "text": text,
                    "metadata": metadata
                }
                
            else:
                text = " ".join(cleaned_values).strip()
                entry = {
                    "_id": f"{base}_{idx}",
                    "text": text
                }
            data.append(entry)

    return data



# data = getcsvdata('data\\faqs.csv')
# # print(data[:3])
# for i in data[:3]:
#     print(i,end='\n\n')

