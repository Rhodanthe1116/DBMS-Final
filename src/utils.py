from inflection import singularize, pluralize, camelize


def is_join_table(table_name, table_list):
    sides = [pluralize(side) for side in table_name.split("_")]

    if len(sides) != 2:
        return False

    one, two = sides

    return one in table_list and two in table_list


def format_type_name(name):
    return pascal_case(singularize(name))


def pascal_case(string):
    return camelize(string, uppercase_first_letter=True)


def find_model_key(key, models):
    if key in models:
        return key

    plural_key = pluralize(key)

    if plural_key in models:
        return plural_key

    singular_key = singularize(key)

    if singular_key in models:
        return singular_key

    raise Exception(f"Model with {key} does not exist")


def format_field_name(name):
    return camelize(name, uppercase_first_letter=False)
