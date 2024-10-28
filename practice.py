import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize the main application window
root = tk.Tk()
root.title("Sales Analysis Dashboard")
root.geometry("800x600")

# Define global variable for data
data = None

# Function to load CSV file
def load_data():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        data = pd.read_csv(file_path)
        # Ensure 'Sales' column is numeric
        data['Sales'] = pd.to_numeric(data['Sales'], errors='coerce')
        messagebox.showinfo("Data Load", "Data loaded successfully!")
    else:
        messagebox.showerror("Data Load Error", "No file selected or file could not be loaded.")

# Function to clear previous plots
def clear_plots():
    for widget in root.pack_slaves():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

# Function to plot sales by month
def plot_sales_by_month():
    if data is None:
        messagebox.showerror("Data Error", "No data loaded.")
        return
    
    # Assume the dataset has columns 'Date' and 'Sales'
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month'] = data['Date'].dt.month
    monthly_sales = data.groupby('Month')['Sales'].sum()

    # Clear previous plots
    clear_plots()

    # Plotting
    fig, ax = plt.subplots()
    monthly_sales.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Sales by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    
    # Embed the plot in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to plot sales by product
def plot_sales_by_product():
    if data is None:
        messagebox.showerror("Data Error", "No data loaded.")
        return
    
    # Assume the dataset has columns 'Product' and 'Sales'
    product_sales = data.groupby('Product')['Sales'].sum()

    # Clear previous plots
    clear_plots()

    # Plotting
    fig, ax = plt.subplots()
    product_sales.plot(kind='bar', ax=ax, color='lightgreen')
    ax.set_title("Sales by Product")
    ax.set_xlabel("Product")
    ax.set_ylabel("Sales")
    
    # Embed the plot in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to display total sales
def display_total_sales():
    if data is None:
        messagebox.showerror("Data Error", "No data loaded.")
        return
    
    total_sales = data['Sales'].sum()
    messagebox.showinfo("Total Sales", f"Total Sales: ${total_sales:.2f}")

# Buttons for the dashboard
btn_load = tk.Button(root, text="Load Data", command=load_data)
btn_load.pack(pady=10)

btn_sales_by_month = tk.Button(root, text="Plot Sales by Month", command=plot_sales_by_month)
btn_sales_by_month.pack(pady=10)

btn_sales_by_product = tk.Button(root, text="Plot Sales by Product", command=plot_sales_by_product)
btn_sales_by_product.pack(pady=10)

btn_total_sales = tk.Button(root, text="Display Total Sales", command=display_total_sales)
btn_total_sales.pack(pady=10)

# Run the application
root.mainloop()
