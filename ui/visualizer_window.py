import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors

class VisualizerWindow:
    def __init__(self, master, dataset_dict):
        self.datasets = dataset_dict
        self.current_df = list(dataset_dict.values())[0]
        self.window = tk.Toplevel(master)
        self.window.title("Visualisation avancée (multi-sources)")
        self.window.geometry("1000x600")
        self.setup_ui()

    def setup_ui(self):
        frame_top = tk.Frame(self.window)
        frame_top.pack(side="top", fill="x", padx=10, pady=10)

        tk.Label(frame_top, text="Dataset :").pack(side="left")
        self.dataset_selector = ttk.Combobox(frame_top, values=list(self.datasets.keys()), state="readonly")
        self.dataset_selector.current(0)
        self.dataset_selector.pack(side="left", padx=5)
        self.dataset_selector.bind("<<ComboboxSelected>>", self.switch_dataset)

        tk.Label(frame_top, text="X :").pack(side="left")
        self.x_column = ttk.Combobox(frame_top, state="readonly")
        self.x_column.pack(side="left", padx=5)

        tk.Label(frame_top, text="Y :").pack(side="left")
        self.y_column = ttk.Combobox(frame_top, state="readonly")
        self.y_column.pack(side="left", padx=5)

        self.plot_type = ttk.Combobox(frame_top, values=["Bar", "Ligne", "Nuage de points", "Camembert"], state="readonly")
        self.plot_type.set("Bar")
        self.plot_type.pack(side="left", padx=5)

        tk.Button(frame_top, text="Tracer", command=self.plot).pack(side="left", padx=10)

        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.refresh_column_options()

    def switch_dataset(self, event=None):
        selected_name = self.dataset_selector.get()
        self.current_df = self.datasets[selected_name]
        self.refresh_column_options()

    def refresh_column_options(self):
        cols = self.current_df.columns.tolist()
        self.x_column['values'] = cols
        self.y_column['values'] = cols
        if cols:
            self.x_column.set(cols[0])
            if len(cols) > 1:
                self.y_column.set(cols[1])
            else:
                self.y_column.set(cols[0])

    def plot(self):
        x_col = self.x_column.get()
        y_col = self.y_column.get()
        kind = self.plot_type.get()

        self.ax.clear()

        try:
            df = self.current_df.copy()
            if kind == "Bar":
                df.plot.bar(x=x_col, y=y_col, ax=self.ax)
            elif kind == "Ligne":
                df.plot.line(x=x_col, y=y_col, ax=self.ax)
            elif kind == "Nuage de points":
                df.plot.scatter(x=x_col, y=y_col, ax=self.ax)
            elif kind == "Camembert":
                counts = df[x_col].value_counts()
                self.ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%")

            self.ax.set_title(f"{kind} - {x_col} vs {y_col}")
            self.canvas.draw()

            if kind in ["Bar", "Ligne"]:
                for container in self.ax.containers:
                    mplcursors.cursor(container, hover=True)
            elif kind == "Nuage de points":
                mplcursors.cursor(self.ax.collections, hover=True)
            elif kind == "Camembert":
                mplcursors.cursor(self.ax.patches, hover=True)

        except Exception as e:
            self.ax.text(0.5, 0.5, f"Erreur : {e}", ha="center", va="center")
            self.canvas.draw()
