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
        print(f"DATA: {data}")
        files: list = data['_embedded']['items']
        return render_template('list.html', files=files, public_key=public_key)
    else:
        return f"Error: {response.status_code} - {response.text}"


@app.route('/download/<path:file_path>')
def download_file(file_path: str) -> Union[Response, str]:
    public_key: Union[str, None] = request.args.get('public_key')
    download_url_api: str = app.config['DOWNLOAD_URL']
    params: dict = {'public_key': public_key, 'path': file_path}

    headers: dict = {
        'Authorization': f'OAuth {app.config["OAUTH_TOKEN"]}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    print(f"URL for download: {download_url_api}")
    response = requests.get(download_url_api, headers=headers, params=params)
    print(f"RESPONCE: {response.url }")

    if response.status_code == 200:
        download_url: str = response.json().get('href')

        if not download_url:
            return "Error: Download link not found"

        return redirect(download_url)

    else:
        return f"Error: {response.status_code} - {response.text}"


if __name__ == '__main__':
    app.run(debug=True)
