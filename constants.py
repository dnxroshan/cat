

class UserType:
    Admin = 0
    Examiner = 1
    Candidate = 2

class Difficulty:
    Easy = 'E'
    Medium = 'M'
    Hard = 'H'

class Options:
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'

STANDARDS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '+1', '+2']

SUBJECTS = [
    'Mathematics',
    'Physics',
    'Chemistry',
    'Botony',
    'Zoology',
    'Computer Science',
    'English',
    'History',
    'Geography'
]

def choices():
    choice_list = list(zip(SUBJECTS, SUBJECTS))
    choice_list.insert(0, ('All', 'All'))
    return choice_list
