# main.py
from drone_controller import TelloController
from ui import DroneInterface

def main():
    """
    Ponto de entrada principal da aplicação.
    Inicializa o controlador do drone e a interface do usuário.
    """
    try:
        controller = TelloController()
        controller.connect()
        app = DroneInterface(drone_controller=controller)
        app.mainloop()
    except Exception as e:
        print(f"Ocorreu um erro ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    main()