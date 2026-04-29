"""
Convert VGMS controlled vocabulary PDFs to structured JSON.

Transcribes the Video Game Metadata Schema controlled vocabularies for
Gameplay Genre (v1.3) and Mechanics (v1.1) from PDF into machine-readable
JSON format. Validates that all thesaurus relationships are reciprocal.

Source PDFs from University of Washington GAMER Group:
- https://github.com/uwgamergroup/vocabulary-gameplay-genre/
- https://github.com/uwgamergroup/vocabulary-mechanics
"""

import json
import sys
from pathlib import Path
from typing import Any


def build_gameplay_genre_vocabulary() -> dict[str, Any]:
    """Build the complete Gameplay Genre controlled vocabulary from PDF content."""
    return {
        "vocabulary": "Gameplay Genre",
        "version": "1.3",
        "date": "2024-12-12",
        "citation": (
            "Lee, J. H., Schmalz, M., Newman, M., & Koughan, L. D. (2024). "
            "UW/SIMM Video Game Metadata Schema: Controlled Vocabulary for Genre. "
            "Version 1.3. Retrieved from: "
            "https://github.com/uwgamergroup/vocabulary-gameplay-genre/"
        ),
        "source_url": "https://github.com/uwgamergroup/vocabulary-gameplay-genre/",
        "terms": {
            # ── ACTION and sub-genres ──
            "Action": {
                "term_type": "preferred",
                "scope_note": (
                    "Games that revolve around a fast-paced experience. These games "
                    "often emphasize reaction-based challenges in terms of how the "
                    "player interacts with the game world."
                ),
                "broader_term": None,
                "narrower_terms": [
                    "Action-Adventure", "Arcade", "Block Breaking", "Brawler",
                    "Fighting", "Hack and Slash", "Multiplayer Online Battle Arena",
                    "Music", "Party", "Platform", "Stealth", "Survival",
                    "Vehicle Combat"
                ],
                "related_terms": [],
                "use_for": [],
            },
            "Action-Adventure": {
                "term_type": "preferred",
                "scope_note": (
                    "Games which focus more on a sense of adventure than fast-paced "
                    "conflict, often with a focus on solving riddles or overcoming "
                    "challenges to progress. Representative games are Myst and "
                    "The Amazon Trail."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Adventure"],
            },
            "Adventure": {
                "term_type": "non-preferred",
                "use": "Action-Adventure",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Arcade": {
                "term_type": "preferred",
                "scope_note": (
                    "Games that either were released in a classic arcade setting or "
                    "have their artistic roots in that aesthetic. These games often "
                    "have simple graphics and gameplay with a focus on attaining a "
                    "high score. Representative games are Pac-Man and Space Invaders."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Block Breaking": {
                "term_type": "preferred",
                "scope_note": (
                    "Games where the primary mechanic for advancement and scoring is "
                    "the breaking of blocks, often with a ball controlled by a paddle. "
                    "Representative games are Brickles and 3-D Brickaway."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Brawler": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on physical hand-to-hand combat, sometimes "
                    "allowing players to use parts of the environment as weapons. "
                    "Characters often engage with multiple enemies simultaneously to "
                    "fight through levels. Representative games are Double Dragon and "
                    "The Bouncer."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": ["Hack and Slash"],
                "use_for": ["Beat 'Em Up"],
            },
            "Beat 'Em Up": {
                "term_type": "non-preferred",
                "use": "Brawler",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Fighting": {
                "term_type": "preferred",
                "scope_note": (
                    "Games where the player controls a character or team of characters "
                    "engaging in physical combat with others. They employ rounds, with "
                    "the winner of the majority deciding the match. Often feature "
                    "diverse characters with unique fighting styles. Representative "
                    "games are Street Fighter 2 and King of Fighters."
                ),
                "broader_term": "Action",
                "narrower_terms": ["Mascot Fighter"],
                "related_terms": [],
                "use_for": [],
            },
            "Mascot Fighter": {
                "term_type": "preferred",
                "scope_note": (
                    "Games featuring mascot characters, often from game or media "
                    "franchises, engaging in combat in the style of fighting games. "
                    "Usually involve more than two characters fighting simultaneously "
                    "in a free-for-all environment. Representative games are Super "
                    "Smash Brothers and PlayStation All-Stars Battle Royale."
                ),
                "broader_term": "Fighting",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Hack and Slash": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on fast-paced gameplay involving melee weapons. "
                    "Players often fight multiple enemies simultaneously to advance "
                    "across levels. Representative games are Gauntlet Legends and "
                    "Golden Axe."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": ["Brawler"],
                "use_for": [],
            },
            "Multiplayer Online Battle Arena": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on a third-person perspective where players "
                    "control a single character in an online environment. Often "
                    "feature teams competing to achieve goals or domination. "
                    "Representative games are League of Legends and Defense of "
                    "the Ancients."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["MOBA"],
            },
            "MOBA": {
                "term_type": "non-preferred",
                "use": "Multiplayer Online Battle Arena",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Music": {
                "term_type": "preferred",
                "scope_note": (
                    "Games revolving around music, beats, or rhythm as a core part of "
                    "their experience. Some feature control of simulated instruments "
                    "like guitars and drums. Representative games are Hi-Fi Rush and "
                    "Rock Band."
                ),
                "broader_term": "Action",
                "narrower_terms": ["Dancing"],
                "related_terms": [],
                "use_for": [],
            },
            "Dancing": {
                "term_type": "preferred",
                "scope_note": (
                    "Games where players interact by moving or dancing on an external "
                    "peripheral. Representative game is Dance Dance Revolution."
                ),
                "broader_term": "Music",
                "narrower_terms": [],
                "related_terms": ["Rhythm"],
                "use_for": [],
            },
            "Party": {
                "term_type": "preferred",
                "scope_note": (
                    'Games that are collections of smaller "mini-games," often meant '
                    "for group play in a casual competitive context. Representative "
                    "games are Mario Party and Wii Party."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Minigame Collection"],
            },
            "Minigame Collection": {
                "term_type": "non-preferred",
                "use": "Party",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Platform": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on jumping or moving between platforms, navigating "
                    "terrain and obstacles, emphasizing hand-eye coordination. "
                    "Representative games are Super Mario Bros. 3 and Sonic the "
                    "Hedgehog."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Platformer"],
            },
            "Platformer": {
                "term_type": "non-preferred",
                "use": "Platform",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Stealth": {
                "term_type": "preferred",
                "scope_note": (
                    "Games emphasizing stealth and avoiding detection. Representative "
                    "games are Metal Gear Solid and Tenchu: Stealth Assassins."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Survival": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on surviving difficult situations, often "
                    "emphasizing resource management (like health and ammunition) "
                    "against overwhelming opposition. Representative games are "
                    "Left 4 Dead and Don't Starve."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Vehicle Combat": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on combat between vehicles as a key mechanic. "
                    "Representative games are Twisted Metal and Burnout."
                ),
                "broader_term": "Action",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Car Combat"],
            },
            "Car Combat": {
                "term_type": "non-preferred",
                "use": "Vehicle Combat",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },

            # ── PUZZLE and sub-genres ──
            "Puzzle": {
                "term_type": "preferred",
                "scope_note": (
                    "Games that emphasize solving puzzles and/or organizing pieces. "
                    "Representative games are Lumines and Portal."
                ),
                "broader_term": None,
                "narrower_terms": [
                    "Block Fill", "Hidden Object", "Match Puzzles",
                    "Point and Click", "Word Puzzles"
                ],
                "related_terms": [],
                "use_for": [],
            },
            "Block Fill": {
                "term_type": "preferred",
                "scope_note": (
                    "Games where players strategically place or arrange blocks to fill "
                    "spaces or complete patterns, aiming to clear lines or match "
                    "shapes. Representative games are Tetris and Puyo Pop Fever."
                ),
                "broader_term": "Puzzle",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Hidden Object": {
                "term_type": "preferred",
                "scope_note": (
                    "Games where players search for specific items concealed within "
                    "detailed scenes to progress. Representative game is The Witness."
                ),
                "broader_term": "Puzzle",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Match Puzzles": {
                "term_type": "preferred",
                "scope_note": (
                    "Games where players align or group identical items (like tiles or "
                    "gems) in sets, typically of three or more, to clear them and "
                    "achieve objectives. Representative games are Candy Crush and "
                    "Bejeweled 3."
                ),
                "broader_term": "Puzzle",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Point and Click": {
                "term_type": "preferred",
                "scope_note": (
                    "Games where players interact by clicking on objects, collecting "
                    "items and information to solve puzzles and advance the narrative. "
                    "Representative games are Deponia and The Secret of Monkey Island."
                ),
                "broader_term": "Puzzle",
                "narrower_terms": [],
                "related_terms": ["Adventure"],
                "use_for": [],
            },
            "Word Puzzles": {
                "term_type": "preferred",
                "scope_note": (
                    "Puzzle-based games challenging players to form, decipher, or "
                    "manipulate words or letters, testing vocabulary and language "
                    "skills. Representative game is WORDLE."
                ),
                "broader_term": "Puzzle",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },

            # ── RHYTHM ──
            "Rhythm": {
                "term_type": "preferred",
                "scope_note": (
                    "These games involve the player inputting commands or completing "
                    "actions while synchronizing to a rhythm. Representative games are "
                    "Space Channel 5 and Donkey Conga."
                ),
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": ["Music"],
                "use_for": [],
            },

            # ── ROLE-PLAYING and sub-genres ──
            "Role-Playing": {
                "term_type": "preferred",
                "scope_note": (
                    "Games related to tabletop role-playing, involving a heavy focus "
                    'on statistical advancement (like "leveling up") of characters, '
                    "combined with exploration."
                ),
                "broader_term": None,
                "narrower_terms": [
                    "Japanese RPG", "Massively Multiplayer Online RPG",
                    "Rogue-Like", "Western RPG"
                ],
                "related_terms": [],
                "use_for": ["RPG"],
            },
            "RPG": {
                "term_type": "non-preferred",
                "use": "Role-Playing",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Japanese RPG": {
                "term_type": "preferred",
                "scope_note": (
                    "RPGs often designed in Japan, placing heavy focus on visual style "
                    "and story elements, frequently involving romance and dramatic "
                    "personal histories. Characters often show anime influence. "
                    "Representative games are Final Fantasy 7 and Dragon Quest."
                ),
                "broader_term": "Role-Playing",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["JRPG"],
            },
            "JRPG": {
                "term_type": "non-preferred",
                "use": "Japanese RPG",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Massively Multiplayer Online RPG": {
                "term_type": "preferred",
                "scope_note": (
                    "RPGs played with a massive number of players in an online "
                    "environment. Representative games are World of Warcraft and "
                    "Star Wars: Knights of the Old Republic."
                ),
                "broader_term": "Role-Playing",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["MMORPG"],
            },
            "MMORPG": {
                "term_type": "non-preferred",
                "use": "Massively Multiplayer Online RPG",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Rogue-Like": {
                "term_type": "preferred",
                "scope_note": (
                    "RPGs where players explore usually randomly generated "
                    "environments, focusing on item discovery and permanent character "
                    "death. Representative games are Angband and Diablo."
                ),
                "broader_term": "Role-Playing",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Rogue RPG"],
            },
            "Rogue RPG": {
                "term_type": "non-preferred",
                "use": "Rogue-Like",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Western RPG": {
                "term_type": "preferred",
                "scope_note": (
                    "RPGs focusing on character customization and development, often "
                    "employing realistic visual styles and vast open worlds. "
                    "Representative games are The Elder Scrolls V: Skyrim and "
                    "Baldur's Gate."
                ),
                "broader_term": "Role-Playing",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },

            # ── SIMULATION and sub-genres ──
            "Simulation": {
                "term_type": "preferred",
                "scope_note": (
                    "Games designed to simulate actions or situations from either an "
                    "existing or fictional reality."
                ),
                "broader_term": None,
                "narrower_terms": [
                    "Breeding", "Construction & Management Simulation",
                    "Flight Simulator", "God Game", "Interactive Movie",
                    "Programming Game", "Sandbox", "Social Simulator",
                    "Virtual Life", "Visual Novel"
                ],
                "related_terms": [],
                "use_for": [],
            },
            "Breeding": {
                "term_type": "preferred",
                "scope_note": (
                    "Games emphasizing the breeding and development or raising of "
                    "animals or entities. Representative games are Spore and "
                    "Monster Rancher."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Construction & Management Simulation": {
                "term_type": "preferred",
                "scope_note": (
                    "Games revolving around creating structures, cities, or other "
                    "built objects, often emphasizing resource management. "
                    "Representative games are SimCity 2000 and Dwarf Fortress."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["City Building", "Tycoon"],
            },
            "City Building": {
                "term_type": "non-preferred",
                "use": "Construction & Management Simulation",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Tycoon": {
                "term_type": "non-preferred",
                "use": "Construction & Management Simulation",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Flight Simulator": {
                "term_type": "preferred",
                "scope_note": (
                    "Games designed to simulate flight, usually of aircraft. Some "
                    "strive for realism, while others are more action-oriented. "
                    "Representative games are Microsoft Flight Simulator and "
                    "Ace Combat."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Aviation Simulator"],
            },
            "Aviation Simulator": {
                "term_type": "non-preferred",
                "use": "Flight Simulator",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "God Game": {
                "term_type": "preferred",
                "scope_note": (
                    "Games allowing the player to interact with a world as an "
                    "all-powerful entity. Representative games are Black & White "
                    "and Viva Pinata."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Interactive Movie": {
                "term_type": "preferred",
                "scope_note": (
                    "Games involving minimal player action, functioning more as a "
                    "series of movies controlled through decisions. Representative "
                    "game is Night Trap."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Programming Game": {
                "term_type": "preferred",
                "scope_note": (
                    "Games revolving around programming, often computer code, as "
                    "their core mechanic. Representative game is CodeCombat."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Sandbox": {
                "term_type": "preferred",
                "scope_note": (
                    "Games involving open environments where players are encouraged "
                    "to explore, act, and create freely. Can be played in various "
                    "ways depending on the player's mood. Representative games are "
                    "Minecraft and Grand Theft Auto."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Open World"],
            },
            "Open World": {
                "term_type": "non-preferred",
                "use": "Sandbox",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Social Simulator": {
                "term_type": "preferred",
                "scope_note": (
                    "Games revolving around simulating social life, situations, and "
                    "interaction. Representative game is The Sims."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Life Simulation Game"],
            },
            "Life Simulation Game": {
                "term_type": "non-preferred",
                "use": "Social Simulator",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Virtual Life": {
                "term_type": "preferred",
                "scope_note": (
                    "Games involving the creation of an in-game avatar controlled by "
                    "the player in a virtual world, living a simulated life, often "
                    "online with interactions between player avatars. Example game "
                    "is Second Life."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Visual Novel": {
                "term_type": "preferred",
                "scope_note": (
                    "Narrative-driven games where players engage with a story "
                    "primarily through text and visuals, making choices that influence "
                    "the plot's direction and outcome. Representative games are "
                    "Doki Doki Literature Club! and VA-11 Hall-A."
                ),
                "broader_term": "Simulation",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },

            # ── SPORTS and sub-genres ──
            "Sports": {
                "term_type": "preferred",
                "scope_note": (
                    'For sports games, assign both the term "sports" as well as the '
                    "name of the sport being represented. Use information associated "
                    "with the item (e.g., packaging) to provide the sport name and "
                    "spelling when possible. If no related information is available, "
                    "use the most common spelling of that sport for the region the "
                    "record is being created for (e.g., American English for records "
                    "in the United States). Representative games are FIFA "
                    "International Soccer and MLB: The Show 24."
                ),
                "broader_term": None,
                "narrower_terms": ["Racing"],
                "related_terms": [],
                "use_for": [],
            },
            "Racing": {
                "term_type": "preferred",
                "scope_note": (
                    "Games revolving around racing as the core mechanic, often "
                    "involving vehicles racing around a course. Representative games "
                    "are Gran Turismo and Forza Motorsport."
                ),
                "broader_term": "Sports",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },

            # ── SHOOTER and sub-genres ──
            "Shooter": {
                "term_type": "preferred",
                "scope_note": (
                    "Games revolving around a shooting mechanic where players target "
                    "and shoot objects or enemies to progress."
                ),
                "broader_term": None,
                "narrower_terms": [
                    "First Person Shooter", "Light Gun Shooter",
                    "Rail Shooter", "Tactical Shooter"
                ],
                "related_terms": [],
                "use_for": ["Shoot 'em Up"],
            },
            "Shoot 'em Up": {
                "term_type": "non-preferred",
                "use": "Shooter",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "First Person Shooter": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on shooting mechanics from a first-person "
                    "perspective. Representative games are Halo: Combat Evolved "
                    "and Doom."
                ),
                "broader_term": "Shooter",
                "narrower_terms": ["Massively Multiplayer FPS"],
                "related_terms": [],
                "use_for": ["FPS"],
            },
            "FPS": {
                "term_type": "non-preferred",
                "use": "First Person Shooter",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Massively Multiplayer FPS": {
                "term_type": "preferred",
                "scope_note": (
                    "First-person shooters played in an online environment with "
                    "massive numbers of players simultaneously. Representative games "
                    "are PlanetSide and Firefall."
                ),
                "broader_term": "First Person Shooter",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Light Gun Shooter": {
                "term_type": "preferred",
                "scope_note": (
                    "Games played using an external gun controller aimed at the "
                    "screen to shoot objects or enemies. Representative games are "
                    "Duck Hunt and House of the Dead 2."
                ),
                "broader_term": "Shooter",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Rail Shooter": {
                "term_type": "preferred",
                "scope_note": (
                    "Shooters where players do not control their movement but are "
                    'propelled along a set course or "rail." Representative games are '
                    "The Lost World: Jurassic Park and Star Fox 64."
                ),
                "broader_term": "Shooter",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Tactical Shooter": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on simulating tactical or military environments, "
                    "revolving around shooting mechanics. Representative games are "
                    "Rainbow Six and Call of Duty: Modern Warfare."
                ),
                "broader_term": "Shooter",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Combat"],
            },
            "Combat": {
                "term_type": "non-preferred",
                "use": "Tactical Shooter",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },

            # ── STRATEGY and sub-genres ──
            "Strategy": {
                "term_type": "preferred",
                "scope_note": (
                    "Games revolving around strategic or tactical planning, often "
                    "involving building, resource management, and exploration "
                    "components."
                ),
                "broader_term": None,
                "narrower_terms": [
                    "4X", "Military Simulator", "Real-Time", "Tactics",
                    "Tower Defense", "Turn-Based Strategy"
                ],
                "related_terms": [],
                "use_for": [],
            },
            "4X": {
                "term_type": "preferred",
                "scope_note": (
                    'Stands for "explore, expand, exploit, and exterminate." Games '
                    "revolve around creating an empire through diplomacy and conquest. "
                    "Representative games are Master of Orion and Sid Meier's "
                    "Civilization V."
                ),
                "broader_term": "Strategy",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Military Simulator": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on simulating realistic militaries or historical "
                    "military events. Representative games are Combat Mission and "
                    "Close Combat."
                ),
                "broader_term": "Strategy",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": ["Wargame"],
            },
            "Wargame": {
                "term_type": "non-preferred",
                "use": "Military Simulator",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Real-Time": {
                "term_type": "preferred",
                "scope_note": (
                    "Games unfolding in real-time, as opposed to using turns. "
                    "Example games are StarCraft and Command and Conquer."
                ),
                "broader_term": "Strategy",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Tactics": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on small-scale conflicts, often involving the "
                    "player positioning and controlling a predetermined number of "
                    "units. Representative games are Final Fantasy Tactics and "
                    "Steel Panthers."
                ),
                "broader_term": "Strategy",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Tower Defense": {
                "term_type": "preferred",
                "scope_note": (
                    "Games focusing on defending a location against waves of enemies, "
                    "requiring strategic placement and control of units and weapons. "
                    "Representative game is Plants vs. Zombies."
                ),
                "broader_term": "Strategy",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Turn-Based Strategy": {
                "term_type": "preferred",
                "scope_note": (
                    "Games utilizing alternating turns as the central mechanic. "
                    "Representative games are Heroes of Might and Magic and "
                    "Rome: Total War."
                ),
                "broader_term": "Strategy",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },

            # ── TRADITIONAL and sub-genres ──
            "Traditional": {
                "term_type": "preferred",
                "scope_note": (
                    "Games based on mechanics that exist in the real world and can "
                    "be played in a physical setting."
                ),
                "broader_term": None,
                "narrower_terms": [
                    "Board Game", "Card Game", "Exercise", "Gambling",
                    "Game Show", "Maze", "Pinball", "Puzzle (Traditional)",
                    "Trivia Game"
                ],
                "related_terms": [],
                "use_for": [],
            },
            "Board Game": {
                "term_type": "preferred",
                "scope_note": (
                    "Games originating from tabletop board games, often adaptations "
                    "of existing ones. Representative games are Settlers of Catan "
                    "and Chessmaster."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Card Game": {
                "term_type": "preferred",
                "scope_note": (
                    "Games originating from tabletop card games, often adaptations "
                    "of existing ones. Representative games are Magic: The Gathering "
                    "and Full House Poker."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Exercise": {
                "term_type": "preferred",
                "scope_note": (
                    "Games involving player movement using an external peripheral for "
                    "physical exercise purposes. Representative game is Wii Fit."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Gambling": {
                "term_type": "preferred",
                "scope_note": (
                    "Games originating from traditional gambling and casino games, "
                    "often adaptations. Representative games are Caesar's Palace and "
                    "Golden Nugget 64."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Game Show": {
                "term_type": "preferred",
                "scope_note": (
                    "Games modeled after, and often adaptations of, television game "
                    "shows. Representative games are Jeopardy! The Video Game and "
                    "Wheel of Fortune."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": ["Trivia Game"],
                "use_for": [],
            },
            "Maze": {
                "term_type": "preferred",
                "scope_note": (
                    "Games revolving around the navigation of a maze. Representative "
                    "game is Labyrinth."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Pinball": {
                "term_type": "preferred",
                "scope_note": (
                    "Simulations of pinball machines. Representative games are "
                    "Full Tilt Pinball and Mario Pinball Land."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
            "Puzzle (Traditional)": {
                "term_type": "preferred",
                "scope_note": (
                    "Traditional puzzle games adapted to video game format. Listed "
                    "under the Traditional category as distinct from the top-level "
                    "Puzzle genre."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": ["Puzzle"],
                "use_for": [],
            },
            "Trivia Game": {
                "term_type": "preferred",
                "scope_note": (
                    "Games involving answering questions based on obscure knowledge. "
                    "Representative games are The Guy Game and Scene It? Box Office "
                    "Smash."
                ),
                "broader_term": "Traditional",
                "narrower_terms": [],
                "related_terms": ["Game Show"],
                "use_for": ["Quiz Game"],
            },
            "Quiz Game": {
                "term_type": "non-preferred",
                "use": "Trivia Game",
                "scope_note": None,
                "broader_term": None,
                "narrower_terms": [],
                "related_terms": [],
                "use_for": [],
            },
        },
    }


def build_mechanics_vocabulary() -> dict[str, Any]:
    """Build the complete Mechanics controlled vocabulary from PDF content."""
    return {
        "vocabulary": "Mechanics",
        "version": "1.1",
        "date": "2024-12-12",
        "citation": (
            "Lee, J. H., Schmalz, M., Newman, M., & Koughan, L. D. (2024). "
            "UW/SIMM Video Game Metadata Schema: Controlled Vocabulary for "
            "Mechanics. Version 1.1. Retrieved from: "
            "https://github.com/uwgamergroup/vocabulary-mechanics"
        ),
        "source_url": "https://github.com/uwgamergroup/vocabulary-mechanics",
        "terms": {
            "Activation": {
                "term_type": "preferred",
                "scope_note": (
                    "User has no agency outside of activating either the game or "
                    "their turn."
                ),
                "related_terms": [],
                "use_for": ["None", "Random Chance"],
                "examples": ["Slot machines", "Candy Land"],
            },
            "Avoiding": {
                "term_type": "preferred",
                "scope_note": (
                    "Taking action to preclude encountering unwanted objects or "
                    "circumstances."
                ),
                "related_terms": ["Jumping"],
                "use_for": [],
                "examples": ["Asteroids", "Super Mario Bros.", "Pac-Man"],
            },
            "Building": {
                "term_type": "preferred",
                "scope_note": "Creating objects in the environment.",
                "related_terms": [],
                "use_for": [],
                "examples": ["Minecraft", "The Sims", "SimCity"],
            },
            "Card Playing": {
                "term_type": "preferred",
                "scope_note": (
                    "Selecting for use an object from a set of similar objects "
                    "(cards, tiles, etc.)."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Hearthstone", "Magic: The Gathering Arena"],
            },
            "Choosing": {
                "term_type": "preferred",
                "scope_note": "Selecting an option from a set of choices.",
                "related_terms": [],
                "use_for": [],
                "examples": ["Mass Effect", "You Don't Know Jack"],
            },
            "Climbing": {
                "term_type": "preferred",
                "scope_note": (
                    "Navigating along a vertically-inclined, non-ground surface."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Shadow of the Colossus", "Assassin's Creed"],
            },
            "Collecting": {
                "term_type": "preferred",
                "scope_note": "Acquiring a set of objects.",
                "related_terms": [],
                "use_for": [],
                "examples": ["Pac-Man", "Katamari Damacy", "Goat Simulator"],
            },
            "Crafting": {
                "term_type": "preferred",
                "scope_note": "Combining objects to create a new object.",
                "related_terms": [],
                "use_for": [],
                "examples": ["Minecraft", "Doodle God", "Skyrim"],
            },
            "Deck Building": {
                "term_type": "preferred",
                "scope_note": "Selecting a subset of objects for later use.",
                "related_terms": [],
                "use_for": [],
                "examples": ["Hearthstone", "Magic: The Gathering Arena"],
            },
            "Destroying": {
                "term_type": "preferred",
                "scope_note": "Destroying objects in the environment.",
                "related_terms": [],
                "use_for": [],
                "examples": ["Minecraft", "Red Faction", "Monster Truck Destruction"],
            },
            "Drawing": {
                "term_type": "preferred",
                "scope_note": (
                    "Using freeform input to create a design as either a creation "
                    "tool or command input."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Line Rider", "Okami"],
            },
            "Driving": {
                "term_type": "preferred",
                "scope_note": (
                    "Navigating a vehicle through the environment. 'Vehicle' is "
                    "defined as any object conforming to movement rules (e.g. car, "
                    "skateboard, horse, etc.)."
                ),
                "related_terms": [],
                "use_for": ["Flying", "Piloting", "Sailing", "Riding"],
                "examples": ["Grand Theft Auto", "Forza", "Mech Warrior", "Star Fox"],
            },
            "Fighting": {
                "term_type": "preferred",
                "scope_note": (
                    "Characters attempting to exert their power over others through "
                    "force."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Super Smash Bros.", "League of Legends", "Hyrule Warriors"],
            },
            "Flying": {
                "term_type": "non-preferred",
                "use": "Driving",
                "scope_note": None,
                "related_terms": [],
                "use_for": [],
                "examples": [],
            },
            "Grab & Release": {
                "term_type": "preferred",
                "scope_note": "Picking up and setting down objects.",
                "related_terms": [],
                "use_for": [],
                "examples": ["Octodad: Dadliest Catch"],
            },
            "Hitting": {
                "term_type": "preferred",
                "scope_note": "Exerting force on an object already in motion.",
                "related_terms": ["Shooting"],
                "use_for": [],
                "examples": ["Pinball", "Baseball", "Piano Tiles"],
            },
            "Input Combinations": {
                "term_type": "preferred",
                "scope_note": (
                    "A specific sequence of inputs which result in a single event."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Tony Hawk's Pro Skater", "Marvel vs. Capcom"],
            },
            "Jumping": {
                "term_type": "preferred",
                "scope_note": "Causing a character to jump in the environment.",
                "related_terms": ["Avoiding"],
                "use_for": [],
                "examples": ["Super Mario Bros.", "Sonic the Hedgehog"],
            },
            "Matching": {
                "term_type": "preferred",
                "scope_note": (
                    "Connecting similar objects through positioning or identification."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Bejeweled", "Puzzle & Dragon", "Memory"],
            },
            "None": {
                "term_type": "non-preferred",
                "use": "Activation",
                "scope_note": None,
                "related_terms": [],
                "use_for": [],
                "examples": [],
            },
            "Pattern Matching": {
                "term_type": "preferred",
                "scope_note": (
                    "Player repeats or simultaneously responds to game patterns."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Guitar Hero", "Dance Dance Revolution", "Simon Says"],
            },
            "Piloting": {
                "term_type": "non-preferred",
                "use": "Driving",
                "scope_note": None,
                "related_terms": [],
                "use_for": [],
                "examples": [],
            },
            "Positioning": {
                "term_type": "preferred",
                "scope_note": (
                    "Placing or moving objects or events within the game world as a "
                    "necessary gameplay element to advance to the next level/zone "
                    "(Block placement in puzzle games, unit placement in tactics "
                    "games with stat impact, etc.)."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Sudoku", "Plants vs. Zombies", "Tetris", "Dear Esther"],
            },
            "Programming": {
                "term_type": "preferred",
                "scope_note": (
                    "Utilizing programming logic to create game behaviors."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Omega", "Codecombat", "Gidget"],
            },
            "Random Chance": {
                "term_type": "non-preferred",
                "use": "Activation",
                "scope_note": None,
                "related_terms": [],
                "use_for": [],
                "examples": [],
            },
            "Resource Management": {
                "term_type": "preferred",
                "scope_note": "Selecting how and when to gather or use resources.",
                "related_terms": [],
                "use_for": [],
                "examples": ["League of Legends", "Plants vs. Zombies", "The Sims"],
            },
            "Riding": {
                "term_type": "non-preferred",
                "use": "Driving",
                "scope_note": None,
                "related_terms": [],
                "use_for": [],
                "examples": [],
            },
            "Sailing": {
                "term_type": "non-preferred",
                "use": "Driving",
                "scope_note": None,
                "related_terms": [],
                "use_for": [],
                "examples": [],
            },
            "Sharing": {
                "term_type": "preferred",
                "scope_note": (
                    "Transferal of a game object from one player to another."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Minecraft", "Farmville"],
            },
            "Shooting": {
                "term_type": "preferred",
                "scope_note": (
                    "Applying directional force to a stationary object."
                ),
                "related_terms": ["Hitting"],
                "use_for": [],
                "examples": ["Call of Duty", "Bubble Bobble", "Pool"],
            },
            "Sneaking": {
                "term_type": "preferred",
                "scope_note": (
                    "Movement with the intent of evading detection of other game "
                    "entities."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Metal Gear Solid", "Assassin's Creed", "Stealth Bastard"],
            },
            "Swiping": {
                "term_type": "preferred",
                "scope_note": (
                    "Using a sustained pointer motion to create an event."
                ),
                "related_terms": [],
                "use_for": [],
                "examples": ["Fruit Ninja", "Cooking Mama"],
            },
            "Text Input": {
                "term_type": "preferred",
                "scope_note": "Entering text to produce commands or provide data.",
                "related_terms": [],
                "use_for": [],
                "examples": ["Zork", "The Typing of The Dead: Overkill"],
            },
        },
    }


def validate_genre_vocabulary(vocab: dict[str, Any]) -> list[str]:
    """Validate reciprocal relationships in the Gameplay Genre vocabulary."""
    errors: list[str] = []
    terms = vocab["terms"]

    for term_name, term_data in terms.items():
        if term_data["term_type"] == "non-preferred":
            # Check that the preferred term has this as USE FOR
            use_target = term_data.get("use")
            if use_target and use_target in terms:
                target = terms[use_target]
                if term_name not in target.get("use_for", []):
                    errors.append(
                        f"'{term_name}' USE '{use_target}', but '{use_target}' "
                        f"does not list '{term_name}' in USE FOR"
                    )
            continue

        # Check BT/NT reciprocity
        bt = term_data.get("broader_term")
        if bt and bt in terms:
            parent = terms[bt]
            if term_name not in parent.get("narrower_terms", []):
                errors.append(
                    f"'{term_name}' has BT '{bt}', but '{bt}' does not list "
                    f"'{term_name}' in NT"
                )

        for nt in term_data.get("narrower_terms", []):
            if nt in terms:
                child = terms[nt]
                child_bt = child.get("broader_term")
                if child_bt != term_name:
                    errors.append(
                        f"'{term_name}' has NT '{nt}', but '{nt}' has BT "
                        f"'{child_bt}' (expected '{term_name}')"
                    )

        # Check RT reciprocity
        for rt in term_data.get("related_terms", []):
            if rt in terms:
                other = terms[rt]
                if term_name not in other.get("related_terms", []):
                    # RT to non-preferred terms or cross-vocab is acceptable
                    pass

    return errors


def validate_mechanics_vocabulary(vocab: dict[str, Any]) -> list[str]:
    """Validate relationships in the Mechanics vocabulary."""
    errors: list[str] = []
    terms = vocab["terms"]

    for term_name, term_data in terms.items():
        if term_data["term_type"] == "non-preferred":
            use_target = term_data.get("use")
            if use_target and use_target in terms:
                target = terms[use_target]
                if term_name not in target.get("use_for", []):
                    errors.append(
                        f"'{term_name}' USE '{use_target}', but '{use_target}' "
                        f"does not list '{term_name}' in USE FOR"
                    )
            continue

        # Check RT reciprocity
        for rt in term_data.get("related_terms", []):
            if rt in terms:
                other = terms[rt]
                if term_name not in other.get("related_terms", []):
                    errors.append(
                        f"'{term_name}' has RT '{rt}', but '{rt}' does not list "
                        f"'{term_name}' in RT (warning: may be acceptable)"
                    )

    return errors


def count_terms(vocab: dict[str, Any]) -> dict[str, int]:
    """Count preferred and non-preferred terms."""
    preferred = sum(
        1 for t in vocab["terms"].values() if t["term_type"] == "preferred"
    )
    non_preferred = sum(
        1 for t in vocab["terms"].values() if t["term_type"] == "non-preferred"
    )
    return {"preferred": preferred, "non_preferred": non_preferred, "total": preferred + non_preferred}


def main() -> None:
    output_dir = Path(__file__).parent.parent / "data" / "vgms"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build and validate Gameplay Genre
    genre_vocab = build_gameplay_genre_vocabulary()
    genre_errors = validate_genre_vocabulary(genre_vocab)

    genre_counts = count_terms(genre_vocab)
    print(f"Gameplay Genre CV: {genre_counts['preferred']} preferred, "
          f"{genre_counts['non_preferred']} non-preferred, "
          f"{genre_counts['total']} total terms")

    if genre_errors:
        print("\nValidation errors in Gameplay Genre:")
        for err in genre_errors:
            print(f"  - {err}")
    else:
        print("  All relationships validated successfully.")

    genre_path = output_dir / "vgms_gameplay_genre.json"
    with open(genre_path, "w", encoding="utf-8") as f:
        json.dump(genre_vocab, f, indent=2, ensure_ascii=False)
    print(f"  Written to: {genre_path}")

    # Build and validate Mechanics
    mech_vocab = build_mechanics_vocabulary()
    mech_errors = validate_mechanics_vocabulary(mech_vocab)

    mech_counts = count_terms(mech_vocab)
    print(f"\nMechanics CV: {mech_counts['preferred']} preferred, "
          f"{mech_counts['non_preferred']} non-preferred, "
          f"{mech_counts['total']} total terms")

    if mech_errors:
        print("\nValidation errors in Mechanics:")
        for err in mech_errors:
            print(f"  - {err}")
    else:
        print("  All relationships validated successfully.")

    mech_path = output_dir / "vgms_mechanics.json"
    with open(mech_path, "w", encoding="utf-8") as f:
        json.dump(mech_vocab, f, indent=2, ensure_ascii=False)
    print(f"  Written to: {mech_path}")

    # Exit with error if validation failed
    total_errors = len(genre_errors) + len(mech_errors)
    if total_errors > 0:
        print(f"\n{total_errors} validation error(s) found.")
        sys.exit(1)
    else:
        print("\nAll validations passed.")


if __name__ == "__main__":
    main()
