import os
try:
    import requests
except:
    print("Please install requests")
    exit()
import re, time
import tkinter as tk
from tkinter import messagebox, ttk

def get_users_who_solved(users, problem_id, progress_var, status_text_var):
    completed_users = []

    for i, user in enumerate(users):
        url = f"https://codeforces.com/api/user.status?handle={user}&from=1&count=125"
        retries = 3
        while(retries):
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
    # Read users from file
    with open("data/lietotaji.txt", 'r') as f:
        users = f.read().split('\n')
        
    # Read scores
    with open("data/majasdarbi.txt", 'r') as f:
        data = f.read().strip()
        tempscores = data.split('\n')
        with open("data/majasdarbi-backup.txt", 'w+') as f_backup:
            f_backup.write(data)
            
        scores = {}
        for s in tempscores:
            x = s.replace("- ", "")
            x = x.split(" ")
            if len(x) < 2 or len(x) > 3:
                print("Majasdarbi.txt ir kautkādas problēmas... Vajadzētu salabot!")
                messagebox.showerror("Opā!", "Majasdarbi.txt ir kautkādas problēmas... Vajadzētu salabot!")
                raise Exception("Malformed Majasdarbi.txt")
            scores[x[0]] = [int(x[1]), (x[2][1:-1] if len(x) > 2 else '+0')]
    if(not justSort):
        problem_id = task_entry.get().upper().replace(" ", "")
        solved_users = get_users_who_solved(users, problem_id, progress_var, status_text_var)
        
        # if not "Valters07" in solved_users:
        #     messagebox.showwarning("Šausmas", "Pats Valters nemaz nav izpildījis mājasdarbu!")
            
        if (solved_users):
            messagebox.showinfo("Nu gan jauki", f"Šodien mājasdarbu {problem_id} izpildīja:\n" + '\n'.join(solved_users))
        else:
            messagebox.showwarning("Šausmas", f"Šodien mājasdarbu {problem_id} izpildīja NEVIENS!!!!!")


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
        out += score[0] + " - " + str(score[1][0]) + " " + ("" if score[1][1] == '+0' or not score[1][1] else "(" + score[1][1] + ')') + "\n"

    # Write updated scores to file
    with open("data/majasdarbi.txt", 'w') as f_out:
        f_out.write(out)

    if (justSort):
        messagebox.showinfo("Super", "Darīts!")
    exit()

root = tk.Tk()
root.title("Valtera superīgā mājasdarbu programma")
root.geometry("400x300") 

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

tk.Button(root, text="AIZIET!", command=process_task, font=("Helvetica", 16)).pack(pady=10)
tk.Button(root, text="Tikai sakārtot", command=process_task_just_sort, font=("Helvetica", 10)).pack(pady=10)

root.mainloop()
