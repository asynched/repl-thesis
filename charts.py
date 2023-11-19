import matplotlib.pyplot as plt
import numpy as np

clients = [50, 100, 500, 1000, 2000]


def plot_request_per_second():
    node_rps = [9601, 6818, 1475, 765, 386]
    python_rps = [2044, 1618, 700, 383, 192]
    repl_rps = [106598, 56927, 9534, 4666, 2514]

    plt.plot(clients, node_rps, label="NodeJS")
    plt.plot(clients, python_rps, label="Python")
    plt.plot(clients, repl_rps, label="REPL")

    plt.xlabel("Clientes conectados")
    plt.ylabel("Requisições por segundo (maior é melhor)")

    plt.title("Comparação de performance em requisições por segundo")
    plt.legend()

    plt.subplots_adjust(left=0.15, right=0.95, top=0.95)

    plt.savefig("charts/rps.png", dpi=300)


def plot_latency():
    node_latency = [1.1, 1.4, 6.2, 12.9, 25]
    python_latency = [1.8, 2.5, 8.7, 19.3, 31]
    repl_latency = [0.1, 0.1, 0.15, 0.3, 0.6]

    plt.plot(clients, node_latency, label="NodeJS")
    plt.plot(clients, python_latency, label="Python")
    plt.plot(clients, repl_latency, label="REPL")

    plt.xlabel("Clientes conectados")
    plt.ylabel("Latência (menor é melhor)")

    plt.title("Comparação de performance em latência")
    plt.legend()

    plt.subplots_adjust(left=0.15, right=0.95, top=0.95)

    plt.savefig("charts/latency.png", dpi=300)


def plot_rate():
    node_rate = [890, 720, 160, 77, 38]
    python_rate = [550, 400, 113, 52, 24]
    repl_rate = [10_000, 10_000, 6_666, 3_333, 1_666]

    plt.plot(clients, node_rate, label="NodeJS")
    plt.plot(clients, python_rate, label="Python")
    plt.plot(clients, repl_rate, label="REPL")

    plt.xlabel("Clientes conectados")
    plt.ylabel("Mensagens por milissegundo (maior é melhor)")

    plt.title("Comparação de performance em mensagens por milissegundo")
    plt.legend()

    plt.subplots_adjust(left=0.15, right=0.95, top=0.95)

    plt.savefig("charts/rate.png", dpi=300)


if __name__ == "__main__":
    print("[INFO] Gerando gráfico de requisições por segundo.")
    plot_request_per_second()

    plt.cla()

    print("[INFO] Gerando gráfico de latência.")
    plot_latency()

    plt.cla()

    print("[INFO] Gerando gráfico de mensagens por milissegundo.")
    plot_rate()
