
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import mplcursors


class ComparatorWindow:
    def __init__(self, master, datasets: dict):
        self.datasets = {k: v.select_dtypes(include='number') for k, v in datasets.items()}
        self.window = tk.Toplevel(master)
        self.window.title("Comparaison des fichiers CSV")
        self.window.geometry("1200x700")
        self.setup_ui()

    def setup_ui(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True)

        self.add_tab(notebook, "Moyennes", self.plot_means)
        self.add_tab(notebook, "Écart-types", self.plot_std)
        self.add_tab(notebook, "Distributions", self.plot_distributions)
        self.add_tab(notebook, "Valeurs manquantes", self.plot_missing)
        self.add_tab(notebook, "Boxplots", self.plot_boxplots)

    def add_tab(self, notebook, title, plot_func):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)

        fig = plt.Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)
        plot_func(ax)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_means(self, ax):
        means_df = pd.DataFrame({name: df.mean() for name, df in self.datasets.items()})
        means_df.plot.bar(ax=ax)
        ax.set_title("Moyenne par colonne")
        ax.set_ylabel("Valeur")
        for container in ax.containers:
            mplcursors.cursor(container, hover=True)

    def plot_std(self, ax):
        std_df = pd.DataFrame({name: df.std() for name, df in self.datasets.items()})
        std_df.plot.bar(ax=ax)
        ax.set_title("Écart-type par colonne")
        ax.set_ylabel("Écart-type")
        for container in ax.containers:
            mplcursors.cursor(container, hover=True)

    def plot_distributions(self, ax):
        common_cols = set.intersection(*(set(df.columns) for df in self.datasets.values()))
        if not common_cols:
            ax.text(0.5, 0.5, "Aucune colonne commune", ha="center")
            return

        col = sorted(common_cols)[0]  # prendre la première colonne commune
        for name, df in self.datasets.items():
            sns.kdeplot(df[col], label=name, ax=ax, fill=True)

        ax.set_title(f"Distribution comparée - {col}")
        ax.legend()

    def plot_missing(self, ax):
        missing = pd.DataFrame({name: df.isnull().sum() for name, df in self.datasets.items()})
        missing.plot.bar(ax=ax)
        ax.set_title("Valeurs manquantes par fichier")
        ax.set_ylabel("Nombre de valeurs nulles")
        for container in ax.containers:
            mplcursors.cursor(container, hover=True)

    def plot_boxplots(self, ax):
        common_cols = set.intersection(*(set(df.columns) for df in self.datasets.values()))
        if not common_cols:
            ax.text(0.5, 0.5, "Aucune colonne commune", ha="center", va="center")
            return

        col = sorted(common_cols)[0]

        try:
            combined = pd.concat([
                pd.DataFrame({col: df[col].dropna(), "Fichier": name})
                for name, df in self.datasets.items() if col in df
            ])

            if combined.empty:
                ax.text(0.5, 0.5, "Pas de données valides pour le boxplot", ha="center", va="center")
                return

            sns.boxplot(data=combined, x="Fichier", y=col, ax=ax, palette="Set2")
            ax.set_title(f"Boxplot comparatif - {col}")
            mplcursors.cursor(ax.artists, hover=True)

        except Exception as e:
            ax.text(0.5, 0.5, f"Erreur : {e}", ha="center", va="center")
