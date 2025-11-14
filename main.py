import sys
from PyQt6.QtWidgets import QScrollArea, QApplication, QWidget, QGridLayout, QLineEdit
from gui import *
from settings import *

# - Semi DONE
# - I'd like to restructure the main logic so that I have a main.py & a GUI.py
# -
# - DONE
# - Need a reset button that clears out everything **
# -
# - DONE
# - Need a nice unified GUI *
# -
# - DONE
# - Have letters auto color themselves if matching pos from previous answers
# -
# - semi DONE
# - TROUT Greens = [T: [0]] Grays = [T: [4]] will result in no T words showing
# - when it should, since the first T is green
# - TUTOR [g, y, y, y, y] should have words with two T's in the results, but it will show
# - other options like TOURS or TOURN
# -
# - DONE
# - Have suggested word button populate the next open word row on click

# - DONE
# - When clicking word, doesn't always go to proper row.
# - if row is populated at all, it will bug out and go to the next row
# -
# - DONE
# - When clicking word, need to update text field to match word that was clicked
# -
# -
# - Create feature to show the most common remaining letter?
# - This can help enforce good guesses that would eliminate that letter
#
# -
# - Test feature that can help detect most efficient word.
# - I anticipate the run time will rend this kind of useless tbh
# - - Take every word in the suggested list and see how many words will remain after picking that word
# - - Leave the word that will result in the smallest return list
# - - - I also anticipate that this could be janky if it returns an unusable wordle word

# Getting all valid words
with open('wordle_approved_words.txt', 'r') as file:
    valid_words = [word.strip().upper() for word in file if len(word.strip()) == 5]


