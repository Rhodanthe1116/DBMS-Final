import pprint
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

pp = pprint.PrettyPrinter(indent=4)

# basic select
def test_comparison_operation(test_client:TestClient):
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
            }
        }
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
    # response = test_client.get("/graphql/")
    # response = test_client.get("/docs")
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected



# basic projection
def test_projection(test_client:TestClient):
    query = """{
            Player {
                name
                age
            }
        }
        """

    expected = {
        "data": {
            "Player": [
            {
                "name": "Otani",
                "age": 25
            },
            {
                "name": "Kershaw",
                "age": 31
            },
            {
                "name": "Valender",
                "age": 35
            },
            {
                "name": "Tax",
                "age": 33
            }
            ]
        }
    }

    response = test_client.post("/graphql/", data=query)
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected


# basic rename
def test_rename(test_client:TestClient):
    query = """{
            Player(where: { age: { _gt: 30 } }) {
                player: name
                nation: nationality
            }
        }
        """

    expected = {
        "data": {
            "Player": [
            {
                "player": "Kershaw",
                "nation": "USA"
            },
            {
                "player": "Valender",
                "nation": "USA"
            },
            {
                "player": "Tax",
                "nation": "USA"
            }
            ]
        }
    }

    response = test_client.post("/graphql/", data=query)
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected



# basic equijoin
def test_equijoin(test_client:TestClient):
    query = """{
            Player {
                name
                team {
                team_name
                city
                }
            }
        }
        """

    expected = {
        "data": {
            "Player": [
            {
                "name": "Otani",
                "team": {
                "team_name": "Dodger",
                "city": "LA"
                }
            },
            {
                "name": "Kershaw",
                "team": {
                "team_name": "Yankees",
                "city": "New York"
                }
            },
            {
                "name": "Valender",
                "team": {
                "team_name": "Red sox",
                "city": "Boston"
                }
            },
            {
                "name": "Tax",
                "team": {
                "team_name": "Red sox",
                "city": "Boston"
                }
            }
            ]
        }
    }

    response = test_client.post("/graphql/", data=query)
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected



# basic natural join
def test_naturaljoin(test_client:TestClient):
    query = """{
            Player {
                name
                team {
                team_name
                city
                }
            }
        }
        """

    expected = {
        "data": {
            "Player": [
            {
                "name": "Otani",
                "team": {
                "team_name": "Dodger",
                "city": "LA"
                }
            },
            {
                "name": "Kershaw",
                "team": {
                "team_name": "Yankees",
                "city": "New York"
                }
            },
            {
                "name": "Valender",
                "team": {
                "team_name": "Red sox",
                "city": "Boston"
                }
            },
            {
                "name": "Tax",
                "team": {
                "team_name": "Red sox",
                "city": "Boston"
                }
            }
            ]
        }
    }

    response = test_client.post("/graphql/", data=query)
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected


# TODO: basic theta join, or maybe need to nested query
def test_thetajoin(test_client:TestClient):
    query = """{
        }
        """

    expected = {
    }

    response = test_client.post("/graphql/", data=query)
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected


# basic in
def test_in_operator(test_client:TestClient):
    query = """{
            Player(where: { age:{_in: [25, 31, 35] }}) {
                name
                age
            }
        }
        """

    expected = {
        "data": {
            "Player": [
            {
                "name": "Otani",
                "age": 25
            },
            {
                "name": "Kershaw",
                "age": 31
            },
            {
                "name": "Valender",
                "age": 35
            }
            ]
        }
    }

    response = test_client.post("/graphql/", data=query)
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected



# TODO: basic in2 Need to fix nested query
def test_in_operator2(test_client:TestClient):
    query = """{
            Player(where: { age:{_in: [25, 31, 35] }}) {
                name
                age
            }
        }
        """

    expected = {
        "data": {
            "Player": [
            {
                "name": "Otani",
                "age": 25
            },
            {
                "name": "Kershaw",
                "age": 31
            },
            {
                "name": "Valender",
                "age": 35
            }
            ]
        }
    }

    response = test_client.post("/graphql/", data=query)
    pp.pprint(response)
    pp.pprint(response.json())
    assert response.json() == expected