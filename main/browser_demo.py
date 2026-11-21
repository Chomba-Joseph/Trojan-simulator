
import tkinter as tk
import logging
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(LOG_DIR / "events.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

MAX_TABS = 10000
INTERVAL = 1
URLS = [
    "https://www.youtube.com/",
    "https://www.msn.com/en-xl?bundles=staging"
]

count = 0
timer_id = None
running = False

root = tk.Tk()
root.title("Browser tab overload virus DEMO")
root.geometry("1360x760")
root.resizable(True, True)

tk.Label(
    root,
    text="Browser tab overload virus DEMO",
    font=("Arial", 16, "bold")
).pack(pady=20)

counter = tk.Label(
    root,
    text=f"YouTube and MSN tabs opened: 0 / {MAX_TABS}",
    font=("Arial", 13)
)
counter.pack(pady=15)

status = tk.Label(
    root,
    text="Status: Ready",
    font=("Arial", 11),
    fg="green"
)
status.pack(pady=10)


def update_counter():
    counter.config(
        text=f"YouTube and MSN tabs opened: {count} / {MAX_TABS}"
    )


def stop_demo():
    global timer_id, running

    running = False

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    status.config(text="Status: Stopped", fg="red")
    logging.info("Demonstration stopped.")


def open_youtube():
    global count, timer_id, running

    if not running:
        return

    if count >= MAX_TABS:
        running = False
        timer_id = None
        status.config(text="Status: Completed", fg="blue")
        logging.info("Demonstration completed.")
        return

    success = webbrowser.open_new_tab(URLS[count % len(URLS)])

    if success:
        count += 1
        update_counter()
        logging.info(f"YouTube and MSN tabs opened: {count}")

    timer_id = root.after(INTERVAL, open_youtube)


def start_demo():
    global running

    if running:
        return

    if count >= MAX_TABS:
        status.config(text="Reset before restarting.", fg="red")
        return

    running = True
    status.config(text="Status: Opening YouTube and MSN tabs", fg="green")

    open_youtube()


def reset_demo():
    global count

    stop_demo()
    count = 0
    update_counter()
    status.config(text="Status: Ready", fg="green")


frame = tk.Frame(root)
frame.pack(pady=20)

tk.Button(
    frame,
    text="Start",
    width=10,
    command=start_demo
).grid(row=0, column=0, padx=5)

tk.Button(
    frame,
    text="Stop",
    width=10,
    command=stop_demo
).grid(row=0, column=1, padx=5)

tk.Button(
    frame,
    text="Reset",
    width=10,
    command=reset_demo
).grid(row=0, column=2, padx=5)


def close_application():
    stop_demo()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_application)
root.mainloop()