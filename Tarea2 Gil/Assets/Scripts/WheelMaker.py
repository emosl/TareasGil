#Emilia Salazar Leipen A01781931
import math

def calculate_normals(v1, v2, v3):
    # Primero tomamos como parámetros los tres vectores de los cuales vamos a crear la normal. Sabemos que la fórmula para calcular el producto cruz es multiplicar los vectores u X v, así que los obtenemos:
    # u = la resta de las coordenadas del vector dos con el vector 1
    # v = la resta de las coordenadas del vector 3 con el vector 1
    ux = v2[0] - v1[0]
    uy = v2[1] - v1[1]
    uz = v2[2] - v1[2]

    vx = v3[0] - v1[0]
    vy = v3[1] - v1[1]
    vz = v3[2] - v1[2]

    # obtenemos las coordenadas del vector normal calculando el producto punto de u X V
    normal_x = uy * vz - uz * vy
    normal_y = uz * vx - ux * vz
    normal_z = ux * vy - uy * vx

    # Calculamos la magnitud del vector y dividimos cada punto entre la magnitud para obtener el vector normalizado
    magnitud = math.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
    return (normal_x/magnitud, normal_y/magnitud, normal_z/magnitud)


def build_wheel(radio, num_lados, ancho):
    vertices = []
    faces = []
    normals = []

    # Primero calculamos los vértices, esto lo hacemos calculando el ángulo por cada uno de los lados de el círculo, y de esta manera podemos calcular con seno para y y con coseno para x el punto de los vértices en los que se va a ir formando el círculo. Esto lo agregamos a nuestra matriz de vértices y dependiendo la cara lo mandamos con -ancho o ancho entre 2. Esto es para que cada cara quede a la altura necesaria del ancho.
    for i in range(num_lados):
        angulo = i * 2 * math.pi / num_lados
        x = radio * math.cos(angulo)
        y = radio * math.sin(angulo)
        vertices.append((x, y, ancho / 2))  
        vertices.append((x, y, -ancho / 2))

    # Podteriormente mandamos dos últimos vectores, para los centros de los lados, para que los triángulos se puedan ir conectando en el centro para formar los lados
    vertices.append((0, 0, ancho / 2))    
    vertices.append((0, 0, -ancho / 2))   

    #Calculamos los dos índices del centro de los círculos de los lados, agarramos los dos últimos vértices de la matriz de caras
    centro_derecha = len(vertices) - 2
    centro_izquierda = len(vertices) - 1
    

    # Para calcular la matriz de cómo van a ir las caras de al redeor lo que hago es crear 4 variables. La primera es el vértice izquiero de mi rueda, la segunda es el vértice derecho de mi rueda, y despues la siguiente derecha y la siguiente izquierda. La izquierda me garantiza que los números van a ser los nones y la derecha que los número van a ser los pares. 
    for i in range(num_lados):
        izquierda = i * 2 + 1
        derecha = i * 2 + 2

        #Aquí utilizamos modulo para que sea cómo un wrapp arount para los vértices por ejemplo el primero y el último que van unidos juntos
        siguiente_izquierda = ((i + 1) % num_lados) * 2 + 1
        siguiente_derecha = ((i + 1) % num_lados) * 2 + 2

        # Aqui appendeamos las caras conforme los triángulos deben de ser unidos para que se forme de manera correcta el círculo
        faces.append((izquierda, derecha, siguiente_derecha))
        faces.append((izquierda, siguiente_derecha, siguiente_izquierda))
        faces.append((centro_derecha + 1, izquierda, siguiente_izquierda))
        faces.append((centro_izquierda + 1, siguiente_derecha, derecha))

        v1, v2, v3 = vertices[izquierda-1], vertices[derecha-1], vertices[siguiente_derecha-1]
        normal_side = calculate_normals(v1, v2, v3)
        normals.append(normal_side)  # Normal for both triangles on the side

        # Add two triangles for each side face
        faces.append((izquierda, derecha, siguiente_derecha))
        faces.append((izquierda, siguiente_derecha, siguiente_izquierda))

        # Now, use the same normal for both triangles
        faces.append((centro_derecha + 1, izquierda, siguiente_izquierda))
        faces.append((centro_izquierda + 1, siguiente_derecha, derecha))

    # Utilizamos nuestras funciones de calcular las normales para calcular las normales de los lados derechos y los lados izquierdos , pasando los vértices para cada lado
    normal_derecha = calculate_normals(vertices[centro_derecha], vertices[0], vertices[2])
    normal_izquierda = calculate_normals(vertices[centro_izquierda], vertices[1], vertices[3])

    normals.append(normal_derecha) 
    normals.append(normal_izquierda) 

    with open('Tarea2 Gil/Assets/Models/wheel.obj', 'w') as file:
        file.write("# OBJ file format\n")
        for vertex in vertices:
            file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for normal in normals:
            file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")

        #Esta función asigna las normales a las caras específicas, i siendo el índice en el que se encuentra la cara de el circulo
        for i, face in enumerate(faces):
            # Lo que hace el primer if es checar si es que i es menor a el numero de caras totales de la llanta menos el número de lados multiplicado por 2 (cada triángulo usado para formar el cuadrado de los lados) Si es menor, entonces está dentro de los índices de las caras que forman el contorno del círculo y se asigna el índice de normal correspondiente 
            if i < len(faces) - num_lados * 2:
                #Se agrupa para que compartan las normales las dos caras del triángulo que comparten el cuadrado
                face_normal = i // 2 + 1

            # Igualmente aquí hacemos lo mismo para determinar si i es menor a el número total de caras menos el número de lados. De esta manera determinamos si estámos usando caras que forman el lado derecho del círculo y le asignamos el normal correspondiente
            elif i < len(faces) - num_lados:
                #Todas las caras comparten las mismas normales
                face_normal = num_lados * 2 + 1
            
            else:
            # Por ultimo asignamos las normales a los índices que se encuentran dentro del rango del lado derecho del circulo 
                #Todas las caras comparten las mismas normales
                face_normal = num_lados * 2 + 2

            ##Escribimos la normal en el formato correspondiente de las normales
            file.write(f"f {face[0]}//{face_normal} {face[1]}//{face_normal} {face[2]}//{face_normal}\n")

    return vertices, faces, normals


def main():
    radio_input = input("Escribe el radio o presiona Enter para usar el valor por defecto: ")
    ancho_input = input("Escribe el ancho o presiona Enter para usar el valor por defecto: ")
    caras_input = input("Escribe el número de caras o presiona Enter para usar el valor por defecto: ")

    default_radio = 1.0
    default_ancho = 0.5
    default_caras = 8

    radio = float(radio_input) if radio_input else default_radio
    ancho = float(ancho_input) if ancho_input else default_ancho
    caras = int(caras_input) if caras_input else default_caras

    build_wheel(radio, caras, ancho)



main()