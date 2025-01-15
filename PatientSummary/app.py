from flask import Flask
from flask import request,jsonify,render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from subprocess import run
import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)
CORS(app)
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/summary', methods=['POST'])
def upload_audio_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        filename = secure_filename(file.filename)
        if file.mimetype == 'audio/wav':
            filename += ".wav"
        file.save(os.path.join(os.getcwd(),'uploads', filename))
        # code to get response from server
        client = Groq()
        filename = "uploads/"+filename
        print("File Name :",filename)
        print("file type :",file.mimetype)
        with open(filename, "rb") as f:
            transcription = client.audio.transcriptions.create(
            file= (filename,f.read()),
            model="whisper-large-v3",
            temperature=0.06,
            prompt= "You are an helpful assistant of a Doctor. Write response like a play script.",
            language="en",
            response_format="verbose_json",
            )
            if transcription.text:
                # create summary for patient
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an helpful assistant. You will be given an script of doctor and patient conversation. Based on the conversation create bullet points for the patient for the disease.Response must be in JSON format."
                        },
                        {
                            "role": "user",
                            "content": transcription.text
                        }
                    ],
                    temperature=1,
                    max_tokens=20240,
                    top_p=1,
                    stream=False,
                    response_format={"type": "json_object"},
                    stop=None,
                )
                return jsonify({"message":transcription.text,"summary":completion.choices[0].message.model_dump()}), 200
                # for chunk in completion:
                #     print(chunk.choices[0].delta.content or "", end="")

            return jsonify({'message': transcription.text}), 200
        return jsonify({'message': 'File uploaded successfully'}), 200

@app.post("/speech_to_text")
def speech_to_text():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        filename = secure_filename(file.filename)
        if file.mimetype == 'audio/wav':
            filename += ".wav"
        file.save(os.path.join(os.getcwd(),'uploads', filename))
        # code to get response from server
        client = Groq()
        filename = "uploads/"+filename
        print("File Name :",filename)
        print("file type :",file.mimetype)
        with open(filename, "rb") as f:
            transcription = client.audio.transcriptions.create(
            file= (filename,f.read()),
            model="whisper-large-v3",
            temperature=0.06,
            prompt= "You are an helpful assistant of a Doctor. Write response like a play script.",
            language="en",
            response_format="verbose_json",
            )
            return jsonify({'message': transcription.text}), 200
        return jsonify({'message': 'File uploaded successfully'}), 200

@app.post("/final_summary")
def summarize():
    context = request.get_json()
    # return context
    if context:
                # create summary for patient
                client = Groq()
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an helpful assistant. You will be given an script of doctor and patient conversation. Based on the conversation create bullet points for the patient for the disease.Response must be in JSON format."
                        },
                        {
                            "role": "user",
                            "content": context.get("context")
                        }
                    ],
                    temperature=1,
                    max_tokens=20240,
                    top_p=1,
                    stream=False,
                    response_format={"type": "json_object"},
                    stop=None,
                )
                return jsonify({"message":context.get("context"),"summary":completion.choices[0].message.model_dump()}), 200
                # for chunk in completion:
                #     print(chunk.choices[0].delta.content or "", end="")
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/encode_audio', methods=['POST'])
def upload_file():
    if 'audioFile' not in request.files:
        return {'error': 'No audio file part'}, 400

    file = request.files['audioFile']

    if file.filename == '':
        return {'error': 'No selected file'}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = f'./uploads/{filename}'
        file.save(filepath)

        # Use FFmpeg for encoding (replace with your preferred library)
        try:
            run(['ffmpeg', '-i', filepath, f'./output/{filename}.webm'], check=True)
            return {'message': 'Encoding successful!'}, 200
        except Exception as e:
            return {'error': f'Encoding failed: {e}'}, 500

    return {'error': 'Invalid file type'}, 400

@app.route('/download/<filename>.webm')
def download_file(filename):
    return send_from_directory('output', f'{filename}.webm')


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8000)