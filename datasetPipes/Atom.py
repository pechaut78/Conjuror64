class Atom:
    def __init__(self, params):
        # Initialiser les paramètres à partir du dictionnaire
        self.params = params
        self.ok = True
        self.msg = ''
        self.input = ''
        self.output = ''

    def fail(self, message):
        # Mettre à jour l'état en cas d'échec
        self.ok = False
        self.msg = message
        

    def success(self, input_value):
        # Mettre à jour l'état en cas de succès
        self.ok = True
        self.msg = input_value
        
       

    def process(self):
        # Fonction process par défaut (ne fait rien)
        pass

    def run(self):
        try:
            # Appeler la fonction process
            self.process()
            # Créer le dictionnaire de résultat
            return {
                'ok': self.ok,
                'msg': self.msg,
                'input': self.input,
                'output': self.output
            }
        except Exception as e:
            # En cas d'exception, utiliser la fonction fail
            self.fail(str(e))

            return  {
                'ok': False,
                'msg': self.msg,
                'input': self.input,
                'output': self.output
            }
        
