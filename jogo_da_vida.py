# ---------------- IMPORTAÇÕES ----------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------------- CONFIGURAÇÕES ----------------
TAMANHO_GRADE = 100
INTERVALO_MS = 50
TOTAL_GERACOES = 800
SEMENTE = 16

# ---------------- PADRÕES INICIAIS ----------------
def carregar_padrao(nome_padrao):
    nome = nome_padrao.lower()

    if nome == "lwss":
        return np.array([
            [0, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0]
        ], dtype=int)

    else:
        return np.random.choice([0, 1], size=(TAMANHO_GRADE, TAMANHO_GRADE), p=[0.8, 0.2])


def inserir_padrao(grade, nome_padrao, posicao=(10, 10)):
    padrao = carregar_padrao(nome_padrao)

    altura, largura = padrao.shape
    px, py = posicao

    if px + altura < TAMANHO_GRADE and py + largura < TAMANHO_GRADE:
        grade[px:px+altura, py:py+largura] = padrao

    return grade


# ---------------- LÓGICA DO JOGO ----------------
def calcular_vizinhos(grade):
    return (
        np.roll(np.roll(grade, 1, 1), 1, 0) +
        np.roll(grade, 1, 0) +
        np.roll(np.roll(grade, -1, 1), 1, 0) +
        np.roll(grade, 1, 1) +
        np.roll(grade, -1, 1) +
        np.roll(np.roll(grade, 1, 1), -1, 0) +
        np.roll(grade, -1, 0) +
        np.roll(np.roll(grade, -1, 1), -1, 0)
    )


def atualizar_frame(frame, grade, imagem, eixo, dados_mudancas):
    nova_grade = grade.copy()
    vizinhos = calcular_vizinhos(grade)

    nascimento = (vizinhos == 3) & (grade == 0)
    sobrevivencia = ((vizinhos == 2) | (vizinhos == 3)) & (grade == 1)

    nova_grade[:] = 0
    nova_grade[nascimento | sobrevivencia] = 1

    celulas_que_mudaram = np.sum(grade != nova_grade) 
    
    dados_mudancas.append(celulas_que_mudaram)

    grade[:] = nova_grade
    imagem.set_array(grade)

    eixo.set_title(f"Geração {frame+1} | Transições Celulares: {celulas_que_mudaram}")
    return [imagem]


# ---------------- ANÁLISE FINAL ----------------
def gerar_grafico_atividade(dados):
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(dados)), dados, color='purple')
    plt.title("Atividade de Transição Celular ao Longo do Tempo")
    plt.xlabel("Geração")
    plt.ylabel("Número de Transições de Estado por Geração")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("atividade_transicao_celular.png")
    print("Arquivo atividade_transicao_celular.png salvo.")
    plt.show()


# ---------------- EXECUÇÃO PRINCIPAL ----------------
if __name__ == "__main__":
    np.random.seed(SEMENTE)
    grade = np.zeros((TAMANHO_GRADE, TAMANHO_GRADE), dtype=int)

    # Escolha inicial
    # grade = inserir_padrao(grade, "lwss", (50, 10))
    grade = carregar_padrao("random")

    historico_mudancas = []

    fig, ax = plt.subplots(figsize=(10, 10))
    imagem = ax.imshow(grade, cmap="binary")
    ax.set_xticks([])
    ax.set_yticks([])

    animacao = FuncAnimation(
        fig,
        atualizar_frame,
        fargs=(grade, imagem, ax, historico_mudancas),
        frames=TOTAL_GERACOES,
        interval=INTERVALO_MS,
        blit=True,
        repeat=False
    )

    print("Rodando simulação e salvando GIF...")
    animacao.save("simulacao_do_jogo_da_vida.gif", writer="pillow", fps=20)
    print("Arquivo simulacao_do_jogo_da_vida.gif salvo.")

    gerar_grafico_atividade(historico_mudancas)