# Wagfu Service Backend
# common enumerations
# Updated 2 Apr 2026

# PEP8 - UPPER_CASE for constants


from enum import Enum

__all__ = [
    "Dog",
    "Cat",
    "Bird",
    "Fish",
    "Reptile",
    "Rabbit",
    "Other",  # breeds
    "DogColor",
    "CatColor",
    "BirdColor",
    "FishColor",
    "ReptileColor",
    "RabbitColor",
    "OtherColor",  # colors
    "AddressType",
]


class Animals(str, Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    FISH = "fish"
    REPTILE = "reptile"
    RABBIT = "rabbit"
    OTHER = "other"


class Dog(str, Enum):
    LABRADOR = "Labrador"
    GERMAN_SHEPHERD = "German Shepherd"
    GOLDEN_RETRIEVER = "Golden Retriever"
    FRENCH_BULLDOG = "French Bulldog"
    BEAGLE = "Beagle"
    POODLE = "Poodle"
    ROTTWEILER = "Rottweiler"


class Cat(str, Enum):
    PERSIAN = "Persian"
    MAINE_COON = "Maine Coon"
    SIAMESE = "Siamese"
    RAGDOLL = "Ragdoll"
    BENGAL = "Bengal"
    SPHYNX = "Sphynx"
    BRITISH_SHORTHAIR = "British Shorthair"


class Bird(str, Enum):
    BUDGIE = "Budgie"
    COCKATIEL = "Cockatiel"
    AFRICAN_GREY = "African Grey"
    LOVEBIRD = "Lovebird"
    CANARY = "Canary"
    MACAW = "Macaw"
    COCKATOO = "Cockatoo"


class Fish(str, Enum):
    BETTA = "Betta"
    GOLDFISH = "Goldfish"
    GUPPY = "Guppy"
    MOLLY = "Molly"
    ANGELFISH = "Angelfish"
    NEON_TETRA = "Neon Tetra"
    OSCAR = "Oscar"


class Reptile(str, Enum):
    BEARDED_DRAGON = "Bearded Dragon"
    LEOPARD_GECKO = "Leopard Gecko"
    BALL_PYTHON = "Ball Python"
    CORN_SNAKE = "Corn Snake"
    RED_EARED_SLIDER = "Red-Eared Slider"
    VEILED_CHAMELEON = "Veiled Chameleon"
    IGUANA = "Iguana"


class Rabbit(str, Enum):
    HOLLAND_LOP = "Holland Lop"
    MINI_REX = "Mini Rex"
    NETHERLAND_DWARF = "Netherland Dwarf"
    LIONHEAD = "Lionhead"
    FLEMISH_GIANT = "Flemish Giant"
    ENGLISH_ANGORA = "English Angora"
    DUTCH_RABBIT = "Dutch Rabbit"


class Other(str, Enum):
    HAMSTER = "Hamster"
    GUINEA_PIG = "Guinea Pig"
    FERRET = "Ferret"
    CHINCHILLA = "Chinchilla"
    HEDGEHOG = "Hedgehog"
    SUGARGLIDER = "Sugarglider"
    RAT = "Rat"


class DogColor(str, Enum):
    BLACK = "Black"
    WHITE = "White"
    BROWN = "Brown"
    GOLDEN = "Golden"
    BRINDLE = "Brindle"
    CREAM = "Cream"


class CatColor(str, Enum):
    BLACK = "Black"
    WHITE = "White"
    CALICO = "Calico"
    TABBY = "Tabby"
    GINGER = "Ginger"
    GREY = "Grey"
    TORTOISESHELL = "Tortoiseshell"


class BirdColor(str, Enum):
    BLUE = "Blue"
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"
    WHITE = "White"
    MULTI_COLORED = "Multi-colored"
    GREY = "Grey"


class FishColor(str, Enum):
    RED = "Red"
    BLUE = "Blue"
    GOLD = "Gold"
    SILVER = "Silver"
    ORANGE = "Orange"
    SPOTTED = "Spotted"
    NEON = "Neon"


class ReptileColor(str, Enum):
    GREEN = "Green"
    BROWN = "Brown"
    YELLOW = "Yellow"
    GREY = "Grey"
    ORANGE = "Orange"
    PATTERNED = "Patterned"
    BLACK = "Black"


class RabbitColor(str, Enum):
    WHITE = "White"
    BLACK = "Black"
    GREY = "Grey"
    CINNAMON = "Cinnamon"
    SPOTTED = "Spotted"
    AGOUTI = "Agouti"
    BROWN = "Brown"


class OtherColor(str, Enum):
    GREY = "Grey"
    CREAM = "Cream"
    BROWN = "Brown"
    BLACK = "Black"
    WHITE = "White"
    TAN = "Tan"
    MULTI = "Multi"


class AddressType(str, Enum):
    home = "home"
    facility = "facility"
    em = "emergency"


class PollType(int, Enum):
    notification = 1  # if its a reminder or oother kind of notification
    call = 2
    chat = 3  # if its a chat notification
