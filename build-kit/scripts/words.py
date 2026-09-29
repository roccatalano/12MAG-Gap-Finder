import subprocess,re,json,os,sys
from xml.etree import ElementTree as ET
B="/mnt/user-data/outputs/org/02 Past Exams/"
PDF={"2023 VCAA E1":"2023/2023 - Exam 1.pdf","2023 VCAA E2":"2023/2023 - Exam 2.pdf","2024 VCAA E1":"2024/2024 - Exam 1.pdf","2024 VCAA E2":"2024/2024 - Exam 2.pdf",
"2025 VCAA E1":"2025/2025 - Exam 1.pdf","2025 VCAA E2":"2025/2025 - Exam 2.pdf","2024 NHT E1":"2024 NHT/2024 NHT - Exam 1.pdf","2024 NHT E2":"2024 NHT/2024 NHT - Exam 2.pdf",
"2025 NHT E1":"2025 NHT/2025 NHT - Exam 1.pdf","2025 NHT E2":"2025 NHT/2025 NHT - Exam 2.pdf","2026 NHT E1":"2026 NHT/2026 NHT - Exam 1.pdf","2026 NHT E2":"2026 NHT/2026 NHT - Exam 2.pdf",
"VCAA Sample E1":"VCAA Sample (current study design)/Sample - Exam 1.pdf","VCAA Sample E2":"VCAA Sample (current study design)/Sample - Exam 2.pdf"}
SCAN={"2024 VCAA E1","2024 VCAA E2","2025 NHT E1","2025 NHT E2"}
def text_words(path):
    import html
    out=subprocess.run(['pdftotext','-bbox',path,'-'],capture_output=True,text=True).stdout
    W=[];pi=0;w=h=1
    for line in out.split('\n'):
        m=re.search(r'<page width="([\d.]+)" height="([\d.]+)"',line)
        if m: pi+=1; w,h=float(m.group(1)),float(m.group(2)); continue
        m=re.search(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*)</word>',line)
        if m: W.append((pi,float(m.group(1))/w,float(m.group(2))/h,float(m.group(3))/w,float(m.group(4))/h,html.unescape(m.group(5))))
    return W
def ocr_words(path,key):
    d=f'/tmp/w/ocrw/{key.replace(" ","_")}'; os.makedirs(d,exist_ok=True)
    subprocess.run(['pdftoppm','-r','150','-gray',path,d+'/p'])
    W=[]
    for f in sorted(os.listdir(d)):
        if not f.endswith('.pgm'): continue
        pi=int(re.findall(r'\d+',f)[-1])
        tsv=subprocess.run(['tesseract',d+'/'+f,'-','tsv'],capture_output=True,text=True).stdout.split('\n')[1:]
        from PIL import Image; im=Image.open(d+'/'+f); w,h=im.size
        for l in tsv:
            c=l.split('\t')
            if len(c)<12 or not c[11].strip(): continue
            x,y,ww,hh=map(int,c[6:10]); W.append((pi,x/w,y/h,(x+ww)/w,(y+hh)/h,c[11]))
    return W
if __name__=='__main__':
  key=sys.argv[1]; p=B+PDF[key]
  W=ocr_words(p,key) if key in SCAN else text_words(p)
  json.dump(W,open(f'/tmp/w/ocrw/{key.replace(" ","_")}.json','w'))
  print(key,len(W))
