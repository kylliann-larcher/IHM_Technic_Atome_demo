
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import pandas as pd
import os

from data.data_loader import load_csv
from ui.statistics_window import StatisticsWindow
from ui.visualizer_window import VisualizerWindow
from ui.comparator_window import ComparatorWindow


class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Multi-Fichiers CSV")
        self.datasets = {}
        self.current_dataset_name = None
        self.current_data = None
        self.separator = tk.StringVar(value=',')
        self.sort_state = {}
        self.current_sorted_column = None

        self.setup_ui()

    def setup_ui(self):
        # Ligne de chargement
        self.file_selector = ttk.Combobox(self.root, state="readonly")
        self.file_selector.grid(row=0, column=0, padx=5, pady=5)
        self.file_selector.bind("<<ComboboxSelected>>", self.select_dataset)

        tk.Button(self.root, text="Ajouter un fichier CSV", command=self.add_csv_file).grid(row=0, column=1, padx=5)
        tk.Label(self.root, text="Séparateur :").grid(row=0, column=2)
        tk.Entry(self.root, textvariable=self.separator, width=5).grid(row=0, column=3)

        # Boutons d'action
        self.visual_button = tk.Button(self.root, text="Visualisation avancée", command=self.open_visualizer)
        self.visual_button.grid(row=0, column=4, padx=5)
        self.visual_button.grid_remove()

        self.stats_button = tk.Button(self.root, text="Statistiques avancées", command=self.show_statistics)
        self.stats_button.grid(row=0, column=5, padx=5)
        self.stats_button.grid_remove()

        self.add_button = tk.Button(self.root, text="Ajouter des données", command=self.add_data)
        self.add_button.grid(row=0, column=6, padx=5)
        self.add_button.grid_remove()

        self.compare_button = tk.Button(self.root, text="Comparer les données", command=self.open_comparator)
        self.compare_button.grid(row=0, column=7, padx=5)

        # Tableau
        self.table = ttk.Treeview(self.root)
        self.table.grid(row=1, column=0, columnspan=7, padx=10, pady=10)

    def add_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            sep = self.separator.get()
            df = load_csv(file_path, sep)
            name = os.path.basename(file_path)

            self.datasets[name] = df
            self.file_selector['values'] = list(self.datasets.keys())
            self.file_selector.set(name)
            self.select_dataset()

            messagebox.showinfo("Succès", f"Fichier '{name}' chargé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du chargement : {e}")

    def select_dataset(self, event=None):
        name = self.file_selector.get()
        if name and name in self.datasets:
            self.current_dataset_name = name
            self.current_data = self.datasets[name]
            self.display_data()
            self.add_button.grid()
            self.stats_button.grid()
            self.visual_button.grid()

    def display_data(self):
        if self.current_data is None:
            return

        self.table.delete(*self.table.get_children())
        self.table["columns"] = list(self.current_data.columns)
        self.table["show"] = "headings"

        for col in self.current_data.columns:
            header_text = col
            if col == self.current_sorted_column:
                ascending = self.sort_state.get(col, True)
                header_text += " ▲" if ascending else " ▼"
            self.table.heading(col, text=header_text, command=lambda c=col: self.sort_by_column(c))

        for _, row in self.current_data.iterrows():
            self.table.insert("", "end", values=list(row))

    def open_comparator(self):
        if len(self.datasets) < 2:
            messagebox.showwarning("Comparer", "Ajoutez au moins deux fichiers pour comparer.")
            return

        ComparatorWindow(self.root, self.datasets)

    def add_data(self):
        if self.current_data is None:
            return

        new_row = {}
        for col in self.current_data.columns:
            value = simpledialog.askstring("Ajouter une donnée", f"Valeur pour '{col}' :")
            if value is None:
                return
            new_row[col] = value

        self.datasets[self.current_dataset_name] = pd.concat(
            [self.current_data, pd.DataFrame([new_row])], ignore_index=True
        )
        self.current_data = self.datasets[self.current_dataset_name]
        self.display_data()

    def sort_by_column(self, column):
        if self.current_data is None:
            return

        ascending = self.sort_state.get(column, True)
        try:
            self.current_data[column] = pd.to_numeric(self.current_data[column], errors='ignore')
        except:
            pass

        self.current_data = self.current_data.sort_values(by=column, ascending=ascending, ignore_index=True)
        self.sort_state[column] = not ascending
        self.current_sorted_column = column
        self.display_data()

    def show_statistics(self):
        if self.current_data is None:
            return
        StatisticsWindow(self.root, self.current_data.copy())

    def open_visualizer(self):
        if self.current_data is None:
            return
        VisualizerWindow(self.root, self.datasets)



def launch_gui():
    root = tk.Tk()
    root.geometry("1200x650")
    app = DashboardApp(root)
    root.mainloop()
