
import streamlit as st

class studentView:
    def render_menu(self):
            with st.sidebar:
                st.title("Menu Principal")
                escolha = st.radio(
                    "Navegação:",
                    ["Cadastrar Aluno", "Relatório"]
                    
                )
            return escolha
    
    def information_students(self):
        st.header("Novo Cadastro")
        nome = st.text_input("Nome do Aluno")
        codigo = st.text_input("Código da Disciplina (Ex: INF1039)")
        return nome, codigo

    def pedir_notas(self, lista_de_notas):
        notas_digitadas = []
        cols = st.columns(len(lista_de_notas))
        for i, rotulo in enumerate(lista_de_notas):
            with cols[i]:
                nota = st.number_input(f"Nota {rotulo}", 0.0, 10.0, 5.0)
                notas_digitadas.append(nota)
        return notas_digitadas