import sys
import time
import json

from PyQt4 import QtGui, QtCore
from functools import partial

class Room(object):
    current_temp = 0
    set_temp = 70
    name = "Test"
    temperature_probe = None
    vents = []
    schedules = []

    def __init__(self, _current_temp, _set_temp, _name):
        self.current_temp = _current_temp
        self.set_temp = _set_temp
        self.name = _name

    def inc_set_temp(self):
        self.set_temp += 1

    def dec_set_temp(self):
        self.set_temp -= 1

    def change_name(self, new_name):
        self.name = new_name

    def to_json(self):
        data = {
            'current_temp':self.current_temp,
            'set_temp':self.set_temp,
            'name':self.name,
            'vents':self.vents,
            'schedules':self.schedules
        }
        return json.dumps(data)

    def load_json(self, json):
        data = json.loads(json)
        self.current_temp = data['current_temp']
        self.set_temp = data['set_temp']
        self.name = data['name']
        for vent in data['vents']:
            self.vents.append(vent)
        for schedule in data['schedules']:
            self.schedules.append(schedule)

    def add_vent(self, vent):
        self.vents.append(vent)

    def add_temp_probe(self, probe):
        self.temperature_probe = probe

class Button(QtGui.QPushButton):
    def __init__(self, text, window, _x, _y, _width = None, _height = None):
        super(Button, self).__init__(text, window)
        if (_width != None and _height != None):
            self.resize(_width, _height)
        self.move(_x, _y)

class Label(QtGui.QLabel):
    def __init__(self, text, window, _x, _y, _width, _height, _fontSize):
        super(Label, self).__init__(window)
        self.setText(text)
        self.resize(_width, _height)
        self.move(_x, _y)
        self.setStyleSheet('color: white')
        self.setFont(QtGui.QFont("Serif", _fontSize, QtGui.QFont.Bold))


class Window(QtGui.QMainWindow):
    def __init__(self, _title, _nextWindow=None):
        super(Window, self).__init__()
        self.setWindowTitle(_title)
        self.nextWindow = _nextWindow

        if (_title != "main"):
            homeButton = Button("Home", self, 0, 0, 50, 20)
            homeButton.clicked.connect(self.goto_home)

        self.refresh_window(self)

    def close_application(self):
        print("custom close")
        sys.exit()

    def change_windows(self):
        self.hide()
        self.refresh_window(self.nextWindow)
        self.nextWindow.show()

    def refresh_window(self, window):
        window.setGeometry(xPos, yPos, width, height)
        window.setPalette(colorPal)

    def goto_home(self):
        self.nextWindow = MainW
        self.change_windows()


class MainWindow(Window):
    def home(self):
        # btn = QtGui.QPushButton("Quit", self)
        # btn.clicked.connect(self.close_application)
        # btn.resize(100, 100)
        # btn.move(0, 0)

        # btn2 = QtGui.QPushButton("Settings", self)
        # btn2.clicked.connect(self.goto_settings)
        # btn2.resize(100, 100)
        # btn2.move(200, 0)

        start_y = 60
        for i in range(len(rooms)):
            print(i)
            btn = Button("Room " + rooms[i].name + " - " + str(rooms[i].current_temp),
                         self, 250, start_y, 200, 60)
            this_room = rooms[i]
            btn.clicked.connect( partial(self.goto_room, room = rooms[i]) )
            start_y += 60
        return

    def show_window(self):
        self.show()

    def goto_settings(self):
        self.nextWindow = SettingsW
        self.change_windows()

    def goto_room(self, room):
        current_room = room
        self.nextWindow = RoomW
        RoomW.set_current_room(room)
        RoomW.home()
        self.change_windows()


