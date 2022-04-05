# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import re
import subprocess

hostName = "0.0.0.0"
serverPort = 8080

# Data e hora do sistema;
# ● Uptime (tempo de funcionamento sem reinicialização do sistema) em segundos;
# ● Modelo do processador e velocidade;
# ● Capacidade ocupada do processador (%);
# ● Quantidade de memória RAM total e usada (MB);
# ● Versão do sistema;
# ● Lista de processos em execução (pid e nome)
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        def get_pretty_value(value_name: str, value: str) -> bytes:
            return bytes(str(f"{value_name}: {value}<br>"), "utf-8")

        def run_shell_command(command: str) -> str:
            return subprocess.run(
                command, stdout=subprocess.PIPE, shell=True
            ).stdout.decode("utf-8")

        date = run_shell_command("date")
        pretty_date = get_pretty_value("Date", date)

        system_uptime = run_shell_command("uptime")
        pretty_sys_uptime = get_pretty_value("System uptime", system_uptime)

        processor_name_and_speed = run_shell_command(
            'head /proc/cpuinfo | grep "model name\|cpu MHz"'
        )
        pretty_processor_name_and_speed = get_pretty_value(
            "Processor info", processor_name_and_speed
        )

        # Processor usage formatting from https://stackoverflow.com/a/9229580
        processor_usage = run_shell_command(
            "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage \"%\"}'"
        )
        pretty_processor_usage_bytes = get_pretty_value(
            "Processor usage", processor_usage
        )

        memory_total = run_shell_command("cat /proc/meminfo | grep 'MemTotal'")
        memory_total_kb = re.sub("[^\d]", "", memory_total)
        memory_total_mb = str(int(memory_total_kb) // 1024)
        pretty_memory_total = get_pretty_value(
            "Memory total", str(memory_total_mb) + " MB"
        )

        memory_free = run_shell_command("cat /proc/meminfo | grep 'MemFree'")
        memory_free_kb = re.sub("[^\d]", "", memory_free)
        memory_free_mb = str(int(memory_free_kb) // 1024)
        memory_in_use_mb = int(memory_total_mb) - int(memory_free_mb)
        pretty_memory_in_use = get_pretty_value(
            "Memory in use", str(memory_in_use_mb) + " MB"
        )

        system_version = run_shell_command("cat /proc/version")
        pretty_system_version = get_pretty_value("System version", system_version)

        process_list = run_shell_command("ps -o pid -o comm")
        pretty_process_list = get_pretty_value(
            "Process list", process_list.replace("\n", "<br>")
        )

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>System Information</title></head>", "utf-8")
        )
        self.wfile.write(pretty_date)
        self.wfile.write(pretty_sys_uptime)
        self.wfile.write(pretty_processor_name_and_speed)
        self.wfile.write(pretty_processor_usage_bytes)
        self.wfile.write(pretty_memory_total)
        self.wfile.write(pretty_memory_in_use)
        self.wfile.write(pretty_system_version)
        self.wfile.write(pretty_process_list)

        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
