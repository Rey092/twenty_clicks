import requests
from faker import Faker
from flask import Flask, render_template

app = Flask(__name__)
fake = Faker()


def generate_fake_users(users_count):
    user_list, email_list = [], []
    for _ in range(users_count):
        user_list.append(fake.name())
        email_list.append(fake.email())
    return list(zip(user_list, email_list))


def generate_fake_passwords(password_len):
    return fake.password(length=password_len, special_chars=False, upper_case=False)


@app.route("/")
@app.route("/<int:clicks>")
def home_page(clicks=20):
    return render_template("home.html", dict={"clicks": clicks})


@app.route("/users/generate/")
@app.route("/users/generate/<int:users_count>")
def users_page(users_count=20):
    users_data = generate_fake_users(users_count)
    return render_template("generate_users.html", users_data=users_data)


@app.route("/password/generate/")
@app.route("/password/generate/<int:password_len>")
def passwords_page(password_len=20):
    password = generate_fake_passwords(password_len)
    return render_template("generate_password.html", password=password)


@app.route("/astro", methods=["GET"])
def starting_url():
    astro = requests.get('http://api.open-notify.org/astros.json')
    astro_json = astro.json()
    people_dict = astro_json.get("people")  # {'craft': 'ISS', 'name': 'Sergey Ryoko'}, ...
    astro_number = astro_json.get("number")
    return render_template("astro.html", people_dict=people_dict, astro_number=astro_number)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
