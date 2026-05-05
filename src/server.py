import cv2
import os
import socket
import time

host = '10.10.1.212'
port = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

print(f"Servidor aguardando conexão em {host}:{port}")

conn, addr = s.accept()
print(f"Conectado por {addr}")

while True:

    def focus(img):

        if img is None:
            print(f"Nao foi possivel carregar a imagem em '{img}'.")
            return False

        filtro_img = cv2.medianBlur(img,3)
        lapl_img = cv2.Laplacian(filtro_img, cv2.CV_64F).var()
        print(f'\n{lapl_img}')

        return lapl_img
    
    def capturar_foto(cam):
        valid, frame = cam.read()
        if valid:
            focused = focus(frame)
            # cv2.imshow(f'Foto (foco: {focused})', frame)
            cv2.waitKey(1000)
            return focused, frame
        else:
            print("Erro ao capturar a foto.")
            return None, None

    threshold = 62
    best_focus = 0
    valores = []
    pos = []
    p = 0

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Erro ao abrir a câmera.")
        exit()

    for f in range(5):
        p += 50 # mudar de acordo com a especificacao dos passos
        
        is_focused, f = capturar_foto(cam)

        if f is not None:
            print("Foto recebida")
            valores.append(is_focused)
            pos.append(p)
                    
            # Verifica foco
            if is_focused > threshold:
                print(f"A imagem {f} esta focada.")

            else:
                print(f"A imagem {f} esta desfocada.")
                # realizar um segundo teste de foco

            conn.send(str(p).encode())
            while True:
                resposta = conn.recv(1024).decode('utf-8')
                if resposta == "ok":
                    print("Posicao ok.")
                    break

    print("\nVerredura feita.\n")
    for i in range(len(valores)):
        if valores[i] > best_focus:
            best_focus = valores[i]
            p = i

    posicao = pos[p]
    conn.send(str(posicao).encode())
    while True:
        resposta = conn.recv(1024).decode('utf-8')
        if resposta == "ok":
            print("Posicao ajustada no melhor foco\n")
            break

    print(valores)
    print(pos)
    
    while best_focus >= threshold:
        print(f"O melhor foco {best_focus: .2f} esta na posicao {posicao: }_<")
        time.sleep(5)

        is_focused, f = capturar_foto(cam)
        
        if (is_focused >= best_focus or is_focused >= threshold):
            best_focus = is_focused
            print("Focado!\n")
            time.sleep(10)
    
        else:
            print("Ajustando lente novamente...\n")
            break
                    
    cam.release()
    cv2.destroyAllWindows()

    print("\nPrograma finalizado.")
