from flask import Flask, render_template, jsonify, request
import chatbot


app = Flask(__name__)

app.config['SECRET_KEY'] = 'miClaveEsMuySecretaParaQueTeLaSepasñoño@'


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('Clean_chat_box.html', **locals())



@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():

    if request.method == 'POST':
        the_question = request.form['question']
        try:
            response = chatbot.get_response(the_question)
        except:
            print('-------')
        

    return jsonify({"response": response })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8890', debug=True)