class SettingsWindow(Window):
    red = False
    maximized = False

    def home(self):
        btn = QtGui.QPushButton("Change color", self)
        btn.clicked.connect(self.change_color)
        btn.resize(100, 100)
        btn.move(100, 0)

        btn3 = QtGui.QPushButton("Change size", self)
        btn3.clicked.connect(self.change_size)
        btn3.resize(100, 100)
        btn3.move(200, 0)

    def show_window(self):
        self.show()

    def change_color(self):
        whitePal = QtGui.QPalette()
        whitePal.setColor(QtGui.QPalette.Background, QtCore.Qt.white)

        redPal = QtGui.QPalette()
        redPal.setColor(QtGui.QPalette.Background, QtCore.Qt.red)

        if self.red:
            # colorPal = whitePal
            colorPal.setColor(QtGui.QPalette.Background, QtCore.Qt.white)
            self.setPalette(colorPal)
            self.red = False
        else:
            # colorPal = redPal
            colorPal.setColor(QtGui.QPalette.Background, QtCore.Qt.red)
            self.setPalette(colorPal)
            self.red = True
        return

    def change_size(self):
        global width, height
        if self.maximized:
            width = 480
            height = 320
            self.setGeometry(xPos, yPos, width, height)
            self.maximized = False
        else:
            width = 960
            height = 640
            self.setGeometry(xPos, yPos, width, height)
            self.maximized = True


class RoomWindow(Window):
    name = "Test"
    current_temp = 0
    set_temp = 0
    current_room = None

    def home(self):

        btn1 = Button("Schedules", self, 10, 260, 220, 50)
        self.nextWindow = ScheduleW
        btn1.clicked.connect(self.change_windows)

        btn2 = Button("Change Room", self, 240, 260, 220, 50)
        self.nextWindow = ScheduleW
        btn2.clicked.connect(self.change_windows)

        actTempLabel = Label(self.current_room.name, self, 20, 20, 240, 50, 12)
        actTemp = Label(str(self.current_room.current_temp), self, 30, 30, 240, 240, 70)


        btn3 = Button("/ Up \\", self, 240, 20, 100, 100)
        btn3.clicked.connect(self.inc_temp)

        btn4 = Button("\\ Down /", self, 240, 130, 100, 100)
        btn4.clicked.connect(self.dec_temp)

        # setTempLabel = Label("Set Temp", self, 370, 200, 30, 55, 10)
        setTemp = Label(str(self.current_room.set_temp), self, 370, 80, 100, 100, 30)

    def inc_temp(self):
        self.current_room.inc_set_temp()
        self.refresh_window(self)

    def dec_temp(self):
        self.current_room.dec_set_temp()
        self.refresh_window(self)

    def set_current_room(self, room):
        self.current_room = room

    def refresh_room(self):
        self.home()


class ScheduleWindow(Window):
    def home(self):
        return

xPos = 100
yPos = 100
width = 480
height = 320
colorPal = QtGui.QPalette()
colorPal.setColor(QtGui.QPalette.Background, QtCore.Qt.gray)

app = QtGui.QApplication(sys.argv)

MainW = MainWindow("main")
SettingsW = SettingsWindow("settings")
RoomW = RoomWindow("room")
ScheduleW = ScheduleWindow("schedule")
rooms = []

rooms.append(Room(70, 70, "Room A"))
rooms.append(Room(69, 69, "Room B"))
rooms.append(Room(68, 68, "Room C"))

current_room = rooms[0]

def load_rooms():
    with open('rooms.json', 'r') as fp:
        data = json.load(fp)
        for room_json in data:
            _current_temp = room_json[0]
            _set_temp = room_json[1]
            _name = room_json[2]
            create_room(_current_temp, _set_temp, _name)


def save_rooms():
    room_data = []
    for room in rooms:
        room_data.append(room.to_json())
    with open('rooms.json', 'w') as fp:
        json.dump(room_data, fp)


def create_room(_current_temp, _set_temp, _name):
    new_room = Room(_current_temp, _set_temp, _name)
    rooms.append(new_room)

# for each in [MainW, SettingsW, RoomW, ScheduleW]:
#     each.home()


def run():
    load_rooms()
    MainW.home()
    MainW.show()
    sys.exit(app.exec_())


run()
