#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

import npyscreen


class SyntaxTest(npyscreen.FixedText):
    # def __init__(self, syntaxColors):
    #     super()

    def __add__():


        hl_red = self.parent.theme_manager.findPair(self, 'DANGER')
        hl_cyan = self.parent.theme_manager.findPair(self, 'STANDOUT')
        hl_green = self.parent.theme_manager.findPair(self, 'LABEL')
        hl_yellow = self.parent.theme_manager.findPair(self, 'CONTROL')
        hl_white = self.parent.theme_manager.findPair(self, 'DEFAULT')
        hl_black = self.parent.theme_manager.findPair(self, 'CURSOR_INVERSE')

        if syntaxColors == c1:
            self._highlightingdata = [
        hl_white,hl_white,hl_white,
        hl_red,hl_red,hl_red,hl_red,hl_red,hl_red,hl_red,hl_red,hl_red,hl_red
        ]
        elif syntaxColors == c2:
            self._highlightingdata = [
        hl_white,hl_white,hl_white,
        hl_green,hl_green,hl_green,hl_green,hl_green,hl_green,hl_green,hl_green,hl_green,hl_green
        ]


    def update_highlighting(self, start, end):
        # highlighting color
        # with open("myfile.txt", "w") as f:
        #     f.write(str(self))

        pass



        # self._highlightingdata = [
        # hl_white,hl_white,hl_white,
        # hl_red,hl_red,hl_red,hl_red,hl_red,hl_red,hl_red,hl_red,hl_red,hl_red
        # ]

# class colorAliases():
#     def update_highlighting(self, start, end):

class SyntaxAsks(npyscreen.FixedText):
    _highlightingdata = [
    1280,1280,1280,
    1024,1024,1024,1024,1024,1024,1024,1024,1024,1024
    ]
    @staticmethod
    def changeTheme(color):

        if color == "c1":
            # with open("myfile.txt", "w") as f:
            #     f.write("SETZE C1")
            _highlightingdata = [
            1280,1280,1280,
            1024,1024,1024,1024,1024,1024,1024,1024,1024,1024
            ]
        elif color == "c2":
            _highlightingdata = [
            1024,1024,1024,
            1280,1280,1280,1280,1280,1280,1280,1280,1280,1280
            ]

class SyntaxHistSell(npyscreen.FixedText):
    def update_highlighting(self, start, end):
        colorRed=1792
        colorCyan=1024
        colorGreen=1280
        colorYellow=2048
        colorWhite=0
        colorBlack=512

        self._highlightingdata = [
         colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,
        ]
class SyntaxHistBuy(npyscreen.FixedText):
    def update_highlighting(self, start, end):
        colorCyan=1024

        self._highlightingdata = [
         colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,
        ]

class SyntaxObBids(npyscreen.FixedText):
    def update_highlighting(self, start, end):
        colorWhite=0
        colorCyan=1024

        self._highlightingdata = [ colorWhite,colorWhite,colorWhite,
        colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,colorCyan,
        ]

class SyntaxObAsks(npyscreen.FixedText):
    def update_highlighting(self, start, end):
        colorWhite=0
        colorRed=1792

        self._highlightingdata = [ colorWhite,colorWhite,colorWhite,
        colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,
        ]

class SyntaxBids(npyscreen.FixedText):

    # def static changeTheme(colorStr):
    #     if colorStr == "c1":
    #         pass


    def update_highlighting(self, start, end):
        # highlighting color
        hl_cyan = 1024
        hl_green = self.parent.theme_manager.findPair(self, 'LABEL')
        hl_white = self.parent.theme_manager.findPair(self, 'DEFAULT')
        # with open("myfile.txt", "w") as f:
        #     f.write(str(self.parent.theme_manager.findPair(self, 'STANDOUT')))




        self._highlightingdata = [
        hl_white,hl_white,hl_white,
        hl_cyan,hl_cyan,hl_cyan,hl_cyan,hl_green,hl_green,hl_green,hl_green,hl_green,hl_green
        ]
