from coordination.coordinator import DemoCoordinator
from demo.catalog import CATALOG


def test_recommends_by_category_and_color():
    result = DemoCoordinator(CATALOG).process_query("camisa azul")

    assert result["refinement"]["needs_clarification"] is False
    assert [product["name"] for product in result["products"]] == ["Camisa de lino"]


def test_recommends_all_products_in_category_without_color():
    result = DemoCoordinator(CATALOG).process_query("busco una camisa")

    assert [product["name"] for product in result["products"]] == [
        "Camisa urbana",
        "Camisa de lino",
    ]


def test_asks_for_missing_category():
    result = DemoCoordinator(CATALOG).process_query("algo bonito")

    assert result["refinement"]["needs_clarification"] is True
    assert result["products"] == []