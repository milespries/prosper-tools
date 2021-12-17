from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=["GET", "POST"])
def form():
    
    if request.method == "POST":

        amount_borrowed = request.form["textinput-0"]
        yeild = request.form["textinput-1"]
        rating = request.form["selectbasic-0"]
        term = request.form["selectbasic-1"]
        if int(yeild) <= 100 and int(yeild) > 0:
            yeild = float(int(yeild)) / 100
            if term == "3 Years":
                term = 36
            elif term == "5 Years":
                term = 60
            scanned = scan(amount_borrowed, yeild, rating, term)
            return redirect(url_for('get_result', value = scanned[0], value2 = scanned[1], value3 = scanned[2]))

    return render_template('form.html')

@app.route('/result/<value>/<value2>/<value3>')
def get_result(value, value2, value3):
    return render_template('result.html', percent=value, total_match=value2, total=value3)

def scan(_amount, _yeild, _rating, _term):
    total = 0
    total_loans = 0
    total_completed = 0
    total_defaulted = 0
    amount_borrowed = _amount
    amount_borrowed_plus = int(amount_borrowed) + 2000
    amount_borrowed_minus = int(amount_borrowed) - 2000
    borrower_rate = _yeild
    borrower_rate_plus = float(borrower_rate) + 0.02
    borrower_rate_minus = float(borrower_rate) - 0.02
    prosper_rating = _rating
    term = _term
    with open("all_loans.csv", "r") as f:
        csvreader = csv.reader(f, delimiter=",")
        next(csvreader)
        for row in csvreader:
            if row[16] == "COMPLETED" or row[16] == "DEFAULTED" or row[16] == "CHARGEOFF":
                total_loans+=1
                if int(round(float(row[1]))) >= amount_borrowed_minus and int(round(float(row[1]))) <= amount_borrowed_plus:
                    if float(row[2]) >= float(borrower_rate_minus) and float(row[2]) <= float(borrower_rate_plus):
                        if row[3] == prosper_rating:
                            if row[4] == str(term):
                                if row[16] == "COMPLETED":
                                    total+=1
                                    total_completed+=1
                                elif row[16] == "DEFAULTED" or row[16] == "CHARGEOFF":
                                    total+=1
                                    total_defaulted+=1
    if total > 0:
        percent_complete = round(total_completed/total * 100, 2)
        return [percent_complete, total, total_loans]
    else:
        return 0