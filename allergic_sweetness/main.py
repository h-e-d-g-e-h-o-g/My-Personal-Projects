from flask import Flask, render_template
import data

app = Flask(__name__)

awareness_needs = ["Prevention and Early Detection", "Promoting Healthy Lifestyles", "Reducing Stigma"]
awareness_images = ["static/images/Diabetes-check-up.jpg", "static/images/health-diabetes.jpg", "static/images/diabetes-stigma.jpg"]

question_images = ['static/images/faq-1.jpg', 'static/images/faq-2.jpg', 'static/images/faq-3.jpg', 'static/images/faq-4.jpeg']
response_data = data.faq_list

@app.route("/")
def home():
    return render_template("index.html", needs=awareness_needs, images=awareness_images)

@app.route("/faq")
def info():
    return render_template("faq.html", questions=response_data)

@app.route("/question/<int:question_id>")
def receive_info(question_id):
    question_title = response_data[question_id-1]['question']
    question_subheading = response_data[question_id-1]['subheading']
    question_answer = response_data[question_id-1]['answer']
    question_image = response_data[question_id-1]['image']
    return render_template("answer.html", title=question_title, subheading=question_subheading, answer=question_answer, image=question_image)

@app.route("/support")
def precautions():
    return render_template("support.html")

if __name__ == "__main__":
    app.run(debug=True)