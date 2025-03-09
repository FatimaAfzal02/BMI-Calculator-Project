import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Function to determine weight category
def get_weight_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Function to calculate BMI
def calculate_bmi():
    try:
        gender = gender_var.get()
        name = name_entry.get().strip()
        age = int(age_entry.get())  # Get age input
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # Convert cm to meters

        if weight <= 0 or height <= 0 or age <= 0 or not name:
            raise ValueError("Invalid input! Make sure all fields are filled correctly.")

        bmi = round(weight / (height ** 2), 1)
        category = get_weight_category(bmi)

        save_data(gender, name, age, weight, height, bmi, category)

        bmi_label.config(text=f"BMI: {bmi} ({category})")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Function to save BMI data to a CSV file
def save_data(gender, name, age, weight, height, bmi, category):
    filename = "bmi_data.csv"
    columns = ["Gender", "Name", "Age", "Weight", "Height", "BMI", "Category"]

    new_data = pd.DataFrame([[gender, name, age, weight, height, bmi, category]], columns=columns)

    if os.path.exists(filename):
        existing_data = pd.read_csv(filename)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data  # Create new file if none exists

    updated_data.to_csv(filename, index=False)

# Function to view stored data in a pop-up window
def view_history():
    filename = "bmi_data.csv"

    try:
        df = pd.read_csv(filename)

        if df.empty:
            messagebox.showinfo("History", "No previous BMI records found.")
            return

        history_text = df.to_string(index=False, justify="center")
        history_window = tk.Toplevel(root)
        history_window.title("BMI History")

        text_widget = tk.Text(history_window, wrap="word", font=("Courier", 12))
        text_widget.insert("1.0", history_text)
        text_widget.pack(expand=True, fill="both")

    except FileNotFoundError:
        messagebox.showinfo("History", "No data found. Calculate BMI first.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load history: {e}")

# Function to plot BMI trend (bar chart)
def plot_trend():
    filename = "bmi_data.csv"

    try:
        df = pd.read_csv(filename)

        if df.empty:
            messagebox.showinfo("Trend", "No data available to show trend.")
            return
        
        plt.figure(figsize=(6, 4))
        plt.bar(df["Name"], df["BMI"], color="blue")
        plt.xlabel("Name")
        plt.ylabel("BMI")
        plt.title("BMI Trend Analysis")
        plt.xticks(rotation=45)
        plt.show()

    except FileNotFoundError:
        messagebox.showinfo("Trend", "No data available.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not plot trend: {e}")

# Create GUI
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("300x550")

# Gender Selection
tk.Label(root, text="Gender:").pack()
gender_var = tk.StringVar(value="Male")  # Default value
male_radio = tk.Radiobutton(root, text="Male", variable=gender_var, value="Male")
female_radio = tk.Radiobutton(root, text="Female", variable=gender_var, value="Female")
male_radio.pack()
female_radio.pack()

# Name
tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Age
tk.Label(root, text="Age:").pack()
age_entry = tk.Entry(root)
age_entry.pack()

# Weight
tk.Label(root, text="Weight (kg):").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

# Height
tk.Label(root, text="Height (cm):").pack()
height_entry = tk.Entry(root)
height_entry.pack()

# Calculate BMI Button
calc_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calc_button.pack()

# BMI Label
bmi_label = tk.Label(root, text="BMI: ")
bmi_label.pack()

# View History Button
history_button = tk.Button(root, text="View History", command=view_history)
history_button.pack()

# Show Trend Button
trend_button = tk.Button(root, text="Show Trend", command=plot_trend)
trend_button.pack()

# Run the application
root.mainloop()
