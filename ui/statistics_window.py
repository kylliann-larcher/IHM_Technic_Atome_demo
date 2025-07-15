import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors


class StatisticsWindow:
    def __init__(self, master, data):
        self.data = data.select_dtypes(include='number')
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
        cursor = mplcursors.cursor(ax.containers[0], hover=True)
        @cursor.connect("add")
        def on_add(sel):
            col_index = sel.index
            label = means.index[col_index]
            value = means.iloc[col_index]
            sel.annotation.set_text(f"{label} : {value:.3f}")

    def plot_median_box(self, ax):
        sns.boxplot(data=self.data, ax=ax, orient="h", palette="Set2")
        ax.set_title("Médiane et dispersion (Boxplot)")
        mplcursors.cursor(ax.artists, hover=True)

    def plot_std(self, ax):
        stds = self.data.std().sort_values()
        stds.plot(kind='bar', ax=ax, color='coral')
        ax.set_title("Écart-type par colonne")
        ax.set_ylabel("Valeur d'écart-type")
        cursor = mplcursors.cursor(ax.containers[0], hover=True)
        @cursor.connect("add")
        def on_add(sel):
            col_index = sel.index
            label = stds.index[col_index]
            value = stds.iloc[col_index]
            sel.annotation.set_text(f"{label} : {value:.3f}")

    def plot_missing_heatmap(self, ax):
        sns.heatmap(self.data.isnull(), cbar=False, yticklabels=False, cmap="Reds", ax=ax)
        ax.set_title("Carte des valeurs manquantes")

    def plot_histograms(self, ax):
        self.data.hist(ax=ax)
        ax.set_title("Histogrammes combinés")
