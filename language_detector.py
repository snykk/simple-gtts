from langdetect import detect

idlang = detect("Hai, apa kabar?")
id2lang = detect("Halo, apa kabar?") 
enlang = detect("Hello, how are you?")
frlang = detect("Bonjour, comment ça va?")

print(idlang)
print(id2lang) # timor leste???
print(enlang)
print(frlang)