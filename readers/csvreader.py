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


def csvtodict(csv_file_path):
    pairs = []

    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cleaned_row = {k: clean_text(v) for k, v in row.items()}
            # data.append([k + clean_text(v) for k, v in row.items()])
            pairs.append(cleaned_row)
    
    return pairs

def getcsvdata(csv_file_path):
    pairs = csvtodict(csv_file_path)
    data = []
    for p in pairs:
        txt = ''
        for val in p.values():
            txt+= val + ' '
        data.append(txt.strip())
    return data


# data = getcsvdata('data\\policy.csv')
# print(data[:3])
# for i in data[:3]:
#     print(i,end='\n\n')

