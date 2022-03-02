from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
lang_dict = {}

# Access csv file using pandas
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    lang_dict = original_data.to_dict(orient="records")
else:
    lang_dict = data.to_dict(orient="records")


# next_card function
def next_card():
    global flip_timer, current_card
    window.after_cancel(flip_timer)
    current_card = random.choice(lang_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(image, image=card_front_image)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(image, image=card_back_image)

def remove_from_dict():
    lang_dict.remove(current_card)
    words_to_learn = pandas.DataFrame(lang_dict)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# Window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_button_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_image,
                      highlightbackground=BACKGROUND_COLOR, command=remove_from_dict)
right_button.grid(column=0, row=1)
wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0,
                      highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=1, row=1)

next_card()

window.mainloop()
