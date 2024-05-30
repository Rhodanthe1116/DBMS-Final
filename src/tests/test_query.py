import pprint
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

pp = pprint.PrettyPrinter(indent=4)




# basic test
def test_comparison_operation(test_client):
    query = """{
            Player(where: { 
                _or: [
                { _and: [
                    { nationality: { _nlike: "Japan" } },
                    { age: {_gt: 31 } }
                    ]
                },
                { defend_role:{_like:"catcher"}}
                ]
            }) {
                player_id
                name
                nationality
                age
                defend_role
            }}
        """

    expected = {
        "data": {
            "Player": [
            {
                "player_id": 3,
                "name": "Valender",
                "nationality": "USA",
                "age": 35,
                "defend_role": "catcher"
            },
            {
                "player_id": 4,
                "name": "Tax",
                "nationality": "USA",
                "age": 33,
                "defend_role": "catcher"
            }
            ]
        }
    }

    response = test_client.post("/graphql/", data=query)
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected

