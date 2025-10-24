import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_create_user(name: str, email: str, password: str):

    data = {"name": name,
            "email": email,
            "password": password}
    
    print(f"Creating user: {name}\n")

    r = requests.post(f"{BASE_URL}/users", json=data)

    resp = r.json()
    requestOk = r.status_code

    if requestOk == 200:
        id = resp["id"]
        print(f"User created correctly with id {id}")
    else:
        msg = resp["detail"]
        print(f"There has been a problem registering the user due to {msg}\n")

def test_list_users():
    
    print(f"####### User list #######\n")

    r = requests.get(f"{BASE_URL}/users")

    resp = r.json()
    requestOk = r.status_code

    if requestOk == 200:
        for i, user in enumerate(resp, start=1):
            print(f"User {i}: {user['name']}")
    else:
        msg = resp["detail"]
        print(f"There has been a problem listing the users due to {msg}\n")


def test_create_note(title: str, file_path: str, user_id: int):
    print(f"\n\n####### Create note #######\n")

    data = {"title": title,
            "file_path": file_path,
            "user_id": user_id}

    r = requests.post(f"{BASE_URL}/notes", json=data)
    resp = r.json()
    requestOk = r.status_code

    if requestOk == 200 or 201:
        print("Note created correctly as:\n")
        print(f"Title: {resp['title']}")
        print(f"User ID: {resp['user_id']}")

def test_list_notes():
    print(f"\n\n####### Notes list #######\n")

    r = requests.get(f"{BASE_URL}/users")

    resp = r.json()
    requestOk = r.status_code

    print(resp)

    if requestOk == 200:
        for note in resp:
            id_ = note.get('id')
            title = note.get('title', '(sin título)')
            print(f"Note {id_}: {title}")
    else:
        msg = resp["detail"]
        print(f"There has been a problem listing the users due to {msg}\n")

def test_get_note(id: int):
    print(f"\n\n####### Get note by id #######\n")

    r = requests.get(f"{BASE_URL}/notes/{id}")

    resp = r.json()
    requestOk = r.status_code

    print(r.status_code)

    if requestOk == 200 or 201:
        print(f"Note title: {resp['title']}\n")
        print(f"Note title: {resp['content']}")
    else:
        print(f"Note not found in database")


def test_delete_note():
    r = requests.delete(f"{BASE_URL}/notes/1")
    print(r.status_code)


if __name__ == "__main__":
    print("########### Iniciando pruebas de la API ###########")
    test_create_user("Pedro", "pedro@romero.com", "superSeguro123")
    test_create_user("Pedrito", "paloma@romero.com", "superSeguro123")
    test_list_users()
    #test_create_note("Probando", "./notas/limones.txt", 1)
    test_list_notes()
    test_get_note(1)
    test_delete_note()
    print("\n✅ Todas las pruebas finalizadas.")