import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from config_loader import load_config, load_gpt_api_config
from translate import translate as translate_service
from utils.common_utils import failure

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

@app.route('/summary', methods=['POST'])
def summarize():
    data = request.get_json()
    if (data is None
            or not isinstance(data, dict)
            or data.get('content') is None):
        return jsonify(failure(code=400, message='Data error'))
    summary_result = summarize_text_once(data['content']) 
    if summary_result.startswith("Error:"):
        return jsonify(failure(code=500, message=summary_result))
    return jsonify({"summary": summary_result})

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    if (data is None
            or not isinstance(data, dict)
            or data.get('prompt') is None
            or data.get('mode') not in ['expand', 'extract']):
        return jsonify(failure(code=400, message='Invalid input data. Ensure "prompt" and "mode" are provided, and "mode" is either "expand" or "extract".'))
    max_words = data.get('max_words', 200)
    if not isinstance(max_words, int) or max_words <= 0:
        return jsonify(failure(code=400, message='"max_words" must be a positive integer.'))
    try:
        result = submit_single_interaction(data['prompt'], data['mode'], max_words)
        return jsonify(success(data=result))
    except Exception as e:
        return jsonify(failure(code=500, message=f"An error occurred: {str(e)}"))

@app.route('/format', methods=['POST'])
def convert_txt_to_docx():
    data = request.get_json()
    if (data is None
            or not isinstance(data, dict)
            or data.get('input_path') is None):
        return jsonify(failure(code=400, message='Missing input_path'))
    input_txt_file = data['input_path']
    if not input_txt_file.lower().endswith('.txt'):
        return jsonify(failure(code=400, message='Only .txt files are supported'))
    try:
        directory = os.path.dirname(input_txt_file)
        base_name = os.path.basename(input_txt_file).replace(".txt", "")
        output_docx_file = os.path.join(directory, f"{base_name}_converted.docx")
        process_file(input_txt_file, output_docx_file)
        return jsonify(success(message='File converted successfully',
                               output_path=output_docx_file))
    except Exception as e:
        return jsonify(failure(code=500, message=f"Conversion error: {str(e)}"))
        
if __name__ == '__main__':
    config_dir = os.path.join('..', 'config')
    server_config_file_name = 'config_server_dev.yaml'
    gpt_api_config_file_name = 'gpt_api_key.yaml'
    server_config = load_config(os.path.join(config_dir, server_config_file_name))
    gpt_api_config = load_gpt_api_config(os.path.join(config_dir, gpt_api_config_file_name))
    if server_config:
        app.run(host=server_config['server']['ip'],
                port=server_config['server']['port'],
                debug=server_config['server']['debug'],
                )
    else:
        app.run(host='127.0.0.1', port=5000, debug=True)
