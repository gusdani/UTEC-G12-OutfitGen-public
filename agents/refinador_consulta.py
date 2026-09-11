from agents.base_agent import BaseAgent


class RefinadorConsulta(BaseAgent):
    """Decide si la consulta tiene información suficiente para recomendar."""

    def __init__(self):
        super().__init__("RefinadorConsulta")

    def execute(self, context):
        missing = [] if context["analysis"].get("category") else ["tipo de prenda"]
        return {
            **context,
            "refinement": {
                "needs_clarification": bool(missing),
                "missing": missing,
                "question": "¿Qué tipo de prenda estás buscando?" if missing else None,
            },
        }