class MainWindow(QWidget):
    def __init__(self):
        # Window settings
        super().__init__()
        self.setWindowTitle('ADIEU')
        self.resize(600, 600)
        #self.setStyleSheet(f"background-color: {WIN_BG};")

        # -- UI Elements
        # - Grid
        self.grid = QGridLayout()
        # - Letter buttons for the user words
        self.letter_buttons = [[LetterButton(row=j, col=i) for i in range(ROWS)] for j in range(COLUMNS)]
        # - Entries for user words
        self.word_entries = [QLineEdit() for _ in range(ROWS + 1)]
        # - Scroll window w/ buttons of suggested words
        self.best_word_buttons = []
        self.scroll = QScrollArea()
        self.content = QWidget()
        self.words_grid = QGridLayout(self.content)
        # Reset button
        self.reset_button = ResetButton('RESET')
        self.setup_ui()

        #
        self.green_letters = {}
        self.yellow_letters = {}

    def setup_ui(self):
        # GRID settings
        self.grid.setSpacing(5)

        # BUTTONS for words the user inputs
        # Each button is an individual letter of the word
        # User can chose color of button so that the letters can be properly filtered
        for i, row in enumerate(self.letter_buttons):
            for j, button in enumerate(row):
                self.grid.addWidget(button, i, j)
        for row in self.letter_buttons:
            for button in row:
                button.clicked.connect(self.update_letter_lists)

        # TEXT ENTRIES for user to input their words
        for i, entry in enumerate(self.word_entries):
            self.grid.addWidget(entry, i, COLUMNS+1)
            entry.grid_row = i
            entry.setMaxLength(5)

        for entry in self.word_entries:
            entry.textChanged.connect(self.update_button_text)

        # WORD BUTTONS for user to chose from. Buttons are inside a scrollable canvas
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.content)

        # Sets the layout based on self.grid
        self.setLayout(self.grid)

        # RESET BUTTON
        self.grid.addWidget(self.reset_button, COLUMNS + 3, ROWS + 2)
        self.reset_button.clicked.connect(self.reset_UI)

    def update_letter_buttons(self, word, row):
        for i, button in enumerate(self.letter_buttons[row]):
            button.setText(word[i].upper())
            if button.text() in self.green_letters:
                if i in self.green_letters[button.text()]:
                    button.change_button_color(GREEN)
            if button.text() in self.yellow_letters:
                if i in self.yellow_letters[button.text()]:
                    button.change_button_color(YELLOW)

    def update_button_text(self, text):
        word = text + ' ' * (5 - len(text))  # Pad the word out with spaces
        entry = self.sender()
        row = getattr(entry, 'grid_row', None)

        self.update_letter_buttons(word, row)

        # for i, button in enumerate(self.letter_buttons[row]):
        #     button.setText(word[i].upper())
        #
        #     # Updates button color if letter matches previous letter color
        #
        #     if button.text() in self.green_letters:
        #         if i in self.green_letters[button.text()]:
        #             button.change_button_color(GREEN)
        #     if button.text() in self.yellow_letters:
        #         if i in self.yellow_letters[button.text()]:
        #             button.change_button_color(YELLOW)

        self.fresh_word = True
        if word.count(' ') == 0 and self.fresh_word:
            self.fresh_word = False
            self.word_entries[row+1].setFocus()
            self.update_letter_lists()

        if word.count(' ') == 5 and self.fresh_word:
            for i, button in enumerate(self.letter_buttons[row]):
                    button.change_button_color()
            self.fresh_word = False
            self.update_letter_lists()

        if word.count(' ') < 5 and not self.fresh_word:
            self.fresh_word = True

    def update_letter_lists(self):
        gray_letters = []
        self.yellow_letters = {}
        self.green_letters = {}
        word = ''
        for i, row in enumerate(self.letter_buttons):
            for button in row:
                letter = button.text()
                col = button.col
                if letter == ' ' or letter == '':
                    continue
                word += letter
                if button.color == YELLOW:
                    if letter not in self.yellow_letters:
                        self.yellow_letters[letter] = []
                        self.yellow_letters[letter].append(col)
                    elif letter in self.yellow_letters and col not in self.yellow_letters[letter]:
                        self.yellow_letters[letter].append(col)

                elif button.color == GREEN:
                    if letter not in self.green_letters:
                        self.green_letters[letter] = []
                        self.green_letters[letter].append(col)

                    elif letter in self.green_letters and col not in self.green_letters[letter]:
                        self.green_letters[letter].append(col)

                # Gets gray letters. Will skip letter if its already a green or yellow letter
                elif button.color == GRAY:
                    if (letter not in gray_letters and
                            letter not in self.green_letters and
                            letter not in self.yellow_letters):
                        gray_letters.append(letter)
            word = ''
        print(gray_letters, self.yellow_letters, self.green_letters)
        self.update_valid_words(gray_letters, self.yellow_letters, self.green_letters)

    def update_valid_words(self, grays, yellows, greens):
        best_words = [[], [], []]

        # Making sure the word list has the green letters in them at the same index
        if greens:
            for word in valid_words:
                green_checks_needed = sum(len(idx) for idx in greens.values())
                green_checks = 0
                for i, letter in enumerate(word):
                    if letter in greens:
                        if i in greens[letter]:
                            green_checks += 1
                if green_checks == green_checks_needed:
                    best_words[0].append(word)
        else:
            best_words[0] = [word for word in valid_words]

        # Making sure the word list has the yellow letters in them at different indexes
        if yellows:
            for word in best_words[0]:
                good_word = True
                yellow_checks_needed = len(yellows)
                yellow_checks = 0
                for i, letter in enumerate(word):
                    if letter in yellows and i in yellows[letter]:
                        good_word = False
                for letter in yellows:
                    if letter in word:
                        yellow_checks += 1
                if good_word and yellow_checks == yellow_checks_needed:
                    best_words[1].append(word)
        else:
            best_words[1] = [word for word in best_words[0]]

        # Making sure the word doesn't have the gray letters in them
        for word in best_words[1]:
            good_word = True
            for i, letter in enumerate(word):
                # ** FIX THIS. THIS IS LAZY SOLUTION TO THE TROUT PROBLEM **
                if letter in grays and letter not in greens:
                    good_word = False

            if good_word:
                best_words[2].append(word)


        # Checking most common letters
        most_common_letters = {}
        for word in best_words[2]:
            for letter in word:
                if letter not in most_common_letters:
                    most_common_letters[letter] = 1
                else:
                    most_common_letters[letter] += 1

        most_common_letters = dict(sorted(most_common_letters.items(), key=lambda item: item[1], reverse=True))
        print(most_common_letters)

        self.update_suggested_buttons(best_words[2])

    def update_suggested_buttons(self, best_words):
        layout = self.content.layout()

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

        if len(best_words) == len(valid_words):
            best_words = []

        self.best_word_buttons = []
        for word in best_words:
            self.best_word_buttons.append(SuggestedWordButton(word))

        print(len(best_words))

        column_count = 0
        row_count = 0
        for button in self.best_word_buttons:
            if column_count > COLUMNS - 2:
                column_count = 0
                row_count += 1
            self.words_grid.addWidget(button, row_count + 6, column_count)
            button.clicked.connect(self.populate_next_row)
            column_count += 1

        self.grid.addWidget(self.scroll, ROWS+3, 0, 10, COLUMNS)

    def reset_UI(self):
        for row in self.letter_buttons:
            for button in row:
                button.change_button_color()
                button.setText(' ')
        for field in self.word_entries:
            field.setText('')

        layout = self.content.layout()

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()  # remove from layout & UI
            widget.deleteLater()    # deletes widget from memory

    def populate_next_row(self):
        # Find the empty row
        update_row = 0
        word = self.sender().text()
        for i, row in enumerate(self.letter_buttons):
            for button in row:
                if button.text() == '' or button.text() == ' ':
                    update_row = i
                    break
            if update_row:
                break
        for i, button in enumerate(self.letter_buttons[update_row]):
            button.setText(word[i])

        self.word_entries[update_row].setText(word.lower())
        self.update_letter_buttons(word, update_row)
        self.update_letter_lists()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



