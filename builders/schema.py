import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)

def build_schema() -> strawberry.Schema:
    return schema


def build_schema_from_infile():
    pass


def build_schema_from_database():
    pass
