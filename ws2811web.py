import serial
from flask import Flask
# Init Flask
app = Flask(__name__)

# Open up conn. with device
ser = serial.Serial("/dev/ttyACM0")
ser.write("%C %U") # Clear the LEDs

# Define a passthrough command
@app.route("/cmd/<string>")
def command(string):
   ser.write(string)
   return "{ result : 'Command Sent' }"

# Define set a LED command
@app.route("/strip/range/<start>/<end>/<color>")
def Range(start,end,color):
   # Parse out color
   rgb = HTMLColorToRGB(color)
   #Push To Device
   ser.write("%R"+start+" "+end+" "+str(rgb[0])+" "+str(rgb[1])+" "+str(rgb[2])+" %U")
   return "{ result : 'Command Sent' }"

@app.route("/strip/set/<led>/<color>")
def Set(led,color):
   # Parse out color
   rgb = HTMLColorToRGB(color)
   #Push To Device
   ser.write("%S"+led+" "+str(rgb[0])+" "+str(rgb[1])+" "+str(rgb[2])+" %U")
   return "{ result : 'Command Sent' }"


# Define Clear Strip Command
@app.route("/strip/clear")
def Clear():
   ser.write("%C")
   return "{ result : 'Command Sent' }"

#Helper Functions
def HTMLColorToRGB(colorstring):
   colorstring = colorstring.strip()
   if colorstring[0] == '#': colorstring = colorstring[1:]
   if len(colorstring) != 6:
      raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
   r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
   r, g, b = [int(n, 16) for n in (r, g, b)]
   return (r, g, b)


# Start the server
if __name__ == "__main__":
   app.debug = True
   app.run(host='0.0.0.0') # Run server on all IFs

