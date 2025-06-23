import subprocess
import time
import threading


def read_output(process):
    """讀取子程序的輸出"""
    while True:
        try:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(f"[程式A收到]: {output.strip()}")
        except Exception as e:
            print(f"讀取錯誤: {e}")
            break


def main():
    print("程式A啟動，準備啟動程式B...")

    input("按 Enter 鍵以啟動程式B...")

    # 啟動程式B，設定STDIO管道
    process = subprocess.Popen(
        ["python", "D:\\#OpenSourceContribute\\net_course_mcp_demo\\child_app.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,  # 行緩衝
    )

    print(f"程式B已啟動，PID: {process.pid}")

    # 啟動讀取執行緒
    read_thread = threading.Thread(target=read_output, args=(process,))
    read_thread.daemon = True
    read_thread.start()

    # 發送訊息給程式B
    messages = [
        "Hello from Process A",
        "How are you doing?",
        "This is message 3",
        "Final message",
        "quit",  # 結束訊號
    ]

    for i, msg in enumerate(messages):
        time.sleep(2)  # 間隔2秒
        # if i == len(messages) - 1:
        #     time.sleep(300)
        print(f"[程式A發送]: {msg}")
        try:
            process.stdin.write(msg + "\n")
            process.stdin.flush()
        except Exception as e:
            print(f"發送錯誤: {e}")
            break

    # 等待程式B結束
    process.wait()
    print(f"程式B已結束，返回碼: {process.returncode}")

    # === 新增這一段，防止主視窗自動關閉 ===
    print("\n監控會話已結束。按 Enter 鍵退出程式A。")
    input()  # 等待使用者輸入，這樣視窗就不會馬上關閉


if __name__ == "__main__":
    main()
