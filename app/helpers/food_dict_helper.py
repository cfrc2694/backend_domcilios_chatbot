""" Helper functions for food_dict module """


def get_str_from_food_dict(food_dict: dict) -> str:
    """Convert food dict to string"""
    result = ", ".join(
        [f"{int(value)} {key}" for key, value in food_dict.items()]
    )
    return result
