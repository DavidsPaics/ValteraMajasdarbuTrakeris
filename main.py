import requests
import re
import tkinter as tk
from tkinter import messagebox

def get_users_who_solved(users, problem_id):
    completed_users = []

    for user in users:
        url = f"https://codeforces.com/api/user.status?handle={user}&from=1&count=1000"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to retrieve data for {user}.")
            continue
        
        submissions = response.json()
        if submissions['status'] != 'OK':
            print(f"Error with user {user}'s data.")
            continue

        for submission in submissions['result']:
            if (str(submission['problem']['contestId']) + str(submission['problem']['index']) == problem_id and
                submission['verdict'] == 'OK'):
                completed_users.append(user)
                break

    return completed_users

def process_task():
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
                raise Exception("Malformed Majasdarbi.txt",)
            scores[x[0]] = [int(x[1]), (x[2][1:-1] if len(x) > 2 else '+0')]

    problem_id = task_entry.get().upper().replace(" ", "")
    solved_users = get_users_who_solved(users, problem_id)
    
    if not "Valters07" in solved_users:
        messagebox.showwarning("Šausmas","Pats Valters nemaz nav izpildījis mājasdarbu!")
        
        
    messagebox.showinfo("Nu gan jauki","Šodien mājasdarbu izpildīja:\n" + '\n'.join(solved_users))
    
    for user in solved_users:
        if user in scores:
            scores[user][0] += 1
        else:
            scores[user] = [1, '+0']
    
    sorted_scores = sorted(
        scores.items(), 
        key=lambda item: item[1][0] + (int("".join(re.findall(r"\d", item[1][1]))) * 0.99999999999), 
        reverse=True
    )

    out = ""
    for score in sorted_scores:
        out += score[0] + " - " + str(score[1][0]) + " " + ("" if score[1][1] == '+0' else "(" + score[1][1] + ')') + "\n"

    # Write updated scores to file
    with open("data/majasdarbi.txt", 'w') as f_out:
        f_out.write(out)
        
    exit()

root = tk.Tk()
root.title("Valtera superīgā mājasdarbu programma")
root.geometry("400x200") 

tk.Label(root, text="Codeforces ID:", font=("Helvetica", 16)).pack(pady=10)
task_entry = tk.Entry(root)
task_entry.pack(pady=5)
task_entry.config(font=("Helvetica", 16))
task_entry.bind("<Return>", lambda event: process_task())
tk.Button(root, text="AIZIET!", command=process_task, font=("Helvetica", 16)).pack(pady=10)

root.mainloop()
