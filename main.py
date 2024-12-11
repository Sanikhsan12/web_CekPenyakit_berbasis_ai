# library
import flask
from flask import request , render_template 
from groq import Groq as gq

# ! inisiasi app
app = flask.Flask(__name__, template_folder='view')

# ! API Key
key = "your-api-key"
client = gq(api_key=key)

def chat_bot(gejala):
    try:
        chat = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"saya merasa {gejala}, kira-kira sakit apa saya?"
                }
            ],
            model="llama-3.2-1b-preview",
            stream=False
        )

        chat_output = chat.choices[0].message.content
        return chat_output
    except Exception as e:
        return "sedang maintainance, coba lagi nanti"
# ! Routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kesehatan', methods=['GET', 'POST'])
def kesehatan():
    if request.method == 'POST':
        # ? ambil data dari form
        gejala = str(request.form['gejala'])

        # ? AI Call
        chat_output = chat_bot(gejala)
        return render_template('ai.html', data=chat_output)
    return render_template('ai.html', data=None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
