from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
from colorthief import ColorThief

UPLOAD_FOLDER = "static/uploads/"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
Bootstrap(app)

numbers = []
for i in range(3, 21):
    numbers.append(i)


class UploadImage(FlaskForm):
    file = FileField(label="Upload Image", validators=[FileRequired(), FileAllowed(["jpg", "png"], "Images Only!")])
    num_colors = SelectField(label="Number of Colors to Extract", choices=numbers, validators=[DataRequired()])
    submit = SubmitField(label="Submit")


@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadImage()
    if form.validate_on_submit():
        file = form.file.data
        num_colors = int(form.num_colors.data)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        color_thief = ColorThief(file_path)
        palette = color_thief.get_palette(color_count=num_colors)
        hex_codes = ['#%02x%02x%02x' % color for color in palette]

        return render_template("home_page.html", form=form, image=filename, hex_codes=hex_codes)
    return render_template("home_page.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
