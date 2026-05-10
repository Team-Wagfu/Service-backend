"""
define valid mappings for Animal->Breed->Color
"""

from models.enums import Animals

SPECIES_BREED_COLOR_MAP = {
    Animals.DOG: {
        "Indian Pariah Dog (Indie)": [
            "Brown",
            "Black",
            "White",
            "Mixed",
            "Fawn",
        ],
        "Rajapalayam": [
            "Milky White",
            "Pale Pinkish",
            "Light Brown",
            "Golden",
        ],
        "Mudhol Hound": [
            "Fawn",
            "Cream",
            "Brindle",
            "Black & Tan",
            "White",
        ],
        "Indian Spitz": [
            "Pure White",
            "Dusky Brown",
            "Light Fawn",
            "Black",
        ],
        "Himalayan Sheepdog": ["Black and Tan", "Solid Black", "White Markings"],
        "Kombai": ["Reddish-Brown", "Black Muzzle"],
        "Labrador Retriever": ["Black", "Yellow", "Chocolate"],
        "Golden Retriever": ["Various shades of Gold", "Cream"],
        "German Shepherd": [
            "Black and Tan",
            "Black and Red",
            "Sable",
            "Solid Black",
        ],
        "Beagle": [
            "Tricolour (White, Brown, Black)",
            "Lemon",
            "White & Tan",
        ],
        "Pug": ["Fawn", "Black"],
        "Rottweiler": ["Black and Tan", "Black and Mahogany"],
        "Shih Tzu": ["Gold", "White", "Black", "Brown", "Combinations"],
        "Doberman Pinscher": [
            "Black & Tan",
            "Red & Rust",
            "Blue",
            "Fawn",
        ],
        "Boxer": ["Fawn", "Brindle", "White"],
        "Cocker Spaniel": ["Golden", "Black", "Liver", "Parti-colored"],
        "Belgian Malinois": ["Fawn to Mahogany with Black Mask"],
        "Great Dane": ["Fawn", "Black", "Blue", "Brindle", "Harlequin"],
        "Saint Bernard": ["White with Brown", "Reddish-Brown", "Brindle"],
        "Dachshund": ["Red", "Black & Tan", "Chocolate", "Cream", "Dapple"],
    },
    Animals.CAT: {
        "Indian Billi (Desi Cat)": [
            "Brown",
            "Black",
            "Grey",
            "White",
            "Mixed Tabby",
        ],
        "Persian Cat": [
            "White",
            "Black",
            "Grey",
            "Blue",
            "Cream",
            "Calico",
        ],
        "Siamese Cat": [
            "Seal Point",
            "Chocolate Point",
            "Blue Point",
            "Lilac Point",
        ],
        "Himalayan Cat": [
            "Chocolate Point",
            "Lilac Point",
            "Seal Point",
            "Blue Point",
        ],
        "Bengal Cat": ["Spotted", "Marbled", "Brown Tabby", "Snow"],
        "Bombay Cat": ["Solid Jet Black"],
        "Maine Coon": [
            "Brown Tabby",
            "White",
            "Black",
            "Red",
            "Mixed",
        ],
        "Ragdoll": [
            "Seal",
            "Blue",
            "Chocolate",
            "Lilac",
            "Pointed Patterns",
        ],
        "British Shorthair": ["Blue", "Cream", "White", "Black"],
        "Exotic Shorthair": ["Various Persian-style colors"],
        "Sphynx Cat": ["Pink", "Grey", "Patterned Skin"],
        "Scottish Fold": ["Blue", "White", "Black", "Tabby"],
        "Russian Blue": ["Solid Blue-Grey with Silver Tipping"],
        "Birman": ["Seal Point", "Blue Point", "White Paws"],
    },
    Animals.BRD: {
        "Budgerigar (Budgie)": ["Green", "Yellow", "Blue", "White", "Mixed"],
        "Lovebird": ["Green", "White", "Yellow", "Blue"],
        "Rose-ringed Parakeet": ["Green", "Blue", "Yellow"],
        "Cockatiel": ["Grey", "White", "Yellow", "Cinnamon"],
    },
    # Note: Specific source details for Fish, Reptiles, and Rabbits are limited compared to Dogs/Cats
    Animals.FISH: {
        "Betta": ["Red", "Blue", "Purple", "White"],
        "Goldfish": ["Orange", "Red", "White", "Calico"],
    },
    Animals.RBT: {
        # Sorted and marked based on primary usage in South Asia
        "Angora (British/Russian/French) [Wool]": ["Pure White"],  # [4], [3]
        "Angora (German) [Wool]": ["Pure White"],  # [5]
        "Californian [Meat/Fur]": [
            "White with Black Points",
            "White with Brown Points",
        ],  # [4], [6]
        "Grey Giant [Meat/Fur]": ["Solid Grey"],  # [2], [7]
        "Himalayan [Meat/Fur/Pet]": ["White with Black Extremities"],  # [8], [9]
        "Indian Crossbreds [Local Type]": [
            "Non-uniform",
            "Grey",
            "Spotted",
            "White",
        ],  # [10], [11]
        "New Zealand White [Meat/Fur]": ["Albino White (Red Eyes)"],  # [2], [12]
        "Soviet Chinchilla [Meat/Fur]": ["Blue-Grey with White Belly"],  # [6]
        "White Giant [Meat/Fur]": ["Pure White (Red Eyes)"],  # [1], [13]
    },
    Animals.OTH: {
        "Hamster": ["Golden", "White", "Grey"],
        "Guinea Pig": ["White", "Black", "Brown", "Tri-color"],
    },
}
