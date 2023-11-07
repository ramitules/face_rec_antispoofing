# Reconocimiento facial Antispoofing
- Proyecto de reconocimiento facial basado en Python
- Proporciona registro e ingreso tanto con reconocimiento facial como con credenciales convencionales (usuario y contraseña).
- Reconocimiento facial creado con filtro antispoofing, lo cual obliga al usuario mirar frente a la camara y pestañear tres veces.
- Se utiliza SQLite como motor de base de datos - Tkinter como GUI
![demo](https://github.com/ramitules/face_rec_antispoofing/assets/111546397/2dff9eaf-2b38-4c5a-88ba-470ea0e54924)

## Requisitos
- Windows (testeado en Windows 10) / Linux (testeado en Linux Mint 21.2)
- Python 3.8 o superior
## Uso
Antes de comenzar, se recomienda instalar todas las dependencias con `pip install -r requirements.txt`
### Registro
1. Proporcionar nombre, usuario, contraseña e informacion biometrica (opcional)
2. Presionar SEND
### Ingreso
1. En caso de elegir ingresar por reconocimiento facial, presionar boton FACE RECOGNITION.
2. En caso de elegir ingresar por credenciales, ingresar usuario y contraseña.
3. Presionar SEND
### Videocaptura biometrica
- Las capturas se realizan con un mallado de la cara a reconocer, teniendo en cuenta puntos claves para posterior identificacion.
- Se debe mirar de frente a la camara, a una distancia predeterminada hasta que un recuadro aparezca en el borde izquierdo de la pantalla.
- Pestañear tres veces.
- Cierre automatico de ventana
## Contacto
- Podes encontrarme en [LinkedIn](https://www.linkedin.com/in/ramitules/) 😉
