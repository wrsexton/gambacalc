# TODO - Currently uses CSV, look into using a SQLAlchemy database and setting it up as its own container?
import logging
import pandas as pd

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_type(row, typestring):
    return row["Type 1"] == typestring or row["Type 2"] == typestring


def is_mega(name):
    return "Mega " in name


def is_primal(name):
    return "Primal " in name


def is_alt_deoxys(name):
    return "Deoxys" in name and "DeoxysNormal" not in name


def is_gen(gen, row):
    name = row["Name"]
    # Don't count Deoxys alt forms
    # TODO - Uncertain if there are conditions under which these should be counted
    if is_alt_deoxys(name):
        return False
    
    # Megas and Primals do not exist before gen 6
    if gen < 6 and \
        (is_mega(name) or is_primal(name)):
        return False
    
    return row["Generation"] <= gen
    


def calculate_chance_of_type_in_team(pokemon_type, team_size, gen):
    # Set up empty lists for populating with data
    pokemon_of_type = []
    pokemon = []

    # Read CSV of pokemon data to populate DataFrame ( df )
    df = pd.read_csv('/home/src/calc/data/pokemon.csv')

    # Iterate over data to populate empty lists
    # TODO - Messy, inefficient.  
    #      Refactoring suggestions:
    #      - Filter by generation in advance before iterating, 
    #           then clean out stragglers ( Megas, Primals, Deoxys Forms )
    #      - List comprehension could make this much better.
    for index, row in df.iterrows():
        if is_gen(gen, row):
            name = row["Name"]
            pokemon.append(name)
            if is_type(row, pokemon_type):
                pokemon_of_type.append(name)
    
    # Grab total pokemon count from fully populated list
    total_pokemon = len(pokemon)
    # Grab pokemon count of specified type being queried
    total_pokemon_of_type = len(pokemon_of_type)
    # All things equal, this is the chance of a pokemon with that type appearring
    chance_of_type = total_pokemon_of_type / total_pokemon
    # This is the chance of a different type appearring.
    chance_of_other_type = 1 - chance_of_type
    # This is the chance of all pokemon on a team of size 'team_size' being a different type
    chance_of_no_pokemon_of_type = pow(chance_of_other_type, team_size)
    # Thus, this is the chance of a single pokemon of the supplied type appearing on the team
    chance_of_pokemon_of_type = 1 - chance_of_no_pokemon_of_type
    
    logger.info(f"Total pokemon:\n {total_pokemon}")
    logger.info(f"{pokemon_type} pokemon:\n {total_pokemon_of_type}")
    logger.info(f"{pokemon_type} Type Chance Per Pokemon:\n {chance_of_type * 100} %")
    logger.info(f"Non {pokemon_type} Type Chance Per Pokemon:\n {chance_of_other_type * 100} %")
    logger.info(f"Percent chance of no {pokemon_type} Type on Team of Size {team_size}:\n {chance_of_no_pokemon_of_type * 100} %")
    logger.info(f"Percent chance of {pokemon_type} Type on Team of Size {team_size}:\n {chance_of_pokemon_of_type * 100} %")

    # Return the calculated chance as a percentage, limited to 3 decimal places.
    return round(chance_of_pokemon_of_type*100, 2)
