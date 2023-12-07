def get_rows(spreadsheet):
    sheet = spreadsheet.sheet1
    return sheet.get_all_values()

def get_questions(rows):
    questions = []
    for row in rows:
        questions.append(row[0].lower())
    return questions

def get_answers(rows):
    answers = []
    for row in rows:
        answers.append(row[1])
    return answers