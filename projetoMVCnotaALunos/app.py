import streamlit as st
from model.student_model import studentModel
from views.student_view import studentView
import pandas as pd


model = studentModel()
view = studentView()
opcao = view.render_menu()

if opcao == "Cadastrar Aluno":
    nome, matricula, codigo = view.information_students()

    if not codigo:
        st.info("Digite o código da disciplina para começar.")
    else:
        metodo = model.disciplinasCriterios.get(codigo.upper())
        
        if not metodo:
            st.error(f"A disciplina '{codigo.upper()}' não está cadastrada.")
        else:
            nome_criterio = metodo.__name__
            n3 = None
            n4 = None

            if nome_criterio in ['criterio04', 'criterio05', 'criterio08']:
                labels = ["G1", "G2", "G3"]
                notas = view.pedir_notas(labels)
                n1, n2, n3 = notas[0], notas[1], notas[2]
            else: 
                labels = ["G1", "G2"]
                notas = view.pedir_notas(labels)
                n1, n2 = notas[0], notas[1]

            media_previa = metodo(n1, n2, n3)
        
            if media_previa < 6.0 and nome_criterio in ['criterio04', 'criterio05']:
                st.warning(f"Média parcial: {media_previa:.2f}. Aluno em Recuperação!")
                n4 = st.number_input("Digite a nota da G4", 0.0, 10.0, 0.0)
            
            if st.button("Finalizar e Salvar"):
                try:
                   
                    media_final = model.saveAlunos(nome, matricula, codigo.upper(), n1, n2, n3, n4)
                    st.success(f"Aluno salvo! Média Final: {media_final:.2f}")
                   
                except ValueError as e:
                    st.error(f"Erro: {e}")

elif opcao == "Relatório":
    st.header("Relatório de Alunos")
    dados = model.get_all() 
    
    if dados:
        df = pd.DataFrame(list(dados.values()))
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Área de Exclusão")
        
      
        matriculas_disponiveis = df['matricula'].unique()
        matricula_alvo = st.selectbox("Selecione a matrícula:", matriculas_disponiveis)
        
        with st.expander("Gerenciar Disciplinas"):

             df_aluno = df[df['matricula'] == matricula_alvo]


             disciplina_alvo = st.selectbox(
                "Remover qual disciplina?", 
                options=df_aluno['materia']
           )
        
             registro_exato = df_aluno[df_aluno['materia'] == disciplina_alvo]

             if not registro_exato.empty:
                    
                        aluno_final = registro_exato.iloc[0]
                    
                        st.write(f"**Aluno:** {aluno_final['nome']}")
                        st.write(f"**Média:** {aluno_final['media']:.2f}")
                        st.write(f"**Situação:** {aluno_final['situacao']}")

                
             if st.button("Confirmar Remoção", type="primary"):
                        chave_composta = f"{matricula_alvo}_{disciplina_alvo}"

                        if model.delete_aluno(chave_composta):
                            st.success(f"Registro {chave_composta} removido!")
                            st.rerun() 
                        else:
                            st.error("Chave não encontrada no banco de dados.")
    else:
        st.info("Nenhum aluno cadastrado no sistema.")