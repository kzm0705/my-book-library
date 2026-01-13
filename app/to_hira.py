from pykakasi import kakasi
import os
kks = kakasi()

def generate_hira(text: str) -> str:
    result = kks.convert(text)
    kana = "".join([item['hira'] for item in result]).lower()
    return kana

# print(os.path.dirname((os.path.abspath(__file__))))
# print(os.path.abspath(__file__))
