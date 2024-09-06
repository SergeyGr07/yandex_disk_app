from flask import Flask, render_template, request, redirect, Response
import requests
from config import Config
from typing import Union

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def index() -> Union[str, Response]:
    if request.method == 'POST':
        public_key: str = request.form['public_key']
        return redirect(f'/list?public_key={public_key}')
    return render_template('index.html')


@app.route('/list')
def list_files() -> Union[str, Response]:
    public_key: Union[str, None] = request.args.get('public_key')
    url: str = app.config['YANDEX_DISK_API_URL']
    params: dict = {'public_key': public_key}

    headers: dict = {
        'Authorization': f'OAuth {app.config["OAUTH_TOKEN"]}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response: requests.Response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data: dict = response.json()
        files: list = data['_embedded']['items']
        return render_template('list.html', files=files, public_key=public_key)
    else:
        return f"Error: {response.status_code} - {response.text}"


@app.route('/download')
def download_file() -> Response:
    file_url = request.args.get('file_url')

    if file_url:
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            filename = file_url.split('/')[-1]
            return Response(
                response.iter_content(chunk_size=1024),
                content_type=content_type,
                headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            )
        else:
            return f"Error: {response.status_code} - {response.text}"
    else:
        return "Error: No file URL provided."


if __name__ == '__main__':
    app.run(debug=True)
