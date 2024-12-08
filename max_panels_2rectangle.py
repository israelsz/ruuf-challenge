from collections import deque

def initialize_two_rectangle_roof(roofWidth, roofHeight, desplazamientoX, desplazamientoY):
    # Calcular las dimensiones del array resultante
    minRowIndex = min(0, desplazamientoY)
    maxRowIndex = max(roofHeight, desplazamientoY + roofHeight)
    minColIndex = min(0, desplazamientoX)
    maxColIndex = max(roofWidth, desplazamientoX + roofWidth)

    totalHeight = maxRowIndex - minRowIndex
    totalWidth = maxColIndex - minColIndex

    # Crear la matriz llenando todas las celdas como ocupadas
    roof = []
    for _ in range(totalHeight):
        row = []
        for _ in range(totalWidth):
            row.append(True)
        roof.append(row)

    # Offset para indexar correctamente en la matriz
    # Asi se ajusta la posición dentro de la matriz resultante
    offset_row = -minRowIndex
    offset_col = -minColIndex

    # Marcar el área del rectángulo A

    for row in range(offset_row, offset_row + roofHeight):
        for column in range(offset_col, offset_col + roofWidth):
            roof[row][column] = False

    # Marcar el área del rectángulo B

    b_start_row = offset_row + desplazamientoY
    b_start_col = offset_col + desplazamientoX

    for row in range(b_start_row, b_start_row + roofHeight):
        for column in range(b_start_col, b_start_col + roofWidth):
            roof[row][column] = False

    return roof, totalHeight, totalWidth

# Verifica si cada celda necesaria para colocar un panel estan disponibles (en False)
def can_place(roof, startRow, startColumn, height, width):
    for r in range(startRow, startRow + height):
        for c in range(startColumn, startColumn + width):
            if roof[r][c]:
                return False
    return True

# Verifica si un panel cabe dentro de las dimensiones del techo
def within_bounds(startRow, startColumn, height, width, roofHeight, roofWidth):
    if startRow + height <= roofHeight and startColumn + width <= roofWidth:
        return True
    return False

# Verifica si se puede colocar un panel tomando como posicion inicial [startRow, startColumn] considerando limites y celdas libres
# Combina las funciones can_place y whithin_bounds para esto
def can_place_panel(roof, startRow, startColumn, panelHeight, panelWidth, roofHeight, roofWidth):
    # Check panel cabe en el techo
    if not within_bounds(startRow, startColumn, panelHeight, panelWidth, roofHeight, roofWidth):
        return False
    # Check celdas estan libres
    return can_place(roof, startRow, startColumn, panelHeight, panelWidth)

# Permite crear una copia del techo
def copy_roof(roof):
    roof_copy = []
    for row in roof:
        new_row = row[:]
        roof_copy.append(new_row)
    return roof_copy

# Modifica un panel, permitiendo cambiar el estado de las celdas
def place_panel(roof, startRow, startColumn, height, width, occupy):
    for r in range(startRow, startRow + height):
        for c in range(startColumn, startColumn + width):
            roof[r][c] = occupy

# Calcula y retorna la siguiente celda en el techo
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

def calculate_max_panels_bfs(roofHeight, roofWidth, panelHeight, panelWidth, desplazamientoX, desplazamientoY):
    # Inicializar el techo doble p y obtener sus dimensiones
    initial_roof, finalHeight, finalWidth = initialize_two_rectangle_roof(roofWidth, roofHeight, desplazamientoX, desplazamientoY)
    pretty_print(initial_roof)

    # Actualizar las dimensiones del techo
    roofHeight = finalHeight
    roofWidth = finalWidth

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
                max_panels = placedPanelCount
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

# Ejecuciones
roofHeight, roofWidth = 2, 3
panelHeight, panelWidth = 1, 2
desplazamientoX, desplazamientoY = 1, 1

max_number_panels = calculate_max_panels_bfs(roofHeight, roofWidth, panelHeight, panelWidth, desplazamientoX, desplazamientoY)
print("\nTecho: ",roofHeight, "x", roofWidth)
print("Panel: ",panelHeight, "x", panelWidth)
print("Desplazamiento -  x:",desplazamientoX, " y:", desplazamientoY)
print("Max numero de paneles que caben:", max_number_panels, "\n")
#----------------------------------------------
roofHeight, roofWidth = 4, 3
panelHeight, panelWidth = 1, 3
desplazamientoX, desplazamientoY = 2, 1

max_number_panels = calculate_max_panels_bfs(roofHeight, roofWidth, panelHeight, panelWidth, desplazamientoX, desplazamientoY)
print("\nTecho: ",roofHeight, "x", roofWidth)
print("Panel: ",panelHeight, "x", panelWidth)
print("Desplazamiento: ",desplazamientoX, "x", desplazamientoY)
print("Max numero de paneles que caben:", max_number_panels, "\n")