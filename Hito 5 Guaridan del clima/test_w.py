import apis  # O el módulo donde está get_advice_gemini

def test_gemini():
    env_vars = {
        "GEMINI_API_KEY": "tu_api_key_aqui"
    }
    climate = "Día lluvioso y frío, 10 grados Celsius"
    ok, tip = apis.get_advice_gemini(climate, api_key=env_vars.get("GEMINI_API_KEY"))
    print("ok:", ok)
    print("tip:", tip)

if __name__ == "__main__":
    test_gemini()