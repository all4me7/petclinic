import requests
import json


class Setup:
    login = "admin"
    password = "admin"
    headers = {"Content-Type": "application/json"}


class URLS:
    owners = "http://localhost:9966/petclinic/api/owners/"
    pettypes = "http://localhost:9966/petclinic/api/pettypes/"
    pets = "http://localhost:9966/petclinic/api/pets/"
    visits = "http://localhost:9966/petclinic/api/visits/"


class Data:
    add_new_pet_type = json.dumps({"name": "owl"})
    add_new_visit = json.dumps(
        {
            "date": "2022-02-03",
            "description": "add superpowers",
            "id": 1,
            "petId": 1,
        }
    )
    add_new_pet = json.dumps(
        {"birthDate": "2022-02-02", "name": "DarkKnight", "ownerId": 1, "typeId": 1}
    )
    add_new_pet_fail = json.dumps(
        {
            "birthDate": "2015-12-02",
            "name": "Asterix",
            "ownerId": 21,  # Incorrect ID
            "typeId": 1,
            "visits": [],
        }
    )


""" HAPPY PATHS """


def test_add_new_pet_type():
    response = requests.post(
        URLS.pettypes,
        auth=(Setup.login, Setup.password),
        headers=Setup.headers,
        data=Data.add_new_pet_type,
    )

    assert response.status_code == 201, "Incorrect Response"


def test_add_new_visit():
    response = requests.post(
        URLS.visits,
        auth=(Setup.login, Setup.password),
        headers=Setup.headers,
        data=Data.add_new_visit,
    )

    assert response.status_code == 201, "Incorrect Response"

    # Added for evidence
    evidence_response = requests.get(
        URLS.visits,
        auth=(Setup.login, Setup.password),
        headers=Setup.headers,
        data=Data.add_new_visit,
    )

    json_data = json.dumps(evidence_response.json(), indent=4)
    with open("evidence_visits.json", "w") as file:
        file.write(json_data)


def test_add_new_pet_to_owner():
    response = requests.post(
        URLS.pets,
        auth=(Setup.login, Setup.password),
        headers=Setup.headers,
        data=Data.add_new_pet,
    )

    # Not 201 - problem with app, check "test_get_a_list_of_pet_owners.json" file as proof of adding a new pet
    assert response.status_code == 204, "Incorrect Response"


def test_get_a_list_of_pet_owners():
    response = requests.get(
        URLS.owners,
        auth=(Setup.login, Setup.password),
        headers=Setup.headers,
    )

    assert response.status_code == 200, "Incorrect Response"

    # Added for evidence
    json_data = json.dumps(response.json(), indent=4)
    with open("evidence_owners_and_visits.json", "w") as file:
        file.write(json_data)


""" UNHAPPY PATH """


def test_unsuccessful_add_new_pet():
    response = requests.post(
        URLS.pets,
        auth=(Setup.login, Setup.password),
        headers=Setup.headers,
        data=Data.add_new_pet_fail,
    )

    assert response.status_code != 201, "Incorrect Response"
