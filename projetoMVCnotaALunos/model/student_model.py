import json
import os
import threading


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls._instances.get(cls) is None:
                
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]




class studentModel(metaclass=SingletonMeta):
    def __init__(self):
        self.file_path = "alunos.json" 
        self.lista_Alunos = self.LoadFromJson()
        self.disciplinasCriterios = {'MAT4161':self.criterio08, 
                                     'INF1039': self.criterio02, 
                                     'CRE1227':self.criterio05, 
                                     'INF1403':self.criterio02, 
                                     'MAT4200': self.criterio04,
                                     'INF1039':self.criterio02}
       
    
    def LoadFromJson(self):
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)
        
    def save_to_json(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.lista_Alunos, file, indent=4, ensure_ascii=False)

    
    def saveAlunos(self, name, matricula,codD, n1, n2, n3=None, n4=None):
    
        funcao_calculo = self.disciplinasCriterios.get(codD)
        
        if funcao_calculo:
        
            media = funcao_calculo(n1, n2, n3, n4)
        else:
             raise ValueError(f"Erro: A disciplina '{codD}' não possui um critério de avaliação cadastrado.")
        if media >= 6.0:
            situacao = "Aprovado" 
        else:
            situacao = "Não Aprovado"
        if len(matricula) > 7:
            raise ValueError (f"Erro: A matricula '{matricula}'não é valida")
        aluno = {
            "nome": name,
            "matricula":matricula,
            "materia": codD,
            "media": media, 
            "situacao": situacao
        }

        self.lista_Alunos[matricula] = aluno
        self.save_to_json()

        return media
    
    def delete_aluno(self,matricula):
        if matricula in self.lista_Alunos:
            del self.lista_Alunos[matricula] 
            self.save_to_json()
            return True
        return False
              
        
    
    def criterio05(self,n1,n2,n3,n4=None):  

        nf = (n1 +n2 +n3)/3
        if n1>=5 and n2>= 5 and n3>= 5 or (nf>=6):
            return nf

        else:
            if n4 is None:
                return nf

            if n4 >= 3.0:
                soma_duas_maiores = (n1 + n2 + n3) - min(n1, n2, n3)
                return  (soma_duas_maiores + n4)/3

            else:
                return ( (n1+n2+n3+(n4*3)) / 6)

    def criterio08(self,n1,n2,n3=None,n4=None):

        nf = ( (n1*2 ) + (n2*3) ) / 5
        if n1>=3 and n2>= 3  and (nf>=6):
            return nf 
        else:
            if n3 is None:
                return nf
            
            if (n1 < 3 or n2<3) and n3 <3:
                return ((n1 + n2 + (n2*2) ) )/ 4
            else:
                return  ((n1*2 ) + (n2*3 ) + ( n3*5)) / 10
            

    def criterio02(self,n1,n2,n3=None,n4=None):
        nf = (n1 + 2*n2) / 3
        return nf

    def criterio04(self,n1,n2,n3,n4=None):
         
        nf = (n1 +n2 +n3)/3
        if n1>=5 and n2>= 5 and n3>= 5 or (nf>=6):
            return nf
        
        if n4 is None:
            return nf

        else:
            if n4 >= 3.0:
                soma_duas_maiores = (n1 + n2 + n3) - min(n1, n2, n3)
                return  (soma_duas_maiores + n4)/3

            else:
                return ( (n1+n2+n3+(n4*3)) / 6)




    def get_all(self):
        return self.lista_Alunos

        