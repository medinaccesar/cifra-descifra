from utils.locale_manager import _

class BarraProgresoConsola():

    def __init__(self, total):
        self._total = total
        self._completado = 10  
        self._progreso = _('Progreso')
        self._completo = _('Completo')  
        
    def dibuja_bp (self, porcentaje, decimales = 0, relleno = '█' , print_end = "\r"):
      
        self._completado = self._completado + porcentaje
        percent = ("{0:." + str(decimales) + "f}").format(self._completado)
        total_rellenedado = int(self._completado)
        barra = relleno * total_rellenedado + '=' * (self._total - total_rellenedado)        
        print(f'\r{self._progreso} |{barra}| {percent}% {self._completo}', end = print_end)
       
        if self._completado == self._total: 
            print()