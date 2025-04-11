import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from config_loader import load_config, load_gpt_api_config, update_env_config
from utils.common_utils import is_empty, failure
from translate import translate as translate_service
from tone import text_with_style as tone_service
from process_text import submit_single_interaction as process_service
from summary import summarize_text_once as summary_service
from format_setting import submit_to_llm, format_to_docx
from role import analyze_text_features, rewrite

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)


@app.route('/')
def hello():
    return 'hi'


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if (data is None
            or not isinstance(data, dict)
            or data.get('content') is None
            or data.get('target_lang') is None):
        return jsonify(failure(code=400, message='Data error'))
    obj = translate_service(data['content'], data['target_lang'], gpt_api_config)
    return jsonify(obj)


@app.route('/tone', methods=['POST'])
def tone():
    data = request.get_json()
    if (data is None
            or not isinstance(data, dict)
            or data.get('text') is None
            or data.get('style') is None):
        return jsonify(failure(code=400, message='Data error'))

    text = data['text'].strip()
    style = data['style'].strip()

    if not text:
        return failure(code=400, message='Please type your text')
    if not style:
        return failure(code=400, message='Please select the language style you want')

    obj = tone_service(text, style, gpt_api_config)
    return jsonify(obj)


@app.route('/summary', methods=['POST'])
def summary():
    data = request.get_json()
    if (data is None
            or not isinstance(data, dict)
            or data.get('prompt') is None):
        return jsonify(failure(code=400, message='Data error'))
    obj = summary_service(data['prompt'], gpt_api_config)
    return jsonify(obj)


@app.route('/process-text', methods=['POST'])
def process_text():
    data = request.get_json()
    if (data is None
            or not isinstance(data, dict)
            or data.get('prompt') is None
            or data.get('mode') not in ['expand', 'extract']
            or data.get('max_word') is None):
        return jsonify(failure(code=400, message='Data error'))
    obj = process_service(data['prompt'], data['mode'], data['max_word'], gpt_api_config)
    return jsonify(obj)


@app.route('/format-text', methods=['POST'])
def format_text():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.txt'):
        return jsonify(failure(code=400, message='File error'))

    try:
        file_text = file.read().decode('utf-8')
        if is_empty(file_text):
            return jsonify(failure(code=400, message='File error'))
    except UnicodeDecodeError:
        return jsonify(failure(code=400, message='File must be UTF-8 encoded'))

    response_obj = submit_to_llm(file_text, gpt_api_config)
    if not response_obj['success']:
        return jsonify(failure(code=response_obj['code'], message=response_obj['message']))

    file_stream = format_to_docx(response_obj['data'])

    return send_file(
        file_stream,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name='converted_output.docx',
    )


@app.route('/role', methods=['POST'])
def role():
    content = request.form.get('content')
    if is_empty(content):
        return jsonify(failure(code=400, message='Data error'))

    file = request.files.get('file')
    if not file or not file.filename.endswith('.txt'):
        return jsonify(failure(code=400, message='File error'))

    try:
        file_text = file.read().decode('utf-8')
        if is_empty(file_text):
            return jsonify(failure(code=400, message='File error'))
    except UnicodeDecodeError:
        return jsonify(failure(code=400, message='File must be UTF-8 encoded'))

    response_obj = analyze_text_features(file_text, gpt_api_config)
    if not response_obj['success']:
        return jsonify(failure(code=response_obj['code'], message=response_obj['message']))

    obj = rewrite(content, response_obj['data'], gpt_api_config)
    return jsonify(obj)


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    config_dir = os.path.join(base_dir, '..', 'config')
    server_config_file_name = 'config_server_dev.yaml'
    gpt_api_config_file_name = 'gpt_api_key.yaml'
    server_config = load_config(os.path.join(config_dir, server_config_file_name))
    gpt_api_config = load_gpt_api_config(os.path.join(config_dir, gpt_api_config_file_name))
    update_env_config(server_config, gpt_api_config)
    if server_config:
        app.run(host=server_config['server']['ip'],
                port=server_config['server']['port'],
                debug=server_config['server']['debug'],
                )
    else:
        app.run(host='127.0.0.1', port=5000, debug=True)
