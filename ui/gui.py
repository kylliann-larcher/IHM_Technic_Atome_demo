import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import pandas as pd
from data.data_loader import load_csv
from ui.statistics_window import StatisticsWindow
from ui.visualizer_window import VisualizerWindow
import os

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Power BI - Dashboard")
        self.data = None
        self.separator = tk.StringVar(value=',')
        self.sort_state = {}
        self.current_sorted_column = None

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Séparateur :").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.separator).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Charger CSV", command=self.load_csv_file).grid(row=0, column=2, padx=5)
        tk.Button(self.root, text="Visualiser les données", command=self.display_data).grid(row=0, column=3, padx=5)

        self.add_button = tk.Button(self.root, text="Ajouter des données", command=self.add_data)
        self.add_button.grid(row=0, column=4, padx=5)
        self.add_button.grid_remove()

        self.stats_button = tk.Button(self.root, text="Statistiques avancées", command=self.show_statistics)
        self.stats_button.grid(row=0, column=5, padx=5)
        self.stats_button.grid_remove()

        self.visual_button = tk.Button(self.root, text="Visualisation avancée", command=self.open_visualizer)
        self.visual_button.grid(row=0, column=6, padx=5)
        self.visual_button.grid_remove()

        self.table = ttk.Treeview(self.root)
        self.table.grid(row=1, column=0, columnspan=7, padx=10, pady=10)

    def load_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            sep = self.separator.get()
            self.data = load_csv(file_path, sep)
            messagebox.showinfo("Succès", "Fichier chargé avec succès !")
            self.display_data()
            self.add_button.grid()
            self.stats_button.grid()
            self.visual_button.grid()
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du chargement : {e}")

    def display_data(self):
        if self.data is None:
            messagebox.showwarning("Avertissement", "Aucune donnée à afficher.")
            return

        self.table.delete(*self.table.get_children())
        self.table["columns"] = list(self.data.columns)
        self.table["show"] = "headings"

        for col in self.data.columns:
            header_text = col
            if col == self.current_sorted_column:
                ascending = self.sort_state.get(col, True)
                header_text += " ▲" if ascending else " ▼"
            self.table.heading(col, text=header_text, command=lambda c=col: self.sort_by_column(c))

        for _, row in self.data.iterrows():
            self.table.insert("", "end", values=list(row))

    def add_data(self):
        if self.data is None:
            messagebox.showwarning("Avertissement", "Chargez un fichier d'abord.")
            return

        new_row = {}
        for col in self.data.columns:
            value = simpledialog.askstring("Ajouter une donnée", f"Valeur pour '{col}' :")
            if value is None:
                return
            new_row[col] = value

        self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
        self.display_data()

    def sort_by_column(self, column):
        if self.data is None:
            return

        ascending = self.sort_state.get(column, True)
        try:
            self.data[column] = pd.to_numeric(self.data[column], errors='ignore')
        except:
            pass

        self.data = self.data.sort_values(by=column, ascending=ascending, ignore_index=True)
        self.sort_state[column] = not ascending
        self.current_sorted_column = column
        self.display_data()

    def show_statistics(self):
        if self.data is None:
            messagebox.showwarning("Avertissement", "Aucune donnée chargée.")
            return
        StatisticsWindow(self.root, self.data.copy())

    def open_visualizer(self):
        if self.data is None:
            messagebox.showwarning("Avertissement", "Aucune donnée chargée.")
            return
        VisualizerWindow(self.root, self.data.copy())

def launch_gui():
    root = tk.Tk()
    root.geometry("1000x600")

    icon_path = os.path.join("assets", "logo.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    app = DashboardApp(root)
    root.mainloop()
