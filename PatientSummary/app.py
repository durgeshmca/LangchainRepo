from flask import Flask
from flask import request,jsonify,render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from subprocess import run
import json
import os
from dotenv import load_dotenv
from groq import Groq
from pydub import AudioSegment
import math

load_dotenv()

app = Flask(__name__)
CORS(app)
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def split_audio(file_path, segment_length=10*60*1000):  # 29 minutes in milliseconds
    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    
    # Get the total length of the audio file
    total_length = len(audio)
    
    # Calculate the number of segments needed
    num_segments = math.ceil(total_length / segment_length)

    # Loop through and create each segment
    for i in range(num_segments):
        start_time = i * segment_length
        end_time = min((i + 1) * segment_length, total_length)  # Ensure the last segment does not exceed total length
        segment = audio[start_time:end_time]

        # Generate the output file name
        output_file = f"{file_path[:-4]}_part{i+1}.mp3"
        
        # Export the segment as an MP3 file
        segment.export(output_file, format="mp3")
        print(f"Exported: {output_file}")

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
            prompt= "You are an helpful assistant.You will be given a conversation script. Language of conversation may be in Hindi or English or both. Write response like a play script.",
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
                data = completion.choices[0].message.model_dump_json()
                data_dict = json.loads(data)
                content_dict = json.loads(data_dict['content'])
                return jsonify({"message":context.get("context"),"summary":content_dict}), 200
                # for chunk in completion:
                #     print(chunk.choices[0].delta.content or "", end="")

@app.post("/meeting_summary")
def summarize_meeting():
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
                            "content": "You are an helpful assistant. You will be given an script of meeting conversation. Based on the conversation create bullet points.Response must be in JSON format and it must contain only two key named `title` and `content`. Value of content must be a text based summary."
                        },
                        {
                            "role": "user",
                            "content": context.get("context")
                        }
                    ],
                    temperature=0.5,
                    max_tokens=20240,
                    top_p=1,
                    stream=False,
                    response_format={"type": "json_object"},
                    stop=None,
                )
                data = completion.choices[0].message.model_dump_json()
                data_dict = json.loads(data)
                content_dict = json.loads(data_dict['content'])

                return jsonify({"message":context.get("context"),"summary":content_dict}), 200
                # for chunk in completion:
                #     print(chunk.choices[0].delta.content or "", end="")
@app.post("/extract_values")
def extract_data():
    data_to_extract = '''
    name
    age
    gender
    occupation
    status
    religion
    mother_tongue
    address
    phone
    way_of_sitting
    expressions
    complaint_start
    initial_symptoms
    onset
    complaint_side
    cross_wise_affections
    pain_duration
    modalities
    probable_diagnosis
    major_illnesses
    predominant
    journey_of_disease
    hereditary_illnesses
    menses_details
    menarche
    menopause
    abortions
    medications
    drug_allergies
    investigations
    built
    body_structure
    face
    hairs
    complexion
    warts_moles
    frown
    discolouration
    appetite
    drinks
    cravings_aversion
    food_drink_agg_amel
    thirst
    perspiration
    stools
    urine
    thermals
    sleep
    dreams
    speed
    side
    gen_sensitivity
    senses
    habits
    living_situation
    education
    expressiveness
    intellect
    conscientiousness
    morals
    memory
    will
    reaction_in_crisis
    nature_disposition
    emotional_reactions
    anger_behavior
    sensitivity
    emotional_sensitivity
    anticipation_Apprehension
    fears
    childhood_history
    infants_to_toddlers
    school_going_children
    college_students
    middle_age
    old_age
    summary
'''

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
                            "content": '''You are an expert in data parsing. You will be given an script of meeting conversation. Based on the conversation try to extract following information.''' + data_to_extract + '''
                            Prepare a JSON object with the key above and values as extracted values. Response must be in JSON format only.
                            '''
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
                data = completion.choices[0].message.model_dump_json()
                data_dict = json.loads(data)
                content_dict = json.loads(data_dict['content'])

                return jsonify({"context":context.get("context"),"data":content_dict}), 200
                # for chunk in completion:
                #     print(chunk.choices[0].delta.content or "", end="")
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.post("/form_values")
def get_form_data():
    
    extraction_list = request.form.get('extract_values_for').split(",")
    # print(extraction_list)
    # extraction_list = json_data['extract_values_for']
    data_to_extract = ', '.join(extraction_list)
    # print(data_to_extract)
    # return {'x':data_to_extract}
    # return context
    text_data,response_code = speech_to_text()
    # print(text_data.get_json())
    context = text_data.get_json().get('message')
    # return {'hi','hello'}
    # context = text_data.get('message')
    if context:
                # create summary for patient
                client = Groq()
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": '''You are an expert in data parsing. You will be given an script of meeting conversation. Based on the conversation try to extract following information.''' + data_to_extract + '''
                            Prepare a JSON object with the key above and values as extracted values. Response must be in JSON format only.
                            '''
                        },
                        {
                            "role": "user",
                            "content": context
                        }
                    ],
                    temperature=1,
                    max_tokens=20240,
                    top_p=1,
                    stream=False,
                    response_format={"type": "json_object"},
                    stop=None,
                )
                data = completion.choices[0].message.model_dump_json()
                data_dict = json.loads(data)
                content_dict = json.loads(data_dict['content'])

                return jsonify({"context":context,"data":content_dict}), 200
                


if __name__ == '__main__':
    # split_audio("uploads/audio1516611971.m4a")
    app.run(debug=True,host="0.0.0.0",port=8000)