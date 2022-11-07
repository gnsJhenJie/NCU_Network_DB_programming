import re
import sqlite3 as lite
from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route('/score', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        con = lite.connect('./dbtest.db')
        with con:
            cur = con.cursor()
            cur.execute(
                f"SELECT * FROM ENROLLMENT inner join COURSE on ENROLLMENT.CID = COURSE.CID  WHERE SID='{request.values['SID']}';")
            rows = cur.fetchall()
            print(rows)
        # return request.form.get('username', '')+';'+request.form.get('email', '')
        # request.values["SID"]

        return render_template('score.html', hasScore=True, SID=request.values["SID"], rows=rows)
        # return register_action()
    else:

        return render_template('score.html', hasScore=False)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002, debug=True)
