import random

# Thesaurus avec genre
words = {
    "salutation": {
        "m": ("Cher", "Très cher"),
        "f": ("Chère", "Très chère"),
    },
    "qualifier": {
        "m": ("tendre", "adoré", "bien-aimé"),
        "f": ("tendre", "adorée", "bien-aimée"),
    },

    "adjectives": {
        "m": (
            "ardent", "tendre", "exquis",
            "fervent", "éternel"
        ),
        "f": (
            "ardente", "tendre", "exquise",
            "fervente", "éternelle"
        ),
    },

    "nouns": {
        "m": (
            "cœur", "esprit", "désir", "souvenir"
        ),
        "f": (
            "âme", "présence", "pensée"
        ),
    },

    "verbs": (
        "admire", "caresse",
        "poursuit", "convoque", "implore"
    ),

    "adverbs": (
        "passionnément", "intensément",
        "fiévreusement", "profondément"
    ),

    "closing": (
        "À toi dévotement,",
        "Tendrement à toi,",
        "Éternellement tien(ne),"
    )
}


def pick(category, gender=None):
    if isinstance(words[category], dict):
        return random.choice(words[category][gender])
    return random.choice(words[category])


def sentence_a(g):
    return (
        f"Mon {pick('adjectives', g)} {pick('nouns', g)} "
        f"{pick('verbs')} {pick('adverbs')} "
        f"ton {pick('adjectives', g)} {pick('nouns', g)}."
    )


def sentence_b(g):
    return (
        f"Ta {pick('adjectives', g)} {pick('nouns', g)} "
        f"{pick('verbs')} {pick('adverbs')} "
        f"ma {pick('adjectives', g)} {pick('nouns', g)}."
    )


def love_letter():
    gender = random.choice(("m", "f"))

    print(
        f"{pick('salutation', gender)} "
        f"{pick('qualifier', gender)},\n"
    )

    for _ in range(5):
        if random.random() < 0.5:
            print(sentence_a(gender))
        else:
            print(sentence_b(gender))

    print("\n" + pick("closing"))


if __name__ == "__main__":
    love_letter()
