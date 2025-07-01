# agent.py

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

class SemanaExerciciosAgent:
    def __init__(self, plano_path="plano_ensino.txt", openai_api_key=None, model="gpt-4.1-mini", temperature=0.3):
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(openai_api_key=self.api_key, model=model, temperature=temperature)

        with open(plano_path, "r", encoding="utf-8") as f:
            self.plano = f.read()

        self.prompt = PromptTemplate.from_template(
            # Prompt especificando o papel do assistente, bem como o momento educacional dos estudantes, 
            # informações que podem, posteriormente, serem adicionadas pelo estudante para tratarmos de
            # outras disciplinas e/ou blocos. 
            # O agente deve: Indicar as subcompetências da semana, 5 exercícios divididos em teóricos, 
            # práticos e desafio, e por fim recomendar que busque um monitor em caso de dúvidas.
            # Ao fim é feito um self check, que em uma melhoria pode ser uma nova etapa de lagchain
            
            """
            You are an educational assistant at a technology college. 
            Your students are in the first six months of a Data Science or Database undergraduate program. 
            Based on the teaching plan below (written in Portuguese):

            {plano}

            Explain to the student what are the subcompetencies he is supposed to be learning righ now and their importance.
            Generate a list of five practice exercises for a student currently in **week {semana}**.
            The exercises should reinforce the content studied during that week. You may include previous topics, 
            but never content from future weeks.

            Two of the exercises should be theoretical, and the others practical, with the last one being especially challenging.
            They should be clearly marked, with "Teórico", "Prático" and "Desafio" in parenthesis at the beggining of each question.
            The output should be a numbered list with clear instructions, and **everything has to be written in Portuguese**.
            At the end, recommend that the student seek help from a tutor ("monitor" in portuguese) if they have any questions.

            Before generating your response, double-check that:
            - The subcompetences informed are exactly the same of the teaching plans in the corresponding week
            - The list includes exactly two theoretical exercises, two practical ones, and one that is especially challenging.
            - All instructions and content are written in Portuguese.
            - You recommend that the student seek help from a "monitor" if they have any questions.

            Do not output your answer until you've confirmed all items in this checklist.
            """
        )

    def gerar_exercicios(self, semana):
        full_prompt = self.prompt | self.llm
        return full_prompt.invoke({
            "semana": semana,
            "plano": self.plano
        }).content