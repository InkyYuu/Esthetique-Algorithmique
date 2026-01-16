from game import Node, Character, Scene

characters = {
    "Phoenix": Character(name="Phoenix Wright", sprites={"neutral":"phoenix/neutral.gif","thinking":"phoenix/thinking.gif","nervous":"phoenix/nervous.gif","surprised":"phoenix/surprised.gif"}),
    
    "Mia": Character(name="Mia Fey", age=27, description="Avocate en chef du cabinet Fey & Co. Ma patronne est un très bon avocat de la défense.", photo="mia/profile.gif",
                     sprites={"grinning":"mia/grinning.gif","normal":"mia/normal.gif","normal-talking":"mia/normal-talking.gif", "smiling":"mia/smiling.gif", 
                      "smiling-talking":"mia/smiling-talking.gif", "surprised":"mia/surprised.gif", "surprised-talking":"mia/surprised-talking.gif"}),

    "Paul": Character(name="Paul Defès", age=23, description="L'accusé dans cette affaire. Un type sympathique et mon ami depuis l'école primaire.", photo="paul/profile.gif",
                      sprites={"angry":"paul/angry.gif","confident":"paul/confident.gif","confident-talking":"paul/confident-talking.gif","crying":"paul/crying.gif", "crying-talking":"paul/crying-talking.gif",
                       "happy":"paul/happy.gif","happy-talking":"paul/happy-talking.gif","normal":"paul/normal.gif","normal-talking":"paul/normal-talking.gif", "scared":"paul/scared.gif","scared-talking":"paul/scared-talking.gif",
                       "scratching-head":"paul/scratching-head.gif", "scratching-head-talking":"paul/scratching-head-talking.gif","thinking":"paul/thinking.gif", "thinking-talking":"paul/thinking-talking.gif", "thumbs-up":"paul/thumbs-up.gif",
                         "thumbs-up-talking":"paul/thumbs-up-talking.gif"}),

    "Judge": Character(name="Juge", sprites={"neutral":"judge/neutral.gif"}),

    "Cindy": Character(name="Cindy Stone", age=22, description="La victime dans cette affaire. Mannequin, elle vivait seule dans son appartement.", photo="cindy/profile.gif",
                       sprites={"neutral":"cindy/neutral.gif","smile":"cindy/smile.gif","sad":"cindy/sad.gif"}),

    "Victor": Character(name="Victor Boulay", age=52, description="Représentant de l'accusation. Manque de charisme. Souvent incapable d'imposer son point de vue.", photo="victor/profile.gif",
                       sprites={"neutral":"victor/neutral.gif","smug":"victor/smug.gif"}),

    "Frank": Character(name="Frank Khavu", age=45, description="Témoin (vendeur de journaux).", photo="frank/profile.gif",
                       sprites={"neutral":"frank/neutral.gif","sweat":"frank/sweat.gif","panic":"frank/panic.gif"}),

    "???": Character(name="???", photo="unknown/profile.gif"),

    "Horloge": Character(name="Horloge", photo="objects/clock.gif"),
}

WAITING_ROOM_BG = "backgrounds/waiting-room.jpg"

nodes = [
  Node(
    id="q1_date",
    type="dialogue",
    scene=Scene(
      textType="date",
      text="August 3, 9:47 AM\n District Court\nDefendant Lobby No. 2",
    ),
    nextId="q1_1",
  ),  
  Node(
    id="q1_1",
    type="dialogue",
    scene=Scene(
      background=WAITING_ROOM_BG,
      characterText="Phoenix",
      textType="thought",
      text="(Boy am I nervous!)",
    ),
    nextId="q1_2",
  ),
  Node(
    id="q1_2",
    type="dialogue",
    scene=Scene(
      background=WAITING_ROOM_BG,
      characterText="Mia",
      textType="dialogue",
      text="Wright!",
    ),
    nextId="q1_3",
  ),
  Node(
    id="q1_3",
    type="dialogue",
    scene=Scene(
      background=WAITING_ROOM_BG,
      character=characters["Mia"],
      characterEmotion="smile",
      smoothEntry=True,
      characterText="Phoenix",
      textType="thought",
      text="Oh, h-hiya, Chief.",
    ),
    nextId="q1_4",  
  ), 
  Node(
    id="q1_4",
    type="dialogue",
    scene=Scene(
      background=WAITING_ROOM_BG,
      character=characters["Mia"],
      characterEmotion="smiling-talking",
      smoothEntry=False,
      characterText="Mia",
      textType="dialogue",
      text="Whew, I'm glad I made it on time.",
    ),
    nextId="q1_5",  
  ),
  Node(
    id="q1_5",
    type="dialogue",
    scene=Scene(
      background=WAITING_ROOM_BG,
      character=characters["Mia"],
      characterEmotion="grinning-talking",
      smoothEntry=False,
      characterText="Mia",
      textType="thought",
      text="Well, I have to say Phoenix, I'm impressed!",
    ),
    nextId="q1_6",
  ),
  Node(
    id="q1_6",
    type="dialogue",
    scene=Scene(
      background=WAITING_ROOM_BG,
      character=characters["Mia"],
      characterEmotion="surprised",
      smoothEntry=False,
      characterText="???",
      textType="testimony",
      text="(It's over! My life, everything, it's all over!)",
    ),
    nextId="q1_7",
  ),
  Node(
    id="q1_7",
    type="dialogue",
    scene=Scene(
      background=WAITING_ROOM_BG,
      character=characters["Mia"],
      characterEmotion="surprised-talking",
      smoothEntry=False,
      characterText="Mia",
      textType="dialogue",
      text="... Is that your client screaming over there?",
    ),
    nextId="q1_8",
  ),
  Node(
    id="q1_8",
    type="dialogue",
    scene=Scene(
      background=WAITING_ROOM_BG,
      character=characters["Paul"],
      characterEmotion="crying-talking",
      smoothEntry=False,
      characterText="Paul",
      textType="dialogue",
      text="Nick!!!",
    ),
    nextId="q1_9",
  ),
]

import os
print("CWD =", os.getcwd())
print("Exists assets/backgrounds/waiting-room.jpg ?",
      os.path.exists("assets/backgrounds/waiting-room.jpg"))
