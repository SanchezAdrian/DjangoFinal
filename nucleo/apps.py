from django.apps import AppConfig


class NucleoConfig(AppConfig):
    name = 'nucleo'
    verbose_name ="Taller"

class Validate():
    def validateMatricula(matricula):
        if matricula[:4].isalpha():
            if matricula[4:7].isnumeric():
                return True
        return False
      
