from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class DeathStar(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(127))

    def __init__(self,name):
        self.name = name




@app.route('/')
def index():
    my_data = DeathStar.query.all()
    return render_template('index.html',names=my_data)

@app.route('/insert',methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        print(name)

    ds = DeathStar(name)
    db.session.add(ds)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        ds = DeathStar.query.get(request.form.get('id'))
        ds.name = request.form['name']

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    ds = DeathStar.query.get(id)
    db.session.delete(ds)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)