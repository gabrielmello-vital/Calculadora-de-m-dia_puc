import streamlit as st

from views.student_view import studentView
import pandas as pd
import requests

API_URL = "http://127.0.0.1:5000/alunos"

view = studentView()
opcao = view.render_menu()

if opcao == "Cadastrar Aluno":
    nome, matricula, codigo = view.information_students()
    response = requests.get(f"{API_URL}/criterio/{codigo.upper()}")
    if not codigo:
        st.info("Digite o código da disciplina para começar.")
    else:
        response = requests.get(f"{API_URL}/criterio/{codigo.upper()}")
    
    if response.status_code == 200:
        dados_criterio = response.json()
        nome_criterio = dados_criterio.get("criterio")

        n3 = 0.0
        n4 = 0.0
        if nome_criterio in ['criterio04', 'criterio05', 'criterio08']:
            labels = ["G1", "G2", "G3"]
            notas = view.pedir_notas(labels)
            n1, n2, n3 = notas[0], notas[1], notas[2]
        else: 
            labels = ["G1", "G2"]
            notas = view.pedir_notas(labels)
            n1, n2 = notas[0], notas[1]

        if nome_criterio in ['criterio04', 'criterio05']:
            n4 = st.number_input("Nota da G4 (se houver)", 0.0, 10.0, 0.0)

        if st.button("Finalizar e Salvar"):
            dados_aluno = {
                "name": nome,
                "matricula": matricula,
                "codigo": codigo.upper(),
                "n1": n1, "n2": n2, "n3": n3, "n4": n4
            }
            
            res = requests.post(API_URL, json=dados_aluno)
            
            if res.status_code == 201:
                info = res.json()
                st.success(f"Salvo! Média: {info.get('media')}")
            else:
                st.error("Erro ao processar cálculo no Model.")

elif opcao == "Relatório":
    st.header("Relatório de Alunos")
    try:
        response = requests.get(API_URL)
        dados = response.json()
    except:
        dados = None
        st.error("Erro ao conectar com a API.")

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

                    try:
                        response = requests.delete(f"{API_URL}/{chave_composta}")

                        if response.status_code == 200:
                            st.success(f"Registro {chave_composta} removido com sucesso!")
                            st.rerun() 
                        else:
                            st.error("Erro ao remover: Aluno não encontrado na API.")

                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")
    else:
        st.info("Nenhum aluno cadastrado no sistema.")