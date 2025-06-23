# client_inspector.py (最終修正版)
import asyncio
from fastmcp import Client
from fastmcp.client.transports import SSETransport
from rich.console import Console
from rich.panel import Panel

# 伺服器的 URL
SERVER_URL = "http://localhost:8001/sse"

# 初始化 rich Console
console = Console()


async def main():
    """
    連接到 MCP 伺服器並列出所有可用的資源。
    """
    console.print(
        f"[bold cyan]正在嘗試連接到 MCP 伺服器:[/bold cyan] [yellow]{SERVER_URL}[/yellow]"
    )

    try:
        transport = SSETransport(SERVER_URL)

        async with Client(transport) as client:
            console.print("[bold green]✅ 連線成功！正在獲取資源資訊...[/bold green]\n")

            # --- 1. 獲取並打印 Tools ---
            list_tools_result = await client.list_tools()
            # console.print(list_tools_result)

            tool_content = ""
            if list_tools_result:
                # 修正處：從結果物件的 .tools 屬性進行迭代
                for tool in list_tools_result:
                    tool_content += f"[bold]名稱:[/] [cyan]{tool.name}[/]\n"
                    tool_content += f"[bold]描述:[/] {tool.description}\n"

            # if tool.inputSchema and tool.inputSchema.get("properties"):
            #     tool_content += "[bold]參數:[/]\n"
            #     for param_name, param_details in tool.inputSchema[
            #         "properties"
            #     ].items():
            #         param_type = param_details.get("type", "any")
            # param_desc = param_details.get("description", "無描述")
            #                 tool_content += f"  - [yellow]{param_name}[/] ([italic]{param_type}[/italic]): {param_desc}\n"
            #         else:
            #             tool_content += "[bold]參數:[/] 無\n"
            #         tool_content += "---\n"
            else:
                tool_content = "未找到任何工具 (Tools)。"
            console.print(
                Panel(
                    tool_content.strip(),
                    title="[bold magenta]🛠️ 工具 (Tools)[/bold magenta]",
                    expand=False,
                )
            )

            # --- 2. 獲取並打印 Resources ---
            list_resources_result = await client.list_resources()
            # console.print(list_resources_result)

            resource_content = ""
            if list_resources_result:
                for res in list_resources_result:
                    resource_content += f"[bold]URI:[/] [cyan]{res.uri}[/]\n"
                    resource_content += f"[bold]名稱:[/] {res.name}\n"
                    resource_content += f"[bold]描述:[/] {res.description}\n"
                    resource_content += f"[bold]MIME 類型:[/] {res.mimeType=}\n"
                    resource_content += "---\n"
            else:
                resource_content = "未找到任何靜態資源 (Resources)。"
            console.print(
                Panel(
                    resource_content.strip(),
                    title="[bold blue]📚 靜態資源 (Resources)[/bold blue]",
                    expand=False,
                )
            )

            # # --- 3. 獲取並打印 Resource Templates ---
            # list_templates_result = await client.list_resource_templates()
            # console.print(list_templates_result)
            # template_content = ""
            # if list_templates_result:
            #     for template in list_templates_result:
            #         template_content += f"[bold]URI 模板:[/] [cyan]{template.uri}[/]\n"
            #         template_content += f"[bold]名稱:[/] {template.name}\n"
            #         template_content += f"[bold]描述:[/] {template.description}\n"
            #         template_content += "---\n"
            # else:
            #     template_content = "未找到任何資源模板 (Resource Templates)。"
            # console.print(
            #     Panel(
            #         template_content.strip(),
            #         title="[bold green]📄 資源模板 (Resource Templates)[/bold green]",
            #         expand=False,
            #     )
            # )

            # --- 4. 獲取並打印 Prompts ---
            list_prompts_result = await client.list_prompts()
            # console.print(list_prompts_result)

            prompt_content = ""
            if list_prompts_result:
                for prompt in list_prompts_result:
                    prompt_content += f"[bold]名稱:[/] [cyan]{prompt.name}[/]\n"
                    prompt_content += f"[bold]描述:[/] {prompt.description}\n"

                    if prompt.arguments and prompt.arguments.get("properties"):
                        prompt_content += "[bold]參數:[/]\n"
                        for param_name in prompt.arguments["properties"]:
                            prompt_content += f"  - [yellow]{param_name}[/]\n"
                    else:
                        prompt_content += "[bold]參數:[/] 無\n"
                    prompt_content += "---\n"
            else:
                prompt_content = "未找到任何提示 (Prompts)。"
            console.print(
                Panel(
                    prompt_content.strip(),
                    title="[bold yellow]💡 提示 (Prompts)[/bold yellow]",
                    expand=False,
                )
            )

    except Exception as e:
        console.print(f"[bold red]❌ 發生錯誤:[/bold red] {e}")


if __name__ == "__main__":
    # 請確保您的 weather_server.py 正在運行
    asyncio.run(main())
