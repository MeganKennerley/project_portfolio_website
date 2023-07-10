from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"
bootstrap = Bootstrap5(app)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-projects.db"
db.init_app(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    github = db.Column(db.String, nullable=False)


# with app.app_context():
#     db.create_all()


class AddProject(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    image = StringField("Image", validators=[DataRequired()])
    github = StringField("Github Link", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/projects')
def projects():
    rows = db.session.query(Project)
    return render_template("projects.html", rows=rows)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddProject()
    if request.method == "POST":
        new_project = Project(title=request.form.get("title"), description=request.form.get("description"),
                              image=request.form.get("image"), github=request.form.get("github"))
        with app.app_context():
            db.session.add(new_project)
            db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)