import sys
import time


def main():
    print("程式B啟動，等待來自程式A的訊息...")
    sys.stdout.flush()

    message_count = 0

    try:
        while True:
            # 從STDIN讀取訊息
            line = sys.stdin.readline()
            if not line:  # EOF
                break

            message = line.strip()
            print(f"程式B收到訊息: {message}")
            sys.stdout.flush()

            # 檢查結束訊號
            if message.lower() == "quit":
                print("程式B收到結束訊號，準備關閉...")
                sys.stdout.flush()
                break

            message_count += 1

            # 回應程式A
            response = f"程式B回應第{message_count}次: 已收到 '{message}'"
            print(response)
            sys.stdout.flush()

            time.sleep(1)  # 模擬處理時間

    except KeyboardInterrupt:
        print("程式B被中斷...")
    except Exception as e:
        print(f"程式B發生錯誤: {e}")
    finally:
        print("程式B結束")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
