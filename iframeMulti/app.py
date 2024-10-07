from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live', methods=['GET', 'POST'])
def live():
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        camera_id = request.form.get('camera_id')
    else:  # This will handle GET requests
        access_token = request.args.get('access_token')
        camera_id = request.args.get('camera_id')
    return render_template('live.html', access_token=access_token, camera_id=camera_id)

@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        camera_id = request.form.get('camera_id')
    else:  # This will handle GET requests
        access_token = request.args.get('access_token')
        camera_id = request.args.get('camera_id')
    return render_template('history.html', access_token=access_token, camera_id=camera_id)

@app.route('/historylive', methods=['GET', 'POST'])
def historylive():
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        camera_id = request.form.get('camera_id')
    else:  # This will handle GET requests
        access_token = request.args.get('access_token')
        camera_id = request.args.get('camera_id')
    return render_template('historylive.html', access_token=access_token, camera_id=camera_id)

if __name__ == '__main__':
    app.run(debug=True, port=3333)
