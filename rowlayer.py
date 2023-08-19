#!/bin/python3
 
# This program is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published 
# by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <https://www.gnu.org/licenses/>. 
#
# Copyright (C) 2023  -  V972501

# "Row Layer"

import signal
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

def start():
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  app = QtWidgets.QApplication(sys.argv)
  overlay = Overlay()
  overlay.show()
  sys.exit(app.exec_())

  
class Overlay(QtWidgets.QWidget):

  def __init__(self):
    super().__init__()
    self.setWindowTitle("RowLayer")
    self.setGeometry(100, 100, 500, 100)
    self.setWindowIcon(QtGui.QIcon("RowLayer.png"))
    self.setAttribute(  QtCore.Qt.WA_TranslucentBackground)
    
    self.setWindowFlags(  QtCore.Qt.WindowStaysOnTopHint 
                        | QtCore.Qt.FramelessWindowHint    
                        )

    self.main_style = ( 
      "QWidget {background-color: qlineargradient( x1:0 y1:1, x2:0 y2:0, " +
      "stop:0 #1e1e1e, stop:1 #313131); " + 
      "border: 1px ridge black} " +

      "QSlider {border: none; height: 7} " +
      "QSizeGrip {image: url(size_grip.png); " +
      " background-color: rgba(0, 0, 0, 0); border: none; } " +

      "QSlider::handle {background-color:#313131 ; border: 2px ridge #1e1e1e}" +
      "QPushButton {padding-top:0;height: 20; background-color: none; " +
      " border: none; color: #5b5b5d} " +

      "QLabel {border: none}"
                      )

    self.mouse_pos = None
    self.color = "black"
    slider_width = 200

    alpha_min = 0
    alpha_max = 100

    size_min = 1
    size_max = 32
    self.button_size = 16

    self.alpha = (alpha_max/2) * 0.01
    self.size = size_max/2

    # Control elements
    ## Open config button
    self.button_config = QtWidgets.QPushButton("^", self)
    self.button_config.setCheckable(True)
    self.button_config.move(0,0)
    self.button_config.clicked.connect(self.toggle_config)
    self.button_config.setChecked(True)
    
    ## Quit button
    self.button_quit = QtWidgets.QPushButton("x", self)
    self.button_quit.setCheckable(True)
    self.button_quit.clicked.connect(self.close)
    
    ## Invert color button
    self.button_invert = QtWidgets.QPushButton("", self)
    self.button_invert.setIcon(QtGui.QIcon("invert.png"))
    self.button_invert.clicked.connect(self.update_color)
    self.button_invert.setFlat(True)

    ## Size grip
    size_grip = QtWidgets.QSizeGrip(self)

    def set_button_size(b):
      b.setFixedSize(self.button_size, self.button_size)

    set_button_size(self.button_config)
    set_button_size(self.button_quit)
    set_button_size(self.button_invert)
    set_button_size(size_grip)


    ## Alpha slider
    icon_alpha = QtWidgets.QLabel("")
    icon_alpha.setPixmap(QtGui.QPixmap("alpha.png"))
    self.slider_alpha = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    self.slider_alpha.setMaximumWidth(slider_width)
    self.slider_alpha.setMinimumWidth(slider_width)
    self.slider_alpha.setMinimum(alpha_min)
    self.slider_alpha.setMaximum(alpha_max)
    self.slider_alpha.setValue(alpha_max/2)
    self.slider_alpha.valueChanged.connect(self.update_alpha)
    
    ## Size slider
    icon_size = QtWidgets.QLabel("")
    icon_size.setPixmap(QtGui.QPixmap("size.png"))
    self.slider_size = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    self.slider_size.setMaximumWidth(slider_width)
    self.slider_size.setMinimumWidth(slider_width)
    self.slider_size.setMinimum(size_min)
    self.slider_size.setMaximum(size_max)
    self.slider_size.setValue(self.size)
    self.slider_size.valueChanged.connect(self.update_size)
    
    
    # Create layouts
    main_layout = QtWidgets.QVBoxLayout()
    top_layout = QtWidgets.QHBoxLayout()
    bottom_layout = QtWidgets.QHBoxLayout()

    def set_margins(layout):
      layout.setContentsMargins( 0, 0, 0, 0)

    set_margins(main_layout)
    set_margins(top_layout)
    set_margins(bottom_layout)

    top_layout.setAlignment(QtCore.Qt.AlignTop)
    bottom_layout.setAlignment(QtCore.Qt.AlignRight)

    self.top_panel = QtWidgets.QFrame()
    self.top_panel.setMaximumHeight(self.button_size)
    self.top_panel.setLayout(top_layout)


    # Compose control elements
    top_layout.addWidget(self.button_config)
    top_layout.addStretch()
    top_layout.addWidget(icon_alpha)
    top_layout.addWidget(self.slider_alpha)
    top_layout.addWidget(icon_size)
    top_layout.addWidget(self.slider_size)
    top_layout.addWidget(self.button_invert, alignment=QtCore.Qt.AlignTop)
    top_layout.addStretch()
    top_layout.addWidget(self.button_quit)
    
    bottom_layout.addWidget(size_grip)
    
    main_layout.addWidget(self.top_panel)
    main_layout.addStretch()
    main_layout.addLayout(bottom_layout)
    
    self.setStyleSheet(self.main_style)
    self.setLayout(main_layout)
    self.menu_elements = [
                          size_grip,
                          icon_size,
                          self.slider_size,
                          icon_alpha,
                          self.slider_alpha,
                          self.button_invert,
                          self.button_quit,
                          ]
    


  def toggle_config(self, checked):
      # Show or hide configs
      if checked:
        self.button_config.setText("^")
        self.setStyleSheet(self.main_style)
        for i in self.menu_elements:
          i.show()

      else:
        self.button_config.setText("v")
        self.setStyleSheet("color:lightGray")
        for i in self.menu_elements:
          i.hide()
        
    
  def resizeEvent(self, event):
    self.button_quit.move(self.width()-self.button_quit.width(),0)

  def mousePressEvent(self, event):
    self.mouse_pos = event.pos()

  def mouseMoveEvent(self, event):
    if self.mouse_pos:
      diff = event.pos() - self.mouse_pos
      newpos = self.pos() + diff
      self.move(newpos)

  def mouseReleaseEvent(self, event):
    self.mouse_pos = None

  def update_alpha(self, value):
    self.alpha = value * 0.01
    self.update()

  def update_size(self, value):
    self.size = value
    self.update()
    
  def update_color(self,checked):
    self.color = "black" if self.color == "white" else "white"
    self.update()

  def paintEvent(self, event=None):
    penSize = -1  # sets off default "3d" effect, makes flat look
    painter = QtGui.QPainter(self)
    painter.setOpacity(self.alpha)
    painter.setBrush(QtGui.QColor(self.color))
    painter.setPen(QtGui.QPen(QtGui.QColor(self.color), penSize))

    height = int(self.height())
    y = self.button_size + 2
    border_size = 1
    while y < height:
      painter.drawRect(border_size, y, 
        int(self.width())-border_size*2, self.size)
      y += self.size * 2
            

start()
