#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# by Jurek Baumann

import npyscreen

# class SyntaxHistSell(npyscreen.FixedText):
#     def update_highlighting(self, start, end):
#         colorRed=1792
#         colorCyan=1024
#         colorGreen=1280
#         colorYellow=2048
#         colorWhite=0
#         colorBlack=512
#
#         self._highlightingdata = [
#          colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,
#         ]


class SyntaxObBids(npyscreen.FixedText):
    def update_highlighting(self, start, end):
        colorWhite=0
        colorGreen=1280

        self._highlightingdata = [ colorWhite,colorWhite,colorWhite,
        colorGreen,colorGreen,colorGreen,colorGreen,colorGreen,colorGreen,colorGreen,colorGreen,colorGreen,colorGreen,
        ]

class SyntaxObAsks(npyscreen.FixedText):
    def update_highlighting(self, start, end):
        colorWhite=0
        colorRed=1792

        self._highlightingdata = [ colorWhite,colorWhite,colorWhite,
        colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,colorRed,
        ]

# class SyntaxBids(npyscreen.FixedText):
#
#     # def static changeTheme(colorStr):
#     #     if colorStr == "c1":
#     #         pass
#
#
#     def update_highlighting(self, start, end):
#         # highlighting color
#         hl_cyan = 1024
#         hl_green = self.parent.theme_manager.findPair(self, 'LABEL')
#         hl_white = self.parent.theme_manager.findPair(self, 'DEFAULT')
#         # with open("myfile.txt", "w") as f:
#         #     f.write(str(self.parent.theme_manager.findPair(self, 'STANDOUT')))
#
#
#
#
#         self._highlightingdata = [
#         hl_white,hl_white,hl_white,
#         hl_cyan,hl_cyan,hl_cyan,hl_cyan,hl_green,hl_green,hl_green,hl_green,hl_green,hl_green
#         ]
