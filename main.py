import os
try:
    import requests
except:
    print("Please install \"requests\"")
    exit()
import re, time
import tkinter as tk
from tkinter import messagebox, ttk, font
import threading
from datetime import datetime
import random
import tkinter.simpledialog as simpledialog

# Update the get_users_who_solved function to use the global count_value
def get_users_who_solved(users, problem_id, progress_var, status_text_var):
    completed_users = []

    for i, user in enumerate(users):
        url = f"https://codeforces.com/api/user.status?handle={user}&from=1"
        retries = 3
        while retries:
            status_text_var.set(f"Pārbauda {user}...")
            root.update_idletasks()
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to retrieve data for {user} ({response.status_code})")
                time.sleep(1)
                retries -= 1
            else:
                print("ok")
                break
        
        if retries == 0:
            print(f"Failed to fetch {user}")
            continue
        
        submissions = response.json()
        if submissions['status'] != 'OK':
            print(f"Error with user {user}'s data.")
            continue

        for submission in submissions['result']:
            try:
                if (str(submission['problem']['contestId']) + str(submission['problem']['index']) == problem_id and
                    submission['verdict'] == 'OK'):
                    completed_users.append(user)
                    break
            except KeyError:
                pass

        # Update progress bar
        progress_var.set((i + 1) / len(users) * 100)
        root.update_idletasks()

    status_text_var.set("Pabeigts!")
    return completed_users


def process_task(justSort=False):
    def task_logic():
        # Read users from file
        with open("data/lietotaji.txt", 'r') as f:
            users = f.read().split('\n')

        # Read and back up scores
        if not os.path.exists("data/majasdarbi.txt"):
            open("data/majasdarbi.txt", 'a').close()

        with open("data/majasdarbi.txt", 'r') as f:
            data = f.read().strip()
            with open("data/majasdarbi-backup.txt", 'w+') as f_backup:
                f_backup.write(data)

            tempscores = data.split('\n')
            scores = {}
            if data:
                for s in tempscores:
                    x = s.replace("- ", "").split(" ")
                    if x[0] not in users:
                        root.after(0, lambda: messagebox.showwarning("Ai ai ai...", f"Kas ir \"{x[0]}\"? Es tādu nepazīstu..."))
                    if len(x) < 2 or len(x) > 3:
                        root.after(0, lambda: messagebox.showerror("Opā!", "Mājasdarbi.txt ir kautkādas problēmas... Vajadzētu salabot!"))
                        raise Exception("Malformed Majasdarbi.txt")
                    scores[x[0]] = [int(x[1]), (x[2][1:-1] if len(x) > 2 else '+0')]

        if not justSort:
            problem_id = task_entry.get().upper().replace(" ", "")
            solved_users = get_users_who_solved(users, problem_id, progress_var, status_text_var)

            if solved_users:
                root.after(0, lambda: messagebox.showinfo("Nu gan jauki", f"Šonedēļ mājasdarbu {problem_id} izpildīja:\n" + '\n'.join(solved_users)))
            else:
                root.after(0, lambda: messagebox.showwarning("Šausmas", f"Šonedēļ mājasdarbu {problem_id} neizpildīja NEVIENS!!!!!"))

            for user in solved_users:
                if user in scores:
                    scores[user][0] += 1
                else:
                    scores[user] = [1, '+0']

        sorted_scores = sorted(
            scores.items(),
            key=lambda item: item[1][0] + (int("0" + "".join(re.findall(r"\d", item[1][1]))) * 0.99999999999),
            reverse=True
        )

        out = ""
        for score in sorted_scores:
            out += score[0] + " - " + str(score[1][0]) + " " + (
                "" if score[1][1] == '+0' or not score[1][1] else "(" + score[1][1] + ')') + "\n"

        # Write updated scores to file
        with open("data/majasdarbi.txt", 'w') as f_out:
            f_out.write(out)

        if justSort:
            root.after(0, lambda: messagebox.showinfo("Super", "Darīts!"))
        
        goButton.pack(pady=10)
        sortButton.pack(pady=10)

    # Start the task in a separate thread
    task_thread = threading.Thread(target=task_logic)
    task_thread.daemon = True  # Ensure thread exits when main program exits
    goButton.pack_forget()
    sortButton.pack_forget()
    task_thread.start()

lastMessage=-1
messages = ["Izmanto OFast, tas atrisinās visas tavas problēmas", "Tu jau nevarētu izpildīt 630A...", "#define endl '\\n'", "Rekursīva main funkcija ir tavs draugs", "Īsāks kods - ātrāks kods",
            "Kompailers visu izdarīs tavā vietā", "Programmēšana ir tikai ļoti specifiska promtu inženierija kompailerim", "Datori ir ātri..", "Olimpiāžu programmēšanā jāizmanto tikai OOP",
            "progammēšana vai kodēšana?", "Cepti vai vārīti pelmeņi?", "Ko tu vēl te dari?", "Valter?", "Tev viss kārtībā?", "...", "Tu gribi vēl padomus?", "nu labi.."
            "Vai zināji, ka 1+1=2?", "Tiešām?", "Tad jau , tu esi ļoti labs matemātiķis.", "hmm..", "Te vairs nekā nav", "Tiešām, tas viss", "Tiešām, tas viss", "Tu vēl turpināsi?", "Nu labi, pamācīšu tev matemātiku",
            "Tu gribi sākt ar saskaitīšanu vai atņemšanu?", "Pieņemšu, ka tu teici saskaitīšanu."]

def motivate():
    global lastMessage
    lastMessage += 1
    if lastMessage >= len(messages):
        a = random.randint(1,100)
        b = random.randint(1,100)
        messagebox.showinfo("Valtera saskaitīšanas privātstundas", f"Vai zināji, ka {a} + {b} = {a+b}?")
    else:
        messagebox.showinfo("C++ padomi", messages[lastMessage])


root = tk.Tk()
root.title("Valtera superīgā mājasdarbu programma")
root.geometry("550x400") 

menu_bar = tk.Menu(root)
settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Padoms", command=motivate)
menu_bar.add_cascade(label="Palīdzība", menu=settings_menu)
root.config(menu=menu_bar)


h1_font = font.Font(family="Helvetica", size=17, weight="bold")
h1_label = tk.Label(root, text="Valtera superīgā mājasdarbu programma V2", font=h1_font)
h1_label.pack(pady=20)

tk.Label(root, text="Codeforces ID:", font=("Helvetica", 16)).pack(pady=10)
task_entry = tk.Entry(root)
task_entry.pack(pady=5)
task_entry.config(font=("Helvetica", 16))
task_entry.bind("<Return>", lambda event: process_task())

# Create status label with StringVar
status_text_var = tk.StringVar()
status_text_var.set("Ieraksi codeforces ID un spied AIZIET!")
status_label = tk.Label(root, textvariable=status_text_var, font=("Helvetica", 12))
status_label.pack(pady=5)

# Add progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill="x", padx=20)

def process_task_just_sort():
    process_task(True)

goButton = tk.Button(root, text="AIZIET!", command=process_task, font=("Helvetica", 16))
goButton.pack(pady=10)
sortButton = tk.Button(root, text="Tikai sakārtot", command=process_task_just_sort, font=("Helvetica", 10))
sortButton.pack(pady=10)

root.mainloop()
