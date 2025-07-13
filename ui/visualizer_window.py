import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VisualizerWindow:
    def __init__(self, master, data):
        self.data = data
        self.window = tk.Toplevel(master)
        self.window.title("Visualisation avancée")
        self.window.geometry("1000x600")
        self.setup_ui()

    def setup_ui(self):
        frame_top = tk.Frame(self.window)
        frame_top.pack(side="top", fill="x", padx=10, pady=10)

        tk.Label(frame_top, text="X :").pack(side="left")
        self.x_column = ttk.Combobox(frame_top, values=self.data.columns.tolist(), state="readonly")
        self.x_column.pack(side="left", padx=5)

        tk.Label(frame_top, text="Y :").pack(side="left")
        self.y_column = ttk.Combobox(frame_top, values=self.data.columns.tolist(), state="readonly")
        self.y_column.pack(side="left", padx=5)

        self.plot_type = ttk.Combobox(frame_top, values=["Bar", "Ligne", "Nuage de points", "Camembert"], state="readonly")
        self.plot_type.set("Bar")
        self.plot_type.pack(side="left", padx=5)

        tk.Button(frame_top, text="Tracer", command=self.plot).pack(side="left", padx=10)

        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot(self):
        x_col = self.x_column.get()
        y_col = self.y_column.get()
        plot_kind = self.plot_type.get()

        self.ax.clear()

        if plot_kind == "Bar":
            self.data.plot.bar(x=x_col, y=y_col, ax=self.ax)
        elif plot_kind == "Ligne":
            self.data.plot.line(x=x_col, y=y_col, ax=self.ax)
        elif plot_kind == "Nuage de points":
            self.data.plot.scatter(x=x_col, y=y_col, ax=self.ax)
        elif plot_kind == "Camembert":
            counts = self.data[x_col].value_counts()
            self.ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%")

        self.ax.set_title(f"{plot_kind} - {x_col} vs {y_col}" if y_col else f"{plot_kind} - {x_col}")
        self.canvas.draw()
