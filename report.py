import tkinter as tk

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =========================
# Functions
# =========================

def update_values():
    weight = float(weight_var.get())
    height = float(height_var.get())
    activity = activity_var.get()

    # ---------- BMI ----------
    if height == 0:
        bmi = 0
    else:
        height_m = height / 100
        bmi = weight / (height_m ** 2)

    bmi_label.config(text=f"{bmi:.1f}")

    # Refresh BMI bar
    for widget in bmi_bar_container.winfo_children():
        widget.destroy()

    bmi_fig = create_bmi_bar(bmi)
    bmi_canvas = FigureCanvasTkAgg(bmi_fig, master=bmi_bar_container)
    bmi_canvas.draw()
    bmi_canvas.get_tk_widget().pack()

    # ---------- Water Intake ----------
    base_water = weight * 0.033 * 1000
    extra = 0 if activity == "Low" else 300 if activity == "Normal" else 700
    water_total = base_water + extra

    water_label.config(text=f"{water_total:.0f} ml/day")

    # ---------- Summary ----------
    summary_label.config(
        text=(
            f"Weight: {weight} kg\n"
            f"Height: {height} cm\n"
            f"BMI: {bmi:.1f}\n"
            f"Water Intake: {water_total:.0f} ml/day"
        )
    )


def create_bmi_bar(bmi):
    colors = ['#3457D5', '#00B2B2', '#00D27F', '#FFB340', '#FF5A5A']
    bmi_range = [15, 16, 18.5, 25, 30, 40]

    fig, ax = plt.subplots(figsize=(5, 1))

    for i, color in enumerate(colors):
        ax.barh(
            0,
            bmi_range[i + 1] - bmi_range[i],
            left=bmi_range[i],
            color=color
        )

    bmi = max(15, min(bmi, 40))
    ax.axvline(bmi, color="black", linewidth=3)

    ax.set_xlim(15, 40)
    ax.axis('off')

    return fig


# =========================
# Main Window
# =========================

root = tk.Tk()
root.title("Health Report")
root.state("zoomed")
root.configure(bg="#F5F6FA")

# =========================
# Scrollable Layout
# =========================

canvas = tk.Canvas(root, bg="#F5F6FA", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#F5F6FA")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Mouse wheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)


# =========================
# Fonts & Card
# =========================

title_font = ("Segoe UI Semibold", 16)
label_font = ("Segoe UI", 12)
bold_font = ("Segoe UI", 14)

def card(master):
    return tk.Frame(master, bg="white", bd=1, relief="solid", padx=15, pady=15)


# =========================
# Weight Card
# =========================

weight_card = card(scrollable_frame)
weight_card.pack(padx=15, pady=10, fill="both")

tk.Label(weight_card, text="Weight", font=title_font, bg="white").pack(anchor="w")

weight_var = tk.StringVar(value="0")
height_var = tk.StringVar(value="0")

tk.Label(weight_card, text="Current Weight (kg)", font=label_font, bg="white").pack(anchor="w")
tk.Entry(weight_card, textvariable=weight_var, font=label_font).pack()

tk.Label(weight_card, text="Height (cm)", font=label_font, bg="white", pady=5).pack(anchor="w")
tk.Entry(weight_card, textvariable=height_var, font=label_font).pack()


# =========================
# BMI Card
# =========================

bmi_card = card(scrollable_frame)
bmi_card.pack(padx=15, pady=10, fill="both")

tk.Label(bmi_card, text="BMI", font=title_font, bg="white").pack(anchor="w")

bmi_label = tk.Label(bmi_card, text="0.0", font=bold_font, bg="white")
bmi_label.pack()

bmi_bar_container = tk.Frame(bmi_card, bg="white")
bmi_bar_container.pack(pady=10)


# =========================
# Water Intake Card
# =========================

water_card = card(scrollable_frame)
water_card.pack(padx=15, pady=10, fill="both")

tk.Label(water_card, text="Water Intake", font=title_font, bg="white").pack(anchor="w")

activity_var = tk.StringVar(value="Normal")

for text, value in [
    ("Low Activity", "Low"),
    ("Normal Activity", "Normal"),
    ("High Activity", "High")
]:
    tk.Radiobutton(
        water_card,
        text=text,
        variable=activity_var,
        value=value,
        bg="white",
        font=label_font
    ).pack(anchor="w")

water_label = tk.Label(water_card, text="0 ml/day", font=bold_font, bg="white")
water_label.pack(anchor="w", pady=5)


# =========================
# Summary Card
# =========================

summary_card = card(scrollable_frame)
summary_card.pack(padx=15, pady=10, fill="both")

tk.Label(summary_card, text="Summary", font=title_font, bg="white").pack(anchor="w")
summary_label = tk.Label(summary_card, text="", font=label_font, bg="white", justify="left")
summary_label.pack(anchor="w")


# =========================
# Update Button
# =========================

button_card = card(scrollable_frame)
button_card.pack(padx=20, pady=15, fill="x")

tk.Button(
    button_card,
    text="Update",
    command=update_values,
    bg="#0066FF",
    fg="white",
    activebackground="#0050D4",
    font=("Segoe UI", 12),
    bd=0,
    padx=20,
    pady=10
).pack(fill="x")


# Initial update
update_values()

root.mainloop()
