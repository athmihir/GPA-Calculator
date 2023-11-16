import pandas as pd

# This is used for US GPA points calculation
grade_to_gpa = {
    'O': 4.0,
    'A+': 4.0,
    'A': 3.5,
    'B+': 3.0,
    'B': 2.5,
    'C': 2.0,
    'P': 2.0,
    'S': 0.0,
    'F': 0.0,
}

# This is used for determining CGPA points
grade_to_points = {
    'O': 10.0,
    'A+': 9.0,
    'A': 8.0,
    'B+': 7.0,
    'B': 6.0,
    'C': 5.0,
    'P': 4.0,
    'S': 0.0,
    'F': 0.0,
}

data = pd.read_csv('gpa.csv')
#Ensure rows are sorted by semester.
data = data.sort_values(by=['Semester'], ascending=True)

currsem = 1
total_credits = 0
total_sem_credits = 0
# Each credit in the cgpa system corresponds to 10 points.
cgpa = {'points':0, 'sem_points':0, 'year_points':0}
# Each credit in the gpa system corresponds to 4 points.
gpa = {'points':0, 'sem_points':0, 'year_points':0}


for index, row in data.iterrows():
    subject_credits = row['Total Credits']
    # We ignore subjects which hold no credit value.
    if subject_credits == 0:
        continue
    grade = row['Grade']
    cgpa_points = grade_to_points[grade] * subject_credits
    gpa_points = grade_to_gpa[grade] * subject_credits
    # Updating total points for all years.
    cgpa['points'] += cgpa_points
    gpa['points'] += gpa_points
    total_credits += subject_credits
    # Updating total points for per sem basis.
    if (currsem == row['Semester']):
        cgpa['sem_points'] += cgpa_points
        gpa['sem_points'] += gpa_points
        total_sem_credits += subject_credits
    else:
        # The semester has changed, so lets print what we have
        print(f'''Sem:{currsem}, CGPA: {round(cgpa['sem_points'] / total_sem_credits, 3)}, GPA: {round(gpa['sem_points'] / total_sem_credits, 3)}''')
        # Reinitialize semester level dicts
        currsem = row['Semester']
        cgpa['year_points'] += round(cgpa['sem_points'] / total_sem_credits, 2)
        gpa['year_points'] += round(gpa['sem_points'] / total_sem_credits, 2)
        cgpa['sem_points'] = cgpa_points
        gpa['sem_points'] = gpa_points
        
        total_sem_credits = subject_credits
        # Check if year has changed as well
        if currsem % 2 == 1:
            print(f'''Year:{int(currsem/2)}, CGPA: {round(cgpa['year_points'] / 2, 3)}, GPA: {round(gpa['year_points'] / 2, 3)}''')
            print("---------------------------------------")
            cgpa['year_points'] = 0
            gpa['year_points'] = 0

print(f'''Sem:{currsem}, CGPA: {round(cgpa['sem_points'] / total_sem_credits, 3)}, GPA: {round(gpa['sem_points'] / total_sem_credits, 3)}''')
cgpa['year_points'] += round(cgpa['sem_points'] / total_sem_credits, 2)
gpa['year_points'] += round(gpa['sem_points'] / total_sem_credits, 2)
print(f'''Year:{int(currsem/2)}, CGPA: {round(cgpa['year_points'] / 2, 3)}, GPA: {round(gpa['year_points'] / 2, 3)}''')
print("---------------------------------------")
print(f'''Final CGPA: {round(cgpa['points'] / total_credits, 3)}, Final GPA: {round(gpa['points'] / total_credits, 3)}''')
