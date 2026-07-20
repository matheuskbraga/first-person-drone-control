

# First-Person Drone Control

Controle um drone Tello ou Tello EDU em primeira pessoa (FPV) usando seu computador. Este projeto fornece uma interface gráfica que exibe o feed de vídeo ao vivo do drone e permite o controle total dos movimentos através do teclado.

---

## 🚧 Status: Em Desenvolvimento

Este projeto está em desenvolvimento ativo. Use com cautela e esteja ciente de que bugs ou comportamentos inesperados podem ocorrer.

## ✨ Funcionalidades

- **Visualização em Primeira Pessoa (FPV):** Veja o feed de vídeo da câmera do drone em tempo real na tela do seu computador.
- **Controle por Teclado:** Pilote o drone usando teclas familiares (WASD + Setas).
- **Comandos Rápidos:** Decole e pouse com o pressionar de uma única tecla.
- **Interface Moderna:** Interface gráfica construída com CustomTkinter para uma aparência limpa e moderna.
- **Controle Suave:** O movimento é contínuo enquanto as teclas são pressionadas, permitindo manobras precisas.

## 🔧 Pré-requisitos

Antes de começar, garanta que você tenha os seguintes itens:

- **Python 3.8+**
- Um drone **Ryze Tello** ou **Tello EDU**.
- Um computador com capacidade de conexão Wi-Fi.

## 🚀 Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências do projeto.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/first-person-drone-control.git
    cd first-person-drone-control
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas Python necessárias.
    ```bash
    pip install -r requirements.txt
    ```

## 🚁 Como Usar

1.  **Ligue seu drone Tello.**
2.  **Conecte seu computador à rede Wi-Fi do Tello.** A rede geralmente aparece como `TELLO-XXXXXX`.
3.  **Execute a aplicação:**
    Rode o script `main.py` a partir do seu terminal.
    ```bash
    python main.py
    ```
4.  Aguarde a interface gráfica aparecer. A mensagem "Aguardando vídeo..." será substituída pelo feed da câmera do drone assim que a conexão for estabelecida. O nível da bateria será impresso no terminal.
5.  Use as teclas abaixo para controlar o drone.

## ⌨️ Controles do Teclado

| Tecla         | Ação                     |
|---------------|--------------------------|
| **T**         | Decolar (Takeoff)        |
| **L**         | Pousar (Land)            |
| **W**         | Subir                    |
| **S**         | Descer                   |
| **A**         | Mover para a esquerda    |
| **D**         | Mover para a direita     |
| **Seta Cima** | Mover para frente        |
| **Seta Baixo**| Mover para trás          |
| **Q**         | Girar (sentido anti-horário) |
| **E**         | Girar (sentido horário)  |

> **Nota:** Soltar uma tecla de movimento irá parar imediatamente a ação correspondente.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* para relatar bugs ou sugerir novas funcionalidades. Se desejar contribuir com código, por favor, abra um *pull request*.
