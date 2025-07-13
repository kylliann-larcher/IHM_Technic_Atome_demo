import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors


class StatisticsWindow:
    def __init__(self, master, data):
        self.data = data.select_dtypes(include='number')  # Numériques uniquement
        self.window = tk.Toplevel(master)
        self.window.title("Statistiques avancées")
        self.window.geometry("1000x700")
        self.setup_ui()

    def setup_ui(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True)

        self.add_stat_tab(notebook, "Moyennes", self.plot_mean)
        self.add_stat_tab(notebook, "Médianes", self.plot_median_box)
        self.add_stat_tab(notebook, "Écart-type", self.plot_std)
        self.add_stat_tab(notebook, "Valeurs manquantes", self.plot_missing_heatmap)
        self.add_stat_tab(notebook, "Histogrammes", self.plot_histograms)

    def add_stat_tab(self, notebook, title, plot_func):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)

        fig = plt.Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        plot_func(ax)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_mean(self, ax):
        means = self.data.mean().sort_values()
        means.plot(kind='barh', ax=ax, color='skyblue')
        ax.set_title("Moyenne par colonne")
        ax.set_xlabel("Valeur moyenne")
        mplcursors.cursor(ax.containers[0], hover=True)

    def plot_median_box(self, ax):
        sns.boxplot(data=self.data, ax=ax, orient="h", palette="Set2")
        ax.set_title("Médiane et dispersion (Boxplot)")
        mplcursors.cursor(ax.artists, hover=True)
    def plot_std(self, ax):
        stds = self.data.std().sort_values()
        stds.plot(kind='bar', ax=ax, color='coral')
        ax.set_title("Écart-type par colonne")
        ax.set_ylabel("Valeur d'écart-type")
        mplcursors.cursor(ax.containers[0], hover=True)

    def plot_missing_heatmap(self, ax):
        sns.heatmap(self.data.isnull(), cbar=False, yticklabels=False, cmap="Reds", ax=ax)
        ax.set_title("Carte des valeurs manquantes")

    def plot_histograms(self, ax):
        self.window.update()
        fig, axs = plt.subplots(nrows=min(4, len(self.data.columns)), ncols=1,
                                figsize=(8, 2 * len(self.data.columns)), dpi=100)

        if len(self.data.columns) == 1:
            axs = [axs]  # single axis

        for i, col in enumerate(self.data.columns[:len(axs)]):
            sns.histplot(self.data[col].dropna(), ax=axs[i], kde=True, color='steelblue')
            axs[i].set_title(f"Histogramme - {col}")

        fig.tight_layout()

        # Remplacer le widget dans l'onglet
        tab = ttk.Frame(self.window)
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.window.children['!notebook'].add(tab, text="Histogrammes (détaillés)")
