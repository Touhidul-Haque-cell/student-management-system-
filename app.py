import sqlite3
import csv

DB = 'students.db'

def setup():
    with sqlite3.connect(DB) as con:
        con.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, department TEXT NOT NULL, email TEXT UNIQUE NOT NULL, cgpa REAL)')

def add():
    name = input('Name: ').strip()
    department = input('Department: ').strip()
    email = input('Email: ').strip()
    if not name or not department or '@' not in email:
        print('Invalid information.'); return
    try:
        cgpa = float(input('CGPA (0-4): '))
        if not 0 <= cgpa <= 4: raise ValueError
        with sqlite3.connect(DB) as con:
            con.execute('INSERT INTO students (name,department,email,cgpa) VALUES (?,?,?,?)',(name,department,email,cgpa))
        print('Student added!')
    except (ValueError, sqlite3.IntegrityError) as e:
        print('Could not add student:', e)

def view(search=''):
    with sqlite3.connect(DB) as con:
        rows = con.execute('SELECT * FROM students WHERE name LIKE ? OR department LIKE ? ORDER BY id',('%'+search+'%','%'+search+'%')).fetchall()
    for row in rows: print(f'ID: {row[0]} | Name: {row[1]} | Department: {row[2]} | Email: {row[3]} | CGPA: {row[4]}')
    if not rows: print('No students found.')

def update():
    try:
        sid = int(input('Student ID: ')); name = input('New name: ').strip()
        if not name: print('Name required.'); return
        with sqlite3.connect(DB) as con:
            result = con.execute('UPDATE students SET name=? WHERE id=?',(name,sid))
        print('Updated.' if result.rowcount else 'Not found.')
    except ValueError: print('Invalid ID.')

def delete():
    try:
        sid = int(input('Student ID: '))
        with sqlite3.connect(DB) as con:
            result = con.execute('DELETE FROM students WHERE id=?',(sid,))
        print('Deleted.' if result.rowcount else 'Not found.')
    except ValueError: print('Invalid ID.')

def export():
    with sqlite3.connect(DB) as con:
        rows=con.execute('SELECT * FROM students ORDER BY id').fetchall()
    with open('students_export.csv','w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f);writer.writerow(['ID','Name','Department','Email','CGPA']);writer.writerows(rows)
    print('Saved students_export.csv')

def main():
    setup()
    while True:
        print('\n=== STUDENT MANAGEMENT SYSTEM ===\n1. Add Student\n2. View All\n3. Search\n4. Update Name\n5. Delete\n6. Export CSV\n0. Exit')
        choice=input('Choose: ').strip()
        if choice=='1': add()
        elif choice=='2': view()
        elif choice=='3': view(input('Search name/department: '))
        elif choice=='4': update()
        elif choice=='5': delete()
        elif choice=='6': export()
        elif choice=='0': break
        else: print('Invalid choice.')

if __name__=='__main__': main()
