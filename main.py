from drone_controller import TelloController
from ui import DroneInterface

def main():
    print("Iniciando o sistema do Drone...")
    
    # 1. Instancia o controlador
    drone = TelloController()
    
    # 2. Conecta à rede WiFi do Tello
    try:
        drone.connect()
    except Exception as e:
        print(f"Erro ao conectar com o Tello: {e}")
        print("Certifique-se de que o computador está conectado no WiFi do drone.")
        return

    # 3. Inicializa a Interface Gráfica injetando o controle do drone nela
    app = DroneInterface(drone)
    
    # 4. Inicia o loop principal da janela do sistema
    print("Interface carregada. Comandos básicos:")
    print("- Pressione 'T' para decolar.")
    print("- Pressione 'L' para pousar.")
    app.mainloop()

if __name__ == "__main__":
    main()