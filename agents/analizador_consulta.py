import re

from agents.base_agent import BaseAgent


class AnalizadorConsultaAgent(BaseAgent):
    """Extrae señales simples de una consulta de moda."""

    def __init__(self):
        super().__init__("AnalizadorConsulta")

    def execute(self, context):
        query = context["user_input"].strip().lower()
        categories = {
            "camisa": "camisas", "camiseta": "camisas", "remera": "camisas",
            "pantalón": "pantalones", "pantalon": "pantalones",
            "vestido": "vestidos", "zapatilla": "calzado", "zapato": "calzado",
            "abrigo": "abrigos", "campera": "abrigos",
        }
        colors = {"negro", "blanco", "azul", "rojo", "verde", "beige"}
        category = next((value for key, value in categories.items() if key in query), None)
        color = next((value for value in colors if re.search(rf"\b{value}\b", query)), None)
        return {**context, "analysis": {"category": category, "color": color}}