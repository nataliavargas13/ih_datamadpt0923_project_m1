import argparse

def bicimad(e):
    dest = input("Introduzca embajada o consulado: ")
    print(e)
    print(f"usted a elegido: {dest}")

def bicipark(e):
    print(e)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Tu BisiSpot más cercano")
    parser.add_argument("-e", type=str, help='Debes introducir una embajada o consulado')
    args = parser.parse_args()

if args.e == "bicimad":
    bicimad(args.e)
elif args.e == "bicipark":
    bicipark(args.e)
