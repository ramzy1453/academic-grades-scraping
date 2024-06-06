from PyPDF2 import PdfReader
import pandas as pd


reader = PdfReader('./Deliberation_annuel-L3-ACAD.pdf')

columns = ['full_name', 'matricule', 'section', 'moyS1', 'credS1', 'moyS2', 'credS2', 'annuel', 'cred_annuel', 'admis']
len(columns)

def find_section(n_page, page):
    i1 = page.find('Section')
    section1 = page[i1+9]

    if n_page == 0:
        return section1, True
    
    previous_page = reader.pages[n_page-1].extract_text()
    i2 = previous_page.find('Section')
    
    section2 = previous_page[i2+9]

    return section1, section1 != section2

def validate_student(fullname, n, matricule, moyS1, credS1, moyS2, credS2, annuel, cred_annuel, state, section):
    return fullname, matricule, section, float(moyS1), int(credS1), float(moyS2), int(credS2), float(annuel), int(cred_annuel), state == 'Admis(e)'

def extract_students(n_page):
    page = reader.pages[n_page].extract_text()
    students = []
    section, is_section_start = find_section(n_page, page)
    if is_section_start:
        i = 0

    for student in page.split('\n'):
        if not student.startswith('    '):
            continue

        student = student.strip().split(' ')
        fullname_end = 0
        for attr in student:
            if not str(attr).isnumeric():
                fullname_end += 1
            else:
                break
        
        student = [' '.join(student[:fullname_end]).lower()] + student[fullname_end:]
        
        if is_section_start:
            if i < 9:
                student = [student[0]] + [student[1][0], student[1][1:]] + student[2:]
            i += 1
        
        student = student[:len(columns)]
        
        student = validate_student(*student, section)
        
        students.append(student)


    return students

all_students = []
for i in range(len(reader.pages)):
    print(i)
    all_students += extract_students(i)

    
df = pd.DataFrame(all_students, columns=columns)
df.to_csv('deliberation_l3_acad.csv', index=False)