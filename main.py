import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import sync_playwright

BASE_URL = "http://210.30.206.93:80"

def run_evaluation(student_id, password):
    with (sync_playwright() as p):
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(BASE_URL)
        page.locator("#un").fill(student_id)
        page.locator("#pd").fill(password)
        page.wait_for_timeout(1000)
        page.locator("#index_login_btn").click()
        page.wait_for_load_state("networkidle")
        page.locator("text=教学质量监控与评价平台").click()
        page.locator("text=学生评教").nth(1).click()
        page.locator("text=学生阶段评价").first.click()
        page.mouse.move(0, 0)
        page.locator("text=查看").click()
        page.wait_for_timeout(3000)
        table_rows = page.locator("tr.el-table__row")
        while True:
            current_row = table_rows.nth(0)
            page.wait_for_timeout(1000)
            try:
                current_row.locator("button:has-text('评价')").click(force=True, timeout=100)
            except:
                try:
                    current_row.locator("button:has-text('修改')").click(force=True, timeout=100)
                except:
                    break
            for j in range(10):
                page.locator("label:has-text('6')").nth(j).click()
            page.get_by_role("button", name="确认").click()
            page.get_by_role("button", name="确定").click()
        messagebox.showinfo("超级评教王", "所有课程已评教完成！\n浏览器窗口将保持10分钟以供查看。")
        page.wait_for_timeout(600000)
        browser.close()

def create_gui():
    def start_evaluation():
        start_button.config(state=tk.DISABLED, text="正在评教...")
        input_id = id_entry.get()
        input_password = password_entry.get()
        if not input_id or not input_password:
            messagebox.showwarning("输入错误", "学号和密码不能为空！")
            start_button.config(state=tk.NORMAL, text="开始评教")
            return
        run_evaluation(input_id, input_password)
        start_button.config(state=tk.NORMAL, text="开始评教")

    root = tk.Tk()
    root.title("超级评教王")
    window_width = 350
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)
    id_label = tk.Label(root, text="学号 (ID):")
    id_label.pack(pady=(15, 0))
    id_entry = tk.Entry(root, width=30)
    id_entry.pack(pady=5)
    password_label = tk.Label(root, text="东北大学一网通办密码 (Password):")
    password_label.pack()
    password_entry = tk.Entry(root, width=30, show="*")
    password_entry.pack(pady=5)
    start_button = tk.Button(root, text="开始评教", command=start_evaluation, bg="#4CAF50", fg="white",
                             font=('Arial', 10, 'bold'))
    start_button.pack(pady=15)
    root.mainloop()

if __name__ == "__main__":
    create_gui()