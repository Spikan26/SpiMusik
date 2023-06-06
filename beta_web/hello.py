from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
import spi_VLC

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
log.disabled = True

@app.route("/", methods=['GET'])
def main():
    return redirect(url_for('index'))

@app.route("/index", methods=['GET'])
def index():
    return render_template("index.html", player=player)

@app.route("/volume/<volume_value>")
def volume_web(volume_value):
    player.volume(volumelevel=volume_value)
    return ("nothing")

@app.route("/button", methods=['POST'])
def button():
    if request.form.get('play_button') == 'PLAY':
        print(player.currentTitle)
        player.play()
    elif  request.form.get('next_button') == 'NEXT':
        player.next()
    elif  request.form.get('stop_button') == 'STOP':
        player.stop()
    else:
        pass # unknown
    return redirect(url_for('index'))

@app.route('/get_current_title', methods=['GET'])
def get_current_title():
    # Retrieve the currentTitle value from wherever it is stored
    current_title = player.currentTitle  # Replace this with your actual variable

    # Return the currentTitle value as a JSON response
    return jsonify(current_title)

@app.route('/get_current_duration', methods=['GET'])
def get_current_duration():
    
    current_time_min = (player.mediaPlayer.get_time() // 1000) // 60
    current_time_sec = (player.mediaPlayer.get_time() // 1000) % 60
    total_time_min = player.currentDuration // 60
    total_time_sec = player.currentDuration % 60

    actual_time = f"{current_time_min:02d}:{current_time_sec:02d} / {total_time_min:02d}:{total_time_sec:02d}"

    # Return the currentTitle value as a JSON response
    return jsonify(actual_time)

################################################################

player = spi_VLC.VLC()

if __name__ == "__main__":
    app.run(debug=True)
