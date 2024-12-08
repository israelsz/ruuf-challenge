from collections import deque

#Crea una matriz 2d que representa el techo. Se inicia cada celda en False lo que significa que esta libre
def initialize_roof(roofWidth, roofHeight):
    roof = []
    for _ in range(roofHeight):
        row = []
        for _ in range(roofWidth):
            row.append(False)
        roof.append(row)
    return roof

#Verifica si cada celda necesaria para colocar un panel estan disponibles (en False)
def can_place(roof, startRow, startColumn, height, width):
    for r in range(startRow, startRow + height):
        for c in range(startColumn, startColumn + width):
            if roof[r][c]:
                return False
    return True

#Verifica si un panel cabe dentro de las dimensiones del techo
def within_bounds(startRow, startColumn, height, width, roofHeight, roofWidth):
    if startRow + height <= roofHeight and startColumn + width <= roofWidth:
        return True
    return False

#Verifica si se puede colocar un panel tomando como posicion inicial [startRow, startColumn] considerando limites y celdas libres
#Combina las funciones can_place y whithin_bounds para esto
def can_place_panel(roof, startRow, startColumn, panelHeight, panelWidth, roofHeight, roofWidth):
    # Check panel cabe en el techo
    if not within_bounds(startRow, startColumn, panelHeight, panelWidth, roofHeight, roofWidth):
        return False
    # Check celdas estan libres
    return can_place(roof, startRow, startColumn, panelHeight, panelWidth)

#Permite crear una copia del techo
#Esto es necesario para no modificar el techo original
def copy_roof(roof):
    roof_copy = []
    for row in roof:
        #copia la fila actual
        new_row = row[:]
        roof_copy.append(new_row)
    return roof_copy

#Modifica un panel, permitiendo cambiar el estado de las celdas
#Empieza desde [startRow, startColumn] y modifica un area de [height, width]
def place_panel(roof, startRow, startColumn, height, width, occupy):
    for r in range(startRow, startRow + height):
        for c in range(startColumn, startColumn + width):
            roof[r][c] = occupy

#Calcula y retorna la siguiente celda en el techo
#La direccion de avance es de izquierda a derecha y luego hacia abajo
def next_position(currentRow, currentColumn, roofWidth):
    nextColumn = currentColumn + 1
    nextRow = currentRow
    if nextColumn >= roofWidth:
        nextColumn = 0
        nextRow = currentRow + 1
    return nextRow, nextColumn

def pretty_print(roof):
    print("Techo inicial:\n")
    for row in roof:
        print(row)

#Funcion principal que calcula la cantidad maxima de paneles que caben en el techo
def calculate_max_panels_bfs(roofHeight, roofWidth, panelHeight, panelWidth):
    initial_roof = initialize_roof(roofWidth, roofHeight)
    #pretty_print(initial_roof)
    max_panels = 0

    # Cada estado tiene: (roof, placedPanelCount, currentRow, currentColumn) -> Tupla
    # roof: Techo actual en el estado 
    # PlacedPanelCount: Cantidad de paneles colocados en el estado
    # currentRow, currentColumn: Posicion actual en el techo que se esta evaluando en el estado

    queue = deque()
    queue.append((initial_roof, 0, 0, 0))

    #Se ejecuta mientras haya estados en la cola
    while queue:
        roof, placedPanelCount, currentRow, currentColumn = queue.popleft()

        # Verificacion: Si ya hemos pasado la ultima fila no hay mas celdas para evaluar
        if currentRow >= roofHeight:
            if placedPanelCount > max_panels:
                max_panels = placedPanelCount #Actualiza la cantidad maxima de paneles encontrada
            continue
        
        #Caso 1: Si la celda actual esta ocupada se pasa a la siguiente
        if roof[currentRow][currentColumn]:
            newRow, newColumn = next_position(currentRow, currentColumn, roofWidth)
            queue.append((roof, placedPanelCount, newRow, newColumn))
            continue
        
        #Caso 2: Si la celda esta libre se intenta colocar un panel sin rotar
        if can_place_panel(roof, currentRow, currentColumn, panelHeight, panelWidth, roofHeight, roofWidth):
            new_roof = copy_roof(roof)
            place_panel(new_roof, currentRow, currentColumn, panelHeight, panelWidth, True)
            newRow, newColumn = next_position(currentRow, currentColumn, roofWidth)
            queue.append((new_roof, placedPanelCount+1, newRow, newColumn))

        #Caso 3: Si la celda esta libre se intenta colocar un panel rotado
        if panelHeight != panelWidth: #Verifica si el panel es cuadrado, si lo es se omite este caso
            if can_place_panel(roof, currentRow, currentColumn, panelWidth, panelHeight, roofHeight, roofWidth):
                new_roof = copy_roof(roof)
                place_panel(new_roof, currentRow, currentColumn, panelWidth, panelHeight, True)
                newRow, newColumn = next_position(currentRow, currentColumn, roofWidth)
                queue.append((new_roof, placedPanelCount+1, newRow, newColumn))

        #Caso 4: No colocar ningun panel en esta celda y avanzar a la siguiente
        newRow, newColumn = next_position(currentRow, currentColumn, roofWidth)
        queue.append((roof, placedPanelCount, newRow, newColumn))

    return max_panels

#Ejecuciones

roofHeight, roofWidth = 2, 4
panelHeight, panelWidth = 1, 2

max_number_panels = calculate_max_panels_bfs(roofHeight, roofWidth, panelHeight, panelWidth)
print("Techo: ",roofHeight, "x", roofWidth)
print("Panel: ",panelHeight, "x", panelWidth)
print("Max numero de paneles que caben:", max_number_panels, "\n")

#----------------------------------------------

roofHeight, roofWidth = 3, 5
panelHeight, panelWidth = 1, 2

max_number_panels = calculate_max_panels_bfs(roofHeight, roofWidth, panelHeight, panelWidth)
print("Techo: ",roofHeight, "x", roofWidth)
print("Panel: ",panelHeight, "x", panelWidth)
print("Max numero de paneles que caben:", max_number_panels, "\n")

#----------------------------------------------

roofHeight, roofWidth = 1, 10
panelHeight, panelWidth = 2, 2

max_number_panels = calculate_max_panels_bfs(roofHeight, roofWidth, panelHeight, panelWidth)
print("Techo: ",roofHeight, "x", roofWidth)
print("Panel: ",panelHeight, "x", panelWidth)
print("Max numero de paneles que caben:", max_number_panels, "\n")

#----------------------------------------------

roofHeight, roofWidth = 3, 5
panelHeight, panelWidth = 2, 2

max_number_panels = calculate_max_panels_bfs(roofHeight, roofWidth, panelHeight, panelWidth)
print("Techo: ",roofHeight, "x", roofWidth)
print("Panel: ",panelHeight, "x", panelWidth)
print("Max numero de paneles que caben:", max_number_panels, "\n")
