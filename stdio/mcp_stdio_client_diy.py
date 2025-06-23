import subprocess
import threading
import time
import json
import queue
import os


class MCPClient:
    def __init__(self, command, env_vars=None):
        self.command = command
        self.process = None
        self.read_thread = None
        self.response_queue = queue.Queue()
        self.env_vars = env_vars or {}

    def _read_output(self):
        """讀取子程式的輸出"""
        while True:
            try:
                if self.process.poll() is not None:
                    break

                output = self.process.stdout.readline()
                if output:
                    output = output.strip()
                    print(f"[收到]: {output}")

                    # 嘗試解析 JSON 回應
                    try:
                        json_response = json.loads(output)
                        self.response_queue.put(json_response)
                    except json.JSONDecodeError:
                        pass  # 忽略非 JSON 輸出

            except Exception as e:
                print(f"讀取錯誤: {e}")
                break

    def start(self):
        """啟動子程式"""
        # 準備環境變數
        env = os.environ.copy()
        env.update(self.env_vars)

        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )

        # 啟動讀取執行緒
        self.read_thread = threading.Thread(target=self._read_output, daemon=True)
        self.read_thread.start()

        time.sleep(2)  # 等待程式啟動

    def send_message(self, message):
        """發送訊息"""
        try:
            json_str = json.dumps(message) + "\n"
            self.process.stdin.write(json_str)
            self.process.stdin.flush()
            print(f"[發送]: {json.dumps(message)}")
        except Exception as e:
            print(f"發送錯誤: {e}")

    def wait_for_response(self, request_id, timeout=10):
        """等待特定 ID 的回應"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = self.response_queue.get(timeout=1)
                if response.get("id") == request_id:
                    return response
                # 不是目標回應，放回佇列
                self.response_queue.put(response)
            except queue.Empty:
                continue
        raise TimeoutError(f"等待回應超時 (ID: {request_id})")

    def initialize_mcp(self):
        """執行 MCP 初始化序列"""
        # 1. 發送 initialize 並等待回應
        init_msg = {
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-03",
                "capabilities": {},
                "clientInfo": {"name": "mcp", "version": "0.1.0"},
            },
            "jsonrpc": "2.0",
            "id": 0,
        }

        self.send_message(init_msg)
        init_response = self.wait_for_response(0)
        print(f"[初始化完成]: {json.dumps(init_response, ensure_ascii=False)}")

        # 2. 發送 notifications/initialized
        self.send_message({"method": "notifications/initialized", "jsonrpc": "2.0"})
        time.sleep(0.5)  # 給伺服器處理時間

        # 3. 發送 tools/list 並等待回應
        tools_msg = {"method": "tools/list", "jsonrpc": "2.0", "id": 1}
        self.send_message(tools_msg)
        tools_response = self.wait_for_response(1)
        print(f"[工具清單]: {json.dumps(tools_response, ensure_ascii=False, indent=2)}")

        return True

    def close(self):
        """關閉程式"""
        if self.process:
            self.process.terminate()


def main():
    # 設定命令和環境變數
    command = ["cmd", "/c", "npx", "server-perplexity-ask"]
    env_vars = {"PERPLEXITY_API_KEY": "YOUR_API_KEY_HERE"}

    # 創建客戶端
    client = MCPClient(command, env_vars)

    try:
        print("啟動 MCP 伺服器...")
        client.start()

        print("執行初始化階段...")
        client.initialize_mcp()

        print("\n=== MCP 初始化完成 ===")
        input("按 Enter 鍵結束...")

    except KeyboardInterrupt:
        print("城市被中斷")
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    print(f"目前應用程式 PID: {os.getpid()}")
    input("按 Enter 鍵開始 MCP 客戶端...")
    main()
