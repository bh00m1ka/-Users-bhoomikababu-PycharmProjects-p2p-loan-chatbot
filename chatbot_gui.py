import asyncio
import json
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import websockets
import requests

API_BASE = "http://localhost:8000"

FORM_LABELS = {
    "en": {"id": "Borrower ID", "amount": "Amount", "purpose": "Purpose", "submit": "Submit Loan Request", "view": "View Requests"},
    "es": {"id": "ID del solicitante", "amount": "Monto", "purpose": "Propósito", "submit": "Enviar solicitud", "view": "Ver solicitudes"},
    "fr": {"id": "ID de l'emprunteur", "amount": "Montant", "purpose": "Objet", "submit": "Soumettre", "view": "Voir les demandes"},
}


class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan ChatBot App")

        self.tab_control = ttk.Notebook(root)

        self.chat_tab = ttk.Frame(self.tab_control)
        self.form_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.chat_tab, text='Chatbot')
        self.tab_control.add(self.form_tab, text='Loan Request')
        self.tab_control.pack(expand=1, fill='both')

        self.build_chat_tab()
        self.build_form_tab()

        self.connect_to_chatbot()

    def build_chat_tab(self):
        self.language = tk.StringVar(value="en")

        self.chat_display = scrolledtext.ScrolledText(self.chat_tab, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.chat_display.pack(padx=10, pady=10)

        self.language_selector = ttk.Combobox(self.chat_tab, textvariable=self.language)
        self.language_selector['values'] = ['en', 'es', 'fr']
        self.language_selector.pack(padx=10, pady=5)

        self.user_input = tk.Entry(self.chat_tab, width=50)
        self.user_input.pack(padx=10, pady=5)
        self.user_input.bind("<Return>", self.send_message)

    def build_form_tab(self):
        self.form_labels = {}

        # Form label translations
        labels = FORM_LABELS[self.language.get()]

        self.form_labels["id_lbl"] = ttk.Label(self.form_tab, text=labels["id"] + ":")
        self.form_labels["id_lbl"].grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.borrower_id = tk.Entry(self.form_tab)
        self.borrower_id.grid(row=0, column=1, padx=10)

        self.form_labels["amount_lbl"] = ttk.Label(self.form_tab, text=labels["amount"] + ":")
        self.form_labels["amount_lbl"].grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.amount = tk.Entry(self.form_tab)
        self.amount.grid(row=1, column=1, padx=10)

        self.form_labels["purpose_lbl"] = ttk.Label(self.form_tab, text=labels["purpose"] + ":")
        self.form_labels["purpose_lbl"].grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.purpose = tk.Entry(self.form_tab)
        self.purpose.grid(row=2, column=1, padx=10)

        self.submit_btn = ttk.Button(self.form_tab, text=labels["submit"], command=self.submit_loan)
        self.submit_btn.grid(row=3, column=0, columnspan=2, pady=5)

        self.view_btn = ttk.Button(self.form_tab, text=labels["view"], command=self.view_loans)
        self.view_btn.grid(row=4, column=0, columnspan=2, pady=5)

        self.results = scrolledtext.ScrolledText(self.form_tab, height=6, width=55, state='disabled')
        self.results.grid(row=5, column=0, columnspan=2, pady=10)

        self.language_selector.bind("<<ComboboxSelected>>", self.update_form_language)

    def update_form_language(self, event=None):
        labels = FORM_LABELS[self.language.get()]
        self.form_labels["id_lbl"].config(text=labels["id"] + ":")
        self.form_labels["amount_lbl"].config(text=labels["amount"] + ":")
        self.form_labels["purpose_lbl"].config(text=labels["purpose"] + ":")
        self.submit_btn.config(text=labels["submit"])
        self.view_btn.config(text=labels["view"])

    def display_message(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def view_loans(self):
        try:
            borrower_id = int(self.borrower_id.get())
            res = requests.get(f"{API_BASE}/api/borrower/loan-requests/{borrower_id}")
            loans = res.json()
            self.results.config(state='normal')
            self.results.delete('1.0', tk.END)
            for loan in loans:
                self.results.insert(tk.END, f"ID: {loan['id']}, Amount: {loan['amount']}, Purpose: {loan['purpose']}\n")
            self.results.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def send_message(self, event=None):
        message = self.user_input.get()
        if message and self.websocket:
            self.display_message("You", message)
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(json.dumps({"message": message, "language": self.language.get()})),
                self.loop
            )
            self.user_input.delete(0, tk.END)

    def connect_to_chatbot(self):
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_async_loop, daemon=True).start()

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.websocket_loop())

    async def websocket_loop(self):
        uri = "ws://localhost:8000/ws/chat"
        async with websockets.connect(uri) as websocket:
            self.websocket = websocket
            while True:
                try:
                    response = await websocket.recv()
                    data = json.loads(response)
                    self.display_message("Bot", data["response"])
                except Exception as e:
                    self.display_message("System", f"Error: {e}")
                    break

    def submit_loan(self):
        data = {
            "borrower_id": int(self.borrower_id.get()),
            "amount": float(self.amount.get()),
            "purpose": self.purpose.get()
        }

        try:
            res = requests.post(f"{API_BASE}/api/borrower/loan-request", json=data)
            if res.status_code == 200:
                messagebox.showinfo("Success", "Loan request submitted.")
                self.amount.delete(0, tk.END)
                self.purpose.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Failed: {res.json().get('detail')}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()


