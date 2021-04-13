import pigpio
from time import sleep
import os
import mimetypes
import http.server
import json
import colorsys

#host settings
host_name = '192.168.2.18'
host_port = 80
#rgb pins
red = 22
blue = 24
green = 23
#file where rgb data is saved
rgb_data_file = 'data.json'

def write_to_json(data, file):
    with open(file, 'w') as outfile:
        json.dump(data, outfile)

def construct_json_from_rgb(rgb):
    data = {}
    data['rgb'] = []
    data['rgb'].append({
        'red': rgb[0],
        'green': rgb[1],
        'blue': rgb[2]
    })
    return data

def get_rgb():
    rgb = []
    rgb.append(str(pi.get_PWM_dutycycle(red)))
    rgb.append(str(pi.get_PWM_dutycycle(green)))
    rgb.append(str(pi.get_PWM_dutycycle(blue)))
    return rgb

def turn_off_ledstrip():
    pi.set_PWM_dutycycle(red, 0)
    pi.set_PWM_dutycycle(green, 0)
    pi.set_PWM_dutycycle(blue, 0)

def set_rgb(rgb):
    pi.set_PWM_dutycycle(red, rgb[0])
    pi.set_PWM_dutycycle(green, rgb[1])
    pi.set_PWM_dutycycle(blue, rgb[2])

def save_rgb_data_to_file():
    rgb = get_rgb()
    data = construct_json_from_rgb(rgb)
    write_to_json(data, 'data.json')

def on_of_handle(is_on):
    if is_on == 'false':
        save_rgb_data_to_file()
        turn_off_ledstrip()

    else:
        with open(rgb_data_file) as json_file:
            data = json.load(json_file)
            for p in data['rgb']:
                pi.set_PWM_dutycycle(red, p['red'])
                pi.set_PWM_dutycycle(green, p['green'])
                pi.set_PWM_dutycycle(blue, p['blue'])

def post_request_handle(post_data):
    if post_data[0] == "brightness":
        brightness = post_data[1]
        brightness_handle(brightness)
        
    elif post_data[0] == "color":
        rgb = post_data[1].split(',')    # Only keep the rgb values
        color_handle(rgb)

    elif post_data[0] == "toggle":
        value = post_data[1] #keep the toggle value
        on_of_handle(value)

def color_handle(rgb):
    set_rgb(rgb)
    save_rgb_data_to_file()

def brightness_handle(brightness):
    rgb = get_rgb()
    print()
    print('RGB: ' + rgb[0] + ', ' + rgb[1] + ', ' + rgb[2])
    print('Brightness: ' + str(brightness))

    r, g, b = float(rgb[0])/255.0, float(rgb[1])/255.0, float(rgb[2])/255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = float(brightness)/200.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = r*255.0, g*255.0, b*255.0
    print(r, g, b)

    rgb = []
    rgb.append(r)
    rgb.append(g)
    rgb.append(b)
    set_rgb(rgb)

    print()

class MyServer(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])    # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")   # Get the data
        post_data = post_data.split("=")
        
        post_request_handle(post_data)

        self._redirect('/')    # Redirect back to the root url

if __name__ == '__main__':
    pi = pigpio.pi()
    http_server = http.server.HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pi.stop()
        http_server.server_close()
