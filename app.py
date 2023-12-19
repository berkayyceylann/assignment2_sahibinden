import sqlite3 as sql
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

def init_db():
    conn = sql.connect('database.db')
    print("Opened database successfully")
    conn.execute('''CREATE TABLE IF NOT EXISTS ads 
                 (id INTEGER PRIMARY KEY, 
                 title TEXT, 
                 description TEXT, 
                 price REAL, 
                 city TEXT)''')
    print("Table created successfully")
    conn.close()

@app.route('/')
def home():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from ads")
    ads = cur.fetchall()
    return render_template("home.html", ads=ads)

@app.route('/new_ad')
def new_ad():
    return render_template('new_ad.html')

@app.route('/add_ad', methods=['POST'])
def add_ad():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            price = float(request.form['price'])
            city = request.form['city']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO ads (title, description, price, city) VALUES (?, ?, ?, ?)",
                            (title, description, price, city))
                con.commit()
                msg = "Ad successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"
        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/del_ad/<int:id>', methods=['GET'])
def del_ad(id):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM ads WHERE id = ?", (id,))
            con.commit()
            msg = "Ad successfully deleted"
    except:
        con.rollback()
        msg = "Error in delete operation"
    finally:
        return redirect(url_for('home'))
        con.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


