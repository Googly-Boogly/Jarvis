import unittest

@unittest.expectedFailure
def unit_test_validate_function(function: dict):
    # UNIT TEST FUNCTION
    # example func
    """
    function = {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
    """

    # Check the presence of required key and their types
    assert "name" in function and isinstance(
        function["name"], str
    ), "'name' must be a string."
    assert "description" in function and isinstance(
        function["description"], str
    ), "'description' must be a string."
    assert "parameters" in function and isinstance(
        function["parameters"], dict
    ), "'parameters' must be a dictionary."

    # Check the structure of 'parameters' key
    params = function["parameters"]

    assert (
            "type" in params and params["type"] == "object"
    ), "'type' must be 'object' in parameters."
    assert "properties" in params and isinstance(
        params["properties"], dict
    ), "'properties' must be a dictionary."
    assert "required" in params and isinstance(
        params["required"], list
    ), "'required' must be a list."

    # Check the structure of 'properties' in 'parameters'
    for key, prop in params["properties"].items():
        assert "type" in prop and isinstance(
            prop["type"], str
        ), f"'type' must be a string in properties of {key}."

        if prop["type"] == "array":
            assert (
                    "items" in prop
            ), f"'items' must be present in properties of {key} when type is 'array'."

        # Enum check only if it exists
        if "enum" in prop:
            assert isinstance(
                prop["enum"], list
            ), f"'enum' must be a list in properties of {key}."

    # Check 'required' properties are in 'properties'
    for key in params["required"]:
        assert (
            key in params["properties"]
        ), f"'{key}' mentioned in 'required' must exist in 'properties'."