import streamlit as st

class controllerALuno():
    def __init__(self, model, views):
        self.model = model
        self.views = views

    def start(self):
        choice = self.views.render_menu()
        
        if choice == "1":
            name, matricula, codigo = self.views.information_students()
          
            metodoCalculo = self.model.disciplinasCriterios.get(codigo)

            if not metodoCalculo:
                self.views.exibir_erro("Disciplina não cadastrada!")
            
            elif len(matricula) > 7:
                st.error("Matrícula inválida! (Máximo de 7 caracteres)")
            
            else:
                nome_criterio = metodoCalculo.__name__
             
                n1 = self.views.pedir_nota("G1")
                n2 = self.views.pedir_nota("G2")
                n3 = None
                n4 = None  
                
                if nome_criterio in ['criterio05', 'criterio04', 'criterio08']:
                    n3 = self.views.pedir_nota("G3")
               
                media = metodoCalculo(n1, n2, n3)
                
                if media < 6.0 and nome_criterio in ['criterio05', 'criterio04']: 
                    st.warning(f"Aluno em recuperação (Média Parcial: {media:.2f})")
                    n4 = self.views.pedir_nota("G4")
                   
                    media = metodoCalculo(n1, n2, n3, n4)

                if st.button("Finalizar e Salvar"):
                    self.model.saveAlunos(name, matricula, codigo, n1, n2, n3, n4)
                    self.views.mostrar_resultado_final(media)
                    st.success("Aluno salvo com sucesso!")

        elif choice == "2":
            lista = self.model.get_all()
            self.views.exibir_relatorio(lista)