import socket

from flask import Flask, render_template, request

import ledvis.lightController as lightController

app = Flask(__name__)

arduino = None

currLevel = 0.4
currColor = ""
currAnim = ""
currPal = ""
lcObject = lightController


@app.route("/")
def home():
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/brightness/", methods=['POST'])
def brightness():
    global lcObject

    btn_name = get_btn_name(request)
    lcObject.messageReceived(identifier=int(btn_name))
    print ("Brightness:", btn_name )
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/duration/", methods=['POST'])
def duration():
    duration = request.form['duration']
    print ("Duration:", duration)
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/color/", methods=['POST'])
def color():
    global lcObject
    btn_name = get_btn_name(request)
    lcObject.messageReceived(identifier=int(btn_name))
    print ("Color:", btn_name )
    
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/palette/", methods=['POST'])
def palette():
    global currLevel
    global currColor
    global currAnim
    global currPal

    btn_name = get_btn_name(request)
    print ("Palette:", btn_name)
    
    templateData = {}
    return render_template('main.html', **templateData);

@app.route("/anim/", methods=['POST'])
def anim():
    global lcObject

    btn_name = get_btn_name(request)
    lcObject.messageReceived(identifier=int(btn_name))
    print ("Animation code:", btn_name)
    templateData = {}
    return render_template('main.html', **templateData);


@app.route("/pal/", methods=['POST'])
def pal():
    global currLevel
    global currColor
    global currAnim
    global currPal

    if 'btnRgb' in request.form:
        currPal = "RGB";
    elif 'btnRainbow' in request.form:
        currPal = "Rainbow";
    elif 'btnParty' in request.form:
        currPal = "Party";
    elif 'btnFire' in request.form:
        currPal = "Fire";
    
    templateData = {
      'currAnim': currAnim,
      'currPal': currPal,
      'currLevel': currLevel,
      'currColor': currColor
    };

    return render_template('main.html', **templateData);


def get_btn_name(request):
    btn_name=""
    for key in request.form.keys():
        #print ("Button pressed:", key)
        btn_name = key
    return btn_name


# def arduino_get_resp(s):
#     time.sleep(.1);
#     while (s.in_waiting > 0):
#         print(s.readline().decode(), end="");
#
# # try to detect the USB port where Arduino is connected
# def arduino_get_port():
#     print("Listing ports")
#     port = None
#     ports = serial.tools.list_ports.comports()
#     for p in ports:
#         print(p)
#         if "Arduino" in p[1]:
#             port = p[0]
#             print("Arduino detected on port", port)
#
#     return port


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip



if __name__ == "__main__":
    print("Current IP is", get_ip())
    print("Point your browser to http://", get_ip(), sep="")
    print()

    #app.run(host='0.0.0.0', port=80, debug=True)
    lightController.main()
    app.run(host='0.0.0.0', port=80)

