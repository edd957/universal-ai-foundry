from universal_ai_foundry.blueprints import get_blueprint, list_blueprints


def test_builtin_blueprints_cover_core_modalities() -> None:
    modalities = {blueprint.modality.value for blueprint in list_blueprints()}

    assert modalities == {"llm", "image", "audio", "video"}


def test_get_blueprint_returns_copy() -> None:
    first = get_blueprint("llm-lora")
    second = get_blueprint("llm-lora")
    first.name = "changed"

    assert second.name == "llm-lora-starter"

