from agents.analizador_consulta import AnalizadorConsultaAgent
from agents.refinador_consulta import RefinadorConsulta


class DemoCoordinator:
    """Orquesta el flujo mínimo de análisis y refinamiento."""

    def __init__(self, catalog):
        self.catalog = catalog
        self.analyzer = AnalizadorConsultaAgent()
        self.refiner = RefinadorConsulta()

    def process_query(self, user_input):
        context = self.analyzer.execute({"user_input": user_input})
        context = self.refiner.execute(context)
        if context["refinement"]["needs_clarification"]:
            return {**context, "response": context["refinement"]["question"], "products": []}

        analysis = context["analysis"]
        products = [
            product for product in self.catalog
            if product["category"] == analysis["category"]
            and (not analysis["color"] or product["color"] == analysis["color"])
        ]
        response = (
            f"Encontré {len(products)} recomendación(es) para tu búsqueda."
            if products else "No encontré coincidencias en el catálogo de demo."
        )
        return {**context, "response": response, "products": products}