from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import QSize
from settings import *


class SuggestedWordButton(QPushButton):
    def __init__(self, label='', parent=None):
        super().__init__(label, parent)


class ResetButton(QPushButton):
    def __init__(self, label='', parent=None, row=0, col=0):
        super().__init__(label, parent)
        self.color = RED
        self.style = f"""
                            background-color: {self.color};
                            color: white;
                            padding: 20px;
                            border-radius: 10px;
                            """
        self.setStyleSheet(self.style)
        self.setFont(BUTTON_FONT)
        self.setMinimumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                           QSizePolicy.Policy.MinimumExpanding)

class LetterButton(QPushButton):
    def __init__(self, label='', parent=None, row=0, col=0):
        super().__init__(label, parent)

        self.row = row
        self.col = col
        self.color = GRAY # Change to blank later
        self.style = f"""
                    background-color: {self.color};
                    color: white;
                    padding: 1px;
                    border-radius: 5px;
                    """
        self.setStyleSheet(self.style)
        self.setFont(BUTTON_FONT)
        self.setMinimumSize(60, 60)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                           QSizePolicy.Policy.MinimumExpanding)
        self.clicked.connect(self.cycle_button_color)

    def cycle_button_color(self):
        COLORS = [GRAY, YELLOW, GREEN, GRAY]
        for i, color in enumerate(COLORS):
            if color == self.color:
                self.color = COLORS[i+1]
                break
        # Update style sheet
        # Look into changing this setup later. It works for now
        # Possibly use StringVar() from Tkinter?
        self.style = f"""
                            background-color: {self.color};
                            color: white;
                            padding: 1px;
                            border-radius: 5px;
                            """
        self.setStyleSheet(self.style)

    def change_button_color(self, color=GRAY):
        self.color = color
        self.style = f"""
                            background-color: {self.color};
                            color: white;
                            padding: 1px;
                            border-radius: 5px;
                            """
        self.setStyleSheet(self.style)

    def sizeHint(self) -> QSize:
        base = super().sizeHint()
        side = max(base.width(), base.height())
        return QSize(side, side)