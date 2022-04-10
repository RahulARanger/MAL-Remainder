from flask import Flask
from _thread import interrupt_main
from MAL_Remainder.common_utils import EnsurePort

app = Flask(__name__)
EnsurePort.get_port()


app.run()