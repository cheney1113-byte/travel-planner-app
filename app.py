from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, scrolledtext


class Trip:
    """Simple trip planner domain model."""

    def __init__(self, name: str, total_days: int) -> None:
        self.name = name.strip()
        self.total_days = total_days
        self.itinerary: dict[int, str] = {}

    def add_activity(self, day: int, activity: str) -> None:
        if day < 1 or day > self.total_days:
            raise ValueError(f"Day must be between 1 and {self.total_days}.")
        clean_activity = activity.strip()
        if not clean_activity:
            raise ValueError("Activity cannot be empty.")
        self.itinerary[day] = clean_activity

    def get_full_plan(self) -> str:
        lines = [f"Travel Plan: {self.name}", f"Total Days: {self.total_days}"]
        for day in range(1, self.total_days + 1):
            activity = self.itinerary.get(day, "(No plan yet)")
            lines.append(f"Day {day}: {activity}")
        return "\n".join(lines)


class TripPlannerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Travel Planner v0.2")
        self.root.geometry("620x520")

        self.trip: Trip | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="旅行名称:").grid(row=0, column=0, sticky="w", pady=4)
        self.name_entry = tk.Entry(frame, width=45)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=4)

        tk.Label(frame, text="日期/天数 (例如 5):").grid(row=1, column=0, sticky="w", pady=4)
        self.days_entry = tk.Entry(frame, width=45)
        self.days_entry.grid(row=1, column=1, sticky="ew", pady=4)

        tk.Label(frame, text="第几天:").grid(row=2, column=0, sticky="w", pady=4)
        self.day_entry = tk.Entry(frame, width=45)
        self.day_entry.grid(row=2, column=1, sticky="ew", pady=4)

        tk.Label(frame, text="每日行程内容:").grid(row=3, column=0, sticky="nw", pady=4)
        self.activity_text = tk.Text(frame, width=45, height=5)
        self.activity_text.grid(row=3, column=1, sticky="ew", pady=4)

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=4, column=1, sticky="w", pady=8)

        self.add_btn = tk.Button(btn_frame, text="添加行程", command=self.add_activity)
        self.add_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.show_btn = tk.Button(btn_frame, text="显示完整计划", command=self.show_plan)
        self.show_btn.pack(side=tk.LEFT)

        tk.Label(frame, text="完整旅行计划:").grid(row=5, column=0, sticky="nw", pady=4)
        self.output_area = scrolledtext.ScrolledText(frame, width=60, height=15, state=tk.DISABLED)
        self.output_area.grid(row=5, column=1, sticky="nsew", pady=4)

        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(5, weight=1)

    def _ensure_trip(self) -> Trip:
        name = self.name_entry.get().strip()
        days_raw = self.days_entry.get().strip()

        if not name:
            raise ValueError("请先输入旅行名称。")
        if not days_raw.isdigit() or int(days_raw) <= 0:
            raise ValueError("请输入有效的正整数天数。")

        days = int(days_raw)
        if self.trip is None or self.trip.name != name or self.trip.total_days != days:
            self.trip = Trip(name=name, total_days=days)
        return self.trip

    def add_activity(self) -> None:
        try:
            trip = self._ensure_trip()
            day_raw = self.day_entry.get().strip()
            if not day_raw.isdigit():
                raise ValueError("请输入要添加行程的天数（正整数）。")
            day = int(day_raw)
            activity = self.activity_text.get("1.0", tk.END).strip()
            trip.add_activity(day, activity)
            messagebox.showinfo("成功", f"已添加第 {day} 天行程。")
            self.activity_text.delete("1.0", tk.END)
        except ValueError as exc:
            messagebox.showerror("输入错误", str(exc))

    def show_plan(self) -> None:
        try:
            trip = self._ensure_trip()
            content = trip.get_full_plan()
            self.output_area.config(state=tk.NORMAL)
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, content)
            self.output_area.config(state=tk.DISABLED)
        except ValueError as exc:
            messagebox.showerror("输入错误", str(exc))


def main() -> None:
    root = tk.Tk()
    app = TripPlannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()