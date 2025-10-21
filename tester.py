import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def debug_notes():
    r = requests.get(f"{BASE_URL}/notes")
    print("\n🧠 DEBUG: notas en la base ->")
    try:
        for n in r.json():
            print(f"  id={n.get('id')}, title={n.get('title')}, user_id={n.get('user_id')}")
    except Exception:
        print("  (no se pudo decodificar la respuesta)")

def test_create_user():
    data = {"name": "Paloma RG", "email": "paloma@example.com", "password": "clave1234"}
    r = requests.post(f"{BASE_URL}/users", json=data)
    print(r.status_code, r.json())

def test_list_users():
    r = requests.get(f"{BASE_URL}/users")
    print(r.status_code, r.json())

def test_create_note():
    with open("nota1.txt", "w", encoding="utf-8") as f:
        f.write("Esta es una nota de prueba.")
    data = {"title": "Primera nota", "file_path": "./nota1.txt", "user_id": 1}
    r = requests.post(f"{BASE_URL}/notes", json=data)
    print(r.status_code, r.json())

def test_list_notes():
    r = requests.get(f"{BASE_URL}/notes")
    print(r.status_code, r.json())

def test_get_note():
    r = requests.get(f"{BASE_URL}/notes/7")
    print(r.status_code, r.json())

def test_search_by_expression():
    print("\n➡️ Buscando notas que contengan 'prueba'...")
    r = requests.get(f"{BASE_URL}/notes/searchExp", params={"expression": "prueba"})
    print(r.status_code, end=" ")
    try:
        print(r.json())
    except:
        print("(sin respuesta JSON válida)")

def test_search_by_user():
    print("\n➡️ Buscando notas del usuario 'Paloma RG'...")
    r = requests.get(f"{BASE_URL}/notes/searchUsr", params={"userName": "Paloma RG"})
    print(r.status_code, end=" ")
    try:
        print(r.json())
    except:
        print("(sin respuesta JSON válida)")

def test_delete_note():
    r = requests.delete(f"{BASE_URL}/notes/1")
    print(r.status_code)


if __name__ == "__main__":
    print("🔍 Iniciando pruebas de la API...")
    test_create_user()
    test_list_users()
    test_create_note()
    test_list_notes()
    test_get_note()
    test_search_by_expression()
    test_search_by_user()
    debug_notes()
    test_delete_note()
    print("\n✅ Todas las pruebas finalizadas.")