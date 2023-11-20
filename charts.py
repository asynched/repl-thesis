import matplotlib.pyplot as plt
import numpy as np

clients = [50, 100, 500, 1000, 2000]


class LoadTest:
    def rps(self):
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

    def latency(self):
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

    def rate(self):
        node_rate = [890, 720, 160, 77, 38]
        python_rate = [550, 400, 113, 52, 24]
        repl_rate = [10_000, 10_000, 6_666, 3_333, 1_666]

        plt.plot(clients, node_rate, label="NodeJS")
        plt.plot(clients, python_rate, label="Python")
        plt.plot(clients, repl_rate, label="REPL")

        plt.xlabel("Clientes conectados")
        plt.ylabel("Mensagens por segundo (maior é melhor)")

        plt.title("Comparação de performance em mensagens por segundo")
        plt.legend()

        plt.subplots_adjust(left=0.15, right=0.95, top=0.95)

        plt.savefig("charts/rate.png", dpi=300)

    def save_plots(self):
        self.rps()
        plt.cla()
        self.latency()
        plt.cla()
        self.rate()
        plt.cla()


class IntegrationTest:
    def rps(self):
        clients = [50, 100, 500, 1000]
        standalone = [984, 557, 136, 67]
        redis = [3719, 2382, 646, 279]
        repl = [2379, 2569, 2471, 2143]

        plt.plot(clients, standalone, label="Node")
        plt.plot(clients, redis, label="Node + Redis")
        plt.plot(clients, repl, label="Node + REPL")

        plt.xlabel("Clientes conectados")
        plt.ylabel("Requisições por segundo (maior é melhor)")

        plt.title("Comparação de performance em requisições por segundo")
        plt.legend()

        plt.subplots_adjust(left=0.15, right=0.95, top=0.95)

        plt.savefig("charts/integration_rps.png", dpi=300)

    def latency(self):
        clients = [50, 100, 500, 1000]
        standalone = [1, 1.4, 8.2, 17]
        redis = [0.25, 0.4, 1.5, 3.8]
        repl = [0.4, 0.4, 0.4, 0.4]

        plt.plot(clients, standalone, label="Node")
        plt.plot(clients, redis, label="Node + Redis")
        plt.plot(clients, repl, label="Node + REPL")

        plt.xlabel("Clientes conectados")
        plt.ylabel("Latência (menor é melhor)")

        plt.title("Comparação de performance em latência")
        plt.legend()

        plt.subplots_adjust(left=0.15, right=0.95, top=0.95)

        plt.savefig("charts/integration_latency.png", dpi=300)

    def rate(self):
        clients = [50, 100, 500, 1000]
        standalone = [990, 714, 120, 60]
        redis = [3900, 2500, 664, 263]
        repl = [2500, 2500, 2500, 2500]

        plt.plot(clients, standalone, label="Node")
        plt.plot(clients, redis, label="Node + Redis")
        plt.plot(clients, repl, label="Node + REPL")

        plt.xlabel("Clientes conectados")
        plt.ylabel("Mensagens por segundo (maior é melhor)")

        plt.title("Comparação de performance em mensagens por segundo")
        plt.legend()

        plt.subplots_adjust(left=0.15, right=0.95, top=0.95)

        plt.savefig("charts/integration_rate.png", dpi=300)

    def save_plots(self):
        self.rps()
        plt.cla()
        self.latency()
        plt.cla()
        self.rate()


if __name__ == "__main__":
    load_test = LoadTest()
    load_test.save_plots()

    integration_test = IntegrationTest()
    integration_test.save_plots()
