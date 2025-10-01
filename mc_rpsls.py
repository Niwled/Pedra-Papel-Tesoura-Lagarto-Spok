import tkinter as tk
import random as rd
import json
import os

class JogoPPTLS:
    def __init__(self):
        self.root= tk.Tk()
        self.root.title('Pedra Papel Tesoura Lagarto Spock')
        self.root.geometry("450x450")
        self.root.resizable(False, False)
        self.root.configure(bg='gray33')
        self.pontuacao_jogador = 0
        self.pontuacao_computador = 0
        self.jogadas = {
            1: '✊ Pedra',
            2: '✋ Papel',
            3: '✌️ Tesoura',
            4: '🦎 Lagarto',
            5: '🖖 Spock',}
        self.historico= []
        self.nome_arquivo = "historico_jogadas.json"
        self.carregar_historico()
        self.interface()

    def interface(self):
        titulo = tk.Label(self.root, text= 'Pedra Papel Tesoura Lagarto Spock', fg= 'orange', bg= 'gray33', font=('Arial', 17, 'bold'))
        titulo.pack(pady=20)
        self.placar = tk.Label(self.root, text= f'Jogador: {self.pontuacao_jogador} | Computador: {self.pontuacao_computador}',
                           fg= 'orange', bg= 'gray33', font=('Arial', 12, 'bold'))
        self.placar.pack()
        jogada1 =tk.Button(self.root, text= '✊ Pedra', width= 7, height= 2, command= lambda: self.jogar(1))
        jogada1.pack(pady=12)
        jogada2 =tk.Button(self.root, text= '✋ Papel', width= 7, height= 2, command= lambda: self.jogar(2))
        jogada2.pack(pady=12)
        jogada3 =tk.Button(self.root, text= '✌️ Tesoura', width= 7, height= 2, command= lambda: self.jogar(3))
        jogada3.pack(pady=12)
        jogada4 =tk.Button(self.root, text= '🦎 Lagarto', width= 7, height= 2, command= lambda: self.jogar(4))
        jogada4.pack(pady=12)
        jogada5 =tk.Button(self.root, text= '🖖 Spock', width= 7, height= 2, command= lambda: self.jogar(5))
        jogada5.pack(pady=12)

    def verificar_vencedor(self, jogador, computador):
        if jogador == computador:
            return 'Empate'
        
        vitorias = {
            1:[3, 4],
            2:[1, 5],
            3:[2, 4],
            4:[2, 5],
            5:[1, 3]
        }

        if computador in vitorias[jogador]:
            return "Você venceu!"
        else:
            return "Você perdeu!"
        
    def carregar_historico(self):
        if os.path.exists(self.nome_arquivo):
            with open(self.nome_arquivo, "r") as arquivo:
                self.historico = json.load(arquivo)
            print(f"Histórico carregado: {len(self.historico)} jogadas")
        else:
            self.historico = []
            print("Nenhum histórico encontrado, começando novo")

    def salvar_historico(self):
        with open(self.nome_arquivo, 'w') as arquivo:
            json.dump(self.historico, arquivo)

    def analisar_frequencias(self):
        contador = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for jogada in self.historico:
            escolha_jogador = jogada["jogador"]
            contador[escolha_jogador] += 1

        jogada_mais_usada = max(contador, key= contador.get)

        return contador, jogada_mais_usada
    
    def analisar_sequencias(self):
        if len(self.historico) < 3:
            return None
        
        padroes = {}


        for i in range (len(self.historico) - 2):

            jogada1 = self.historico[i]["jogador"]
            jogada2 = self.historico[i +1]["jogador"]
            proxima = self.historico[i +2]["jogador"]

            sequencia = f"{jogada1}-{jogada2}"


            if sequencia not in padroes:
                padroes[sequencia] = []
            padroes[sequencia].append(proxima)
        
        return padroes

    def iniciar(self):
        self.root.mainloop()

    def jogar(self, escolha_jogador):
        print(f"Botão{escolha_jogador} foi clicado!")
        print(f"Você escolheu: {self.jogadas[escolha_jogador]}")

        escolha_computador = self.cerrebro()
        print(f"Computador escolheu: {self.jogadas[escolha_computador]}")

        resultado = self.verificar_vencedor(escolha_jogador, escolha_computador)
        if resultado == 'Você perdeu!':
            self.pontuacao_computador +=1
        elif resultado == 'Você venceu!':
            self.pontuacao_jogador +=1
        elif resultado == 'Empate':
            self.pontuacao_jogador +=0

        self.placar.config(text = f'Jogador: {self.pontuacao_jogador} | Computador: {self.pontuacao_computador}')

        jogada_atual = {
            "jogador": escolha_jogador,
            "computador": escolha_computador,
            "resultado": resultado,
            "rodada": len(self.historico) +1
            }
        
        self.historico.append(jogada_atual)
        self.salvar_historico()

        if len(self.historico) > 3:
            contador, mais_usada = self.analisar_frequencias()
            print(f"Teste - Contador: {contador}")
            print(f"Teste - Jogada mais usada: {mais_usada} ({self.jogadas[mais_usada]})")

            padroes = self.analisar_sequencias()
            if padroes:
                print(f"Teste - Padrões detectados: {padroes}")
    
    def cerrebro(self):

        if len(self.historico) < 3:
            return rd.randint(1, 5)
        
        previsao = None

        padroes = self.analisar_sequencias()
        if padroes:

            ultima = self.historico[-1]["jogador"]
            penultima = self.historico[-2]["jogador"]
            sequencia_atual = f"{penultima}-{ultima}"

            if sequencia_atual in padroes:
                jogadas_possiveis = padroes[sequencia_atual]
                previsao = max(set(jogadas_possiveis), key= jogadas_possiveis.count)

            if previsao is None:
                contador, mais_usada = self.analisar_frequencias()
                previsao = mais_usada

            if previsao is None:
                return rd.radind(1, 5)
            
            respostas = {
                1: [2, 5],
                2: [3, 4],
                3: [1, 5],
                4: [1, 3],
                5: [2, 4]
                }
            
            jogadas_vencedoras= respostas[previsao]
            escolha_ia= rd.choice(jogadas_vencedoras)

            return escolha_ia


if __name__ == '__main__':
    jogo = JogoPPTLS()
    jogo.iniciar()
