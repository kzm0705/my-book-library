from pykakasi import kakasi

kks = kakasi()



# for fr in ["J", "K", "a", "E"]:

#     kakas.setMode(fr, "H")

#     conv = kakas.getConverter()
#     print(conv.do("封印再度　who in side"))

def generate_hira(text: str) -> str:

    result = kks.convert("あいうえおabcdfg挨拶")

    kana = "".join([item['hira'] for item in result]).lower()

    return kana