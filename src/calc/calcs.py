import pandas as pd
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_type(row, typestring):
    return row["Type 1"] == typestring or row["Type 2"] == typestring


def calculate_chance_of_type_in_team_in_gen_3(pokemon_type, team_size):
    pokemon_of_type = []
    pokemon = []
    df = pd.read_csv('/home/src/calc/data/pokemon.csv')
    for index, row in df.iterrows():
        gen = row['Generation']
        name = row["Name"]
        is_mega = "Mega " in name
        is_primal = "Primal " in name
        is_alt_deoxys = "Deoxys" in name and "DeoxysNormal" not in name
        if gen <= 3 and \
                not is_mega and \
                not is_primal and \
                not is_alt_deoxys:
            pokemon.append(name)
            if is_type(row, pokemon_type):
                pokemon_of_type.append(name)
    total_pokemon = len(pokemon)
    total_pokemon_of_type = len(pokemon_of_type)
    chance_of_type = total_pokemon_of_type / total_pokemon
    chance_of_other_type = 1 - chance_of_type
    chance_of_no_pokemon_of_type = pow(chance_of_other_type, team_size)
    chance_of_pokemon_of_type = 1 - chance_of_no_pokemon_of_type
    
    logger.info(f"Total pokemon:\n {total_pokemon}")
    logger.info(f"{pokemon_type} pokemon:\n {total_pokemon_of_type}")
    logger.info(f"{pokemon_type} Type Chance Per Pokemon:\n {chance_of_type * 100} %")
    logger.info(f"Non {pokemon_type} Type Chance Per Pokemon:\n {chance_of_other_type * 100} %")
    logger.info(f"Percent chance of no {pokemon_type} Type on Team of Size {team_size}:\n {chance_of_no_pokemon_of_type * 100} %")
    logger.info(f"Percent chance of {pokemon_type} Type on Team of Size {team_size}:\n {chance_of_pokemon_of_type * 100} %")

    return round(chance_of_pokemon_of_type*100, 3)
