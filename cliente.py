import requests

URL = "http://localhost:5000"

def pedir_datos():
    return {"usuario": input("Usuario: "), "contraseña": input("Contraseña: ")}

def enviar(ruta, datos):
    """Envía el POST y maneja los errores de conexión."""
    try:
        return requests.post(f"{URL}{ruta}", json=datos, timeout=5)
    except requests.exceptions.RequestException:
        print("No se pudo conectar con el servidor")
        return None
    
while True:
    print("\n1- Registrarse\n2- Inicio de sesión\n3- Salir")
    option = input("Opción: ")
    if option == "1":
        r = enviar("/registro", pedir_datos())
    elif option == "2":
        r = enviar("/login", pedir_datos())
    elif option == "3":
        break
    else:
        print("Opción inválida")
        continue

    if r is not None:
        print(r.status_code, r.json())