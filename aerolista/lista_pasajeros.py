# ==============================================================
#  lista_pasajeros.py  ·  Lista enlazada de pasajeros
# ==============================================================
#        head
#         |
#         v
#    +----------+---+    +----------+---+    +----------+---+
#    | #1005    | o-+--->| #1002    | o-+--->| #1009    | o-+---> None
#    | Diana 3C |   |    | Ana 1A   |   |    | Luis 7D  |   |
#    +----------+---+    +----------+---+    +----------+---+
#       data    next        data    next        data    next
#
#  Los pasajeros quedan en ORDEN DE LLEGADA (el orden en que reservaron).
# ==============================================================

from pasajero import Pasajero


class Nodo:
    """Un vagón del tren: lleva un pasajero (data) y el enganche al siguiente (next)."""

    def __init__(self, data):
        self.data = data          # el Pasajero que viaja en este vagón
        self.next = None          # al nacer no está enganchado a nadie


class ListaPasajeros:
    """Lista enlazada simple con todas las reservas del vuelo."""

    # ----------------------------------------------------------
    # ✅ EJEMPLO RESUELTO 1: el constructor
    # ----------------------------------------------------------
    def __init__(self):
        self.head = None          # la cabeza: el primer nodo (None = avión vacío)
        self.cantidad = 0         # cuántas reservas (nodos) hay

    # ----------------------------------------------------------
    # ✅ EJEMPLO RESUELTO 2: ingresar (= insertar_final de la Unidad 3)
    #    Engancha un pasajero NUEVO al final del tren.
    # ----------------------------------------------------------
    def ingresar(self, pasajero):
        nuevo = Nodo(pasajero)                # 1. creo el vagón con el pasajero

        if self.head is None:                 # 2a. Lista vacía:
            self.head = nuevo                 #     el nuevo es la cabeza
        else:                                 # 2b. Lista con nodos:
            actual = self.head                #     pongo el dedo en la cabeza
            while actual.next is not None:    #     mientras NO sea el último...
                actual = actual.next          #     ...avanzo un vagón
            actual.next = nuevo               #     el último ahora apunta al nuevo

        self.cantidad = self.cantidad + 1     # 3. hay una reserva más
        return True

    # ==========================================================
    # ✍ MÉTODOS IMPLEMENTADOS (Evaluados en la rúbrica)
    # ==========================================================

    def esta_vacia(self):
        """Retorna True si no hay ninguna reserva; False si hay al menos una.
        Pista: mira self.head."""
        return self.head is None

    def longitud(self):
        """Retorna cuántas reservas hay.
        Pista: no recorras nada, ya tienes self.cantidad."""
        return self.cantidad

    def listar(self):
        """Retorna una list de Python con TODOS los Pasajero, en orden:
        desde head hasta el último. Si está vacía retorna [].
        ⚠ Guarda el pasajero (actual.data), no el nodo.
        👉 Cuando funcione, ¡el avión se pinta con los asientos ocupados!"""
        resultado = []
        actual = self.head
        while actual is not None:
            resultado.append(actual.data)
            actual = actual.next
        return resultado

    def buscar(self, numero):
        """Búsqueda lineal por número de reserva (int).
        Retorna el Pasajero encontrado o None si no existe."""
        actual = self.head
        while actual is not None:
            if actual.data.numero == numero:
                return actual.data
            actual = actual.next
        return None

    def buscar_por_asiento(self, asiento):
        """Retorna el Pasajero sentado en ese asiento ("7D") o None si está libre.
        👉 Flask lo usa al hacer clic en un asiento rojo y para no
           vender dos veces el mismo asiento."""
        actual = self.head
        while actual is not None:
            if actual.data.asiento == asiento:
                return actual.data
            actual = actual.next
        return None

    def buscar_por_cedula(self, cedula):
        """Retorna el Pasajero con esa cédula (str) o None.
        👉 Flask lo usa para que una persona no reserve dos asientos."""
        actual = self.head
        while actual is not None:
            if actual.data.cedula == cedula:
                return actual.data
            actual = actual.next
        return None

    def modificar(self, numero, nuevo_nombre, nueva_edad, nuevo_asiento):
        """Cambia nombre, edad y asiento del pasajero con ese número.
        Usa buscar(). El nodo NO cambia de lugar en la lista: solo cambia su carga.
        Retorna True si lo modificó, False si no existe."""
        pasajero = self.buscar(numero)
        if pasajero is not None:
            pasajero.nombre = nuevo_nombre
            pasajero.edad = nueva_edad
            pasajero.asiento = nuevo_asiento
            return True
        return False

    def eliminar(self, numero):
        """Cancela la reserva: desengancha el nodo que tiene ese número.
        Piensa en los casos: lista vacía · es la cabeza · está en medio o al
        final · no existe. ¡No olvides restar self.cantidad!
        Retorna el Pasajero eliminado, o None si no existía."""
        # Caso A: Lista vacía
        if self.head is None:
            return None

        # Caso B: El nodo a eliminar es la cabeza
        if self.head.data.numero == numero:
            eliminado = self.head.data
            self.head = self.head.next
            self.cantidad -= 1
            return eliminado

        # Caso C y D: Está en medio, al final o no existe
        anterior = self.head
        actual = self.head.next
        while actual is not None:
            if actual.data.numero == numero:
                anterior.next = actual.next
                self.cantidad -= 1
                return actual.data
            anterior = actual
            actual = actual.next

        return None

    def filtrar_por_clase(self, clase):
        """Retorna una list con los pasajeros de esa clase ("Ejecutiva" o
        "Económica"), en el mismo orden de la lista.
        Pista: cada pasajero sabe su clase con  pasajero.clase()"""
        resultado = []
        actual = self.head
        while actual is not None:
            if actual.data.clase() == clase:
                resultado.append(actual.data)
            actual = actual.next
        return resultado

    # ==========================================================
    # ⭐ RETOS EXTRA (Opcionales)
    # ==========================================================

    def contar_menores(self):
        """Retorna cuántos pasajeros tienen menos de 18 años."""
        contador = 0
        actual = self.head
        while actual is not None:
            if actual.data.edad < 18:
                contador += 1
            actual = actual.next
        return contador

    def pasajeros_de_fila(self, fila):
        """Retorna una list con los pasajeros de una fila específica."""
        resultado = []
        actual = self.head
        while actual is not None:
            try:
                if int(actual.data.asiento[:-1]) == fila:
                    resultado.append(actual.data)
            except (ValueError, TypeError):
                pass
            actual = actual.next
        return resultado

    def mayor(self):
        """Retorna el pasajero de más edad (patrón campeón)."""
        if self.head is None:
            return None
        campeon = self.head.data
        actual = self.head.next
        while actual is not None:
            if actual.data.edad > campeon.edad:
                campeon = actual.data
            actual = actual.next
        return campeon

    def invertir(self):
        """Gira todos los enlaces: el último pasa a ser la cabeza."""
        anterior = None
        actual = self.head
        while actual is not None:
            siguiente = actual.next
            actual.next = anterior
            anterior = actual
            actual = siguiente
        self.head = anterior
