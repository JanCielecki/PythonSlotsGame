import random
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

balance = 100  # Inicjalizacja zmiennej na początku
symbols = ['🍒', '🍉', '🍋', '🔔', '⭐']

def spin_row():
    return [random.choice(symbols) for _ in range(3)]

def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == '🍒':
            return bet * 3
        elif row[0] == '🍉':
            return bet * 4
        elif row[0] == '🍋':
            return bet * 5
        elif row[0] == '🔔':
            return bet * 10
        elif row[0] == '⭐':
            return bet * 20
    return 0

def animate_spin(counter=0, final_result=None, bet=0):
    if counter < 20:  # Ilość "obrotów" animacji
        row = spin_row()  # Generowanie losowego rzędu
        slot_label.config(text=" | ".join(row))  # Wyświetlanie tymczasowego rzędu
        counter += 1
        root.after(100, animate_spin, counter, final_result, bet)  # Powtarzaj co 100 ms
    else:
        slot_label.config(text=" | ".join(final_result))  # Wyświetl ostateczny wynik
        payout = get_payout(final_result, bet)
        if payout > 0:
            messagebox.showinfo("Congratulations!", f"You won ${payout}!")
            global balance
            balance += payout
        else:
            messagebox.showinfo("Try Again", "Sorry, you lost this round.")
        balance_label.config(text=f"Balance: ${balance}")

        if balance <= 0:
            messagebox.showinfo("Game Over", "Your balance is $0. Game over!")
            root.quit()

def spin():
    global balance
    bet = bet_entry.get()

    if not bet.isdigit():
        messagebox.showerror("Invalid Bet", "Please enter a valid number.")
        return

    bet = int(bet)

    if bet > balance:
        messagebox.showerror("Insufficient Funds", "You don't have enough balance.")
        return

    if bet <= 0:
        messagebox.showerror("Invalid Bet", "Bet must be greater than 0.")
        return

    balance -= bet
    balance_label.config(text=f"Balance: ${balance}")

    final_result = spin_row()  # Ostateczny wynik po zakończeniu animacji
    animate_spin(final_result=final_result, bet=bet)  # Uruchom animację

def quit_game():
    root.quit()

# GUI Setup
root = tk.Tk()
root.title("Python Slots")
root.geometry("500x400")
root.configure(bg="#17e64b")

# Wczytanie obrazów z poprawnymi nazwami i zmniejszenie rozmiaru
spin_img = Image.open("spin.png")
spin_img_resized = spin_img.resize((100, 50))  # Zmniejszenie do 100x50 pikseli
spin_photo = ImageTk.PhotoImage(spin_img_resized)

quit_img = Image.open("quit.png")
quit_img_resized = quit_img.resize((100, 50))  # Zmniejszenie do 100x50 pikseli
quit_photo = ImageTk.PhotoImage(quit_img_resized)

# Style configuration
style = ttk.Style()
style.configure("TButton", font=('Helvetica', 14), padding=10)
style.configure("TLabel", font=('Helvetica', 14), background="#2c3e50", foreground="white")
style.configure("Header.TLabel", font=('Helvetica', 24, 'bold'), background="#1abc9c", foreground="white")

# Header Frame
header_frame = tk.Frame(root, bg="#1abc9c", padx=20, pady=10)
header_frame.pack(fill="x")

header_label = ttk.Label(header_frame, text="🎰 Python Slots 🎰", style="Header.TLabel")
header_label.pack()

# Slot Frame
slot_frame = tk.Frame(root, bg="#34495e", padx=20, pady=20, relief="raised", bd=5)
slot_frame.pack(pady=20)

slot_label = ttk.Label(slot_frame, text="🍒 | 🍉 | 🍋", font=('Helvetica', 36), style="TLabel")
slot_label.pack()

# Balance Frame
balance_frame = tk.Frame(root, bg="#2c3e50", pady=10)
balance_frame.pack()

balance_label = ttk.Label(balance_frame, text=f"Balance: ${balance}", style="TLabel")
balance_label.pack()

# Bet Frame
bet_frame = tk.Frame(root, bg="#2c3e50", pady=10)
bet_frame.pack()

bet_label = ttk.Label(bet_frame, text="Enter your bet:", style="TLabel")
bet_label.pack()

bet_entry = ttk.Entry(bet_frame, font=('Helvetica', 14), width=10)
bet_entry.pack(pady=5)

# Button Frame
button_frame = tk.Frame(root, bg="#2c3e50", pady=20)
button_frame.pack()

# Dodanie przycisków z obrazkami
spin_button = tk.Button(button_frame, image=spin_photo, command=spin)
spin_button.grid(row=0, column=0, padx=10)

quit_button = tk.Button(button_frame, image=quit_photo, command=quit_game)
quit_button.grid(row=0, column=1, padx=10)

root.mainloop()
