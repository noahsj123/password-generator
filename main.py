from tkinter import *
# Because messagebox is not a class, need to import separately
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
from random import randint, choice, shuffle

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)
    #.join() joins everything in the list-- in this case using an empty char
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    # The line below copies the password to the clipboard
    pyperclip.copy(password)
    # messagebox.showinfo(message="Password copied to clipboard")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def clear_text_boxes():
    password_entry.delete(0, END)
    website_entry.delete(0, END)

def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    #PART OF JSON UPDATE:
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Empty Field", message="Oops, you left a required field empty!")
    else:
        is_okay = messagebox.askokcancel(title=website, message=f"Your info for {website.title()}:\nEmail: "
                                                                f"{email}\nPassword: {password}"
                                                                f"\nClick 'Cancel' to redo or 'OK' to save")
        if is_okay:
            #JSON UPDATE:
            try:
                with open("data.json", "r") as data_file:
                    #Read old data
                    data = json.load(data_file)
            except:
                with open("data.json", "w") as data_file:
                    pass
                    # Saving updated data
                    json.dump(new_data, data_file, indent=4)
            else:
                #Updating old data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                clear_text_boxes()

        else:
            clear_text_boxes()
# ---------------------------- SEARCH --------------------------------- #
def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            pw = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {pw}")
        else:
            messagebox.showinfo(title=website, message=f"No details for {website} exist")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(bg="white", padx=20, pady=20)

# CANVAS
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="/Users/noahjacobs/Documents/PycharmProjects/password-generator/logo.png")
canvas.create_image(100, 100, image=logo)
canvas.config(bg="white", highlightthickness=0)
canvas.grid(row=0, column=1)

# LABELS
website_label = Label(text="Website:", bg="white", fg="black")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", bg="white", fg="black")
email_label.grid(row=2, column=0)

pw_label = Label(text="Password:", bg="white", fg="black")
pw_label.grid(row=3, column=0)

# ENTRIES
website_entry = Entry(highlightbackground="white", bg="white", fg="black", width=21)
website_entry.focus()
website_entry.grid(row=1, column=1)

email_entry = Entry(highlightbackground="white", bg="white", fg="black", width=37)
email_entry.insert(0, "noahsj@umich.edu")
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(highlightbackground="white", bg="white", fg="black", width=21)
password_entry.grid(row=3, column=1, columnspan=1)

# BUTTONS
generate_pw_button = Button(text="Generate Password", highlightbackground="white", fg="black", command=generate_password)
generate_pw_button.grid(row=3, column=2)

add_button = Button(text="Add", highlightbackground="white", fg="black", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", highlightbackground="white", fg="black", width=13, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
