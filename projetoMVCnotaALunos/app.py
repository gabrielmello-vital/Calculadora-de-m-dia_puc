import streamlit as st
from model.student_model import studentModel
from views.student_view import studentView
import pandas as pd



model = studentModel()
view = studentView()
opcao = view.render_menu()


if opcao == "Cadastrar Aluno":
    nome, codigo = view.information_students()
    
    if codigo:
        metodo = model.disciplinasCriterios.get(codigo.upper())
        if metodo:
            nome_criterio = metodo.__name__
            n3 =None
            n4 =None
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
            

            if st.button("Salvar no Sistema"):
                media_final = model.saveAlunos(nome, codigo.upper(), n1, n2, n3, n4)
                st.success(f"Cadastro realizado! Média Final: {media_final:.2f}")
    else:
        st.error("Disciplina não cadastrada.")

elif opcao == "Relatório":
    st.header("Alunos Cadastrados")
    dados = model.get_all()

    if dados:
        df = pd.DataFrame(dados)
        st.subheader("Relatório de Alunos")
        st.dataframe(
            df,
            column_config={
                "media": st.column_config.NumberColumn("Média", format="%.2f"),
                "nome": "Nome do Aluno",
                "situacao": "Status Final"
            })
    else:
        st.warning("Nenhum dado encontrado no arquivo JSON.")