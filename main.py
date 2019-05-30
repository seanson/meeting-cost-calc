#!/usr/bin/env python3

import sys
from math import floor

from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLCDNumber, QLabel
from PyQt5.QtCore import Qt, QTimer, QTime, QDateTime

class Meeting(QWidget):
    def __init__(self, people, rate=100.0, scale=10):
        super().__init__()

        self.people = people
        self.rate = rate

        self.layout = QVBoxLayout()

        self.startlabel = QLabel()
        self.startlabel.setFont(QtGui.QFont("SansSerif", scale))

        self.elapsedlabel = QLabel()
        self.elapsedlabel.setFont(QtGui.QFont("SansSerif", scale))

        self.cost = QLabel()
        self.cost.setFont(QtGui.QFont("SansSerif", scale))    

        self.time = QDateTime.currentDateTime()
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

        self.layout.addWidget(self.startlabel)
        self.layout.addWidget(self.elapsedlabel)
        self.layout.addWidget(self.cost)
        
        self.startlabel.setText(f"Start: {self.time.toString('hh:mm:ss')}")

    def tick(self):
        currentTime = QDateTime.currentDateTime()
        elapsed = self.time.secsTo(currentTime)
        peoplecost = (elapsed * self.people * (self.rate/3600.0))
        
        secs = elapsed % 60
        mins = floor(elapsed / 60.0) % 60
        hours = floor(elapsed / 3600.0) % 60

        self.elapsedlabel.setText(f"Elapsed: {hours:02.0f}:{mins:02.0f}:{secs:02.0f}")
        self.cost.setText(f"{self.people} people at ${self.rate:.0f}/hr: ${peoplecost:.2f}")

if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[1]} <people> [rate]")
    sys.exit(1)
if len(sys.argv) == 2:
    people = int(sys.argv[1])
    rate = 100.0
    scale = 24
if len(sys.argv) == 3:
    people = int(sys.argv[1])
    rate = float(sys.argv[2])
    scale = 24
if len(sys.argv) == 4:
    people = int(sys.argv[1])
    rate = float(sys.argv[2])
    scale = int(sys.argv[3])

print(f"Configured for {people} people at ${rate}/hour.")

app = QApplication([])
window = QWidget()
meeting = Meeting(people, rate, scale)
meeting.tick()
window.setLayout(meeting.layout)
window.setWindowFlags(Qt.WindowStaysOnTopHint)
window.show()
app.exec_()
