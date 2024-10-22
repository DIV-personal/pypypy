import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional

from support import *
from support import Position

class Weapon:
    """
    Abstract class from which all instantiated types of weapon inherit.
    Provides default weapon behaviour.


    Attributes:
        - get_name: The name of the weapon
        - get_symbol: The symbol of the weapon
        - get_effect: Returns a dictionary representing the weapon's effect
        - get_targets: Returns a list of all positions within the range for this
          weapon, given the weapon is currently at position.
    """

    def __init__(self):
        """
        Initializes the instance based on Weapon behaviour
        """
        self._symbol = "W"
        self._name = "AbstractWeapon"
        self._effect = {}  #dictionary {key(str):Value(int)} 
        # weapontype(damage/healing/poison)
        self._range = 0
        # diagonal damage not allowed

    def get_name(self) -> str:
        """
        Returns the name of the weapon
        """
        return self._name
        
    def get_symbol(self) -> str:
        """
        Returns the symbol of the weapon
        """
        return self._symbol
    
    def get_effect(self) -> dict[str, int]:
        """
        Returns a dictionary representing the weapons effects
        """
        return self._effect

    def get_targets(self, position: tuple[int, int]) -> list[Position]:
        """
        Returns a list of all positions within range for this weapon

        Precondition:
            Weapon is currently at position

        Parameters:
            self, position : tuple [int, int]

        Returns:
            ans = [Positions]
        """
        row, col = position
        targets = []

        # Generating all positions within the range in four directions
        for i in range(1, self._range + 1):
            targets.append(Position((row + i, col)))  # Down
            targets.append(Position((row - i, col)))  # Up
            targets.append(Position((row, col + i)))  # Right
            targets.append(Position((row, col - i)))  # Left

        return targets

    def __str__(self) -> str:
        """
        Returns the name of the weapon
        """
        return self._name
    
    def __repr__(self) -> str:
        """
        Returns the representation of the weapon class
        """
        return self.__class__.__name__ + "()"
    
class PoisonDart(Weapon):
    """
    PoisonDart inherits from Weapon
    A poison dart has a range of 2 and applies 2 poison to its targets
    """
    def __init__(self) -> None:
        super().__init__()
        self._name = "PoisonDart"
        self._symbol = POISON_DART_SYMBOL
        self._effect = {"poison" : 2}
        self._range = 2

class PoisonSword(Weapon):
    """
    PoisonSword inherits from Weapon
    A poison sword has a range of 1 and both damages its targets
    by 2 and increases their poison stat by 1
    """

    def __init__(self):
        super().__init__()
        self._name = "PoisonSword"
        self._symbol = POISON_SWORD_SYMBOL
        self._effect = {"damage" : 2, "poison" : 1}
        self._range = 1

class HealingRock(Weapon):
    """
    Healing rock inherits from weapon
    A healing rock has a range of 2 and increases its targets health
    by 2
    """
    def __init__(self):
        super().__init__()
        self._name = "HealingRock"
        self._symbol = HEALING_ROCK_SYMBOL
        self._effect = {"healing" : 2}
        self._range = 2
    
class Tile():
    """
    Tile class represents individual tiles (positions) in the dungeon.
    
    Attributes:
        - symbol: A string representing what type of tile it is.
        - is_blocking: A boolean indicating whether the tile is blocking.
        - weapon: An optional weapon placed on this tile (default: None).
        
    Methods:
        - is_blocking
        - get_weapon
        - set_weapon
        - remove_weapon
        - __str__
        - __repr__
    """

    def __init__(self, symbol: str, is_blocking: bool) -> None:
        """
        Constructs a new tile instance with the given symbol and is_blocking 
        status

        Parameters:
            symbol (str): The symbol representing the tile.
            is_blocking (bool): Whether the tile is blocking movement.

        Returns:
            None
        """
        self._weapon = None
        self._symbol = symbol
        self._is_blocking = is_blocking
    
    def is_blocking(self) -> bool:
        """
        Returns True if this tile is blocking and False otherwise.
        """
        return self._is_blocking
    
    def get_weapon(self) -> Optional[Weapon]:
        return self._weapon

    def set_weapon(self, weapon: Weapon) -> None:
        """
        Sets the weapon on this tile to the provided weapon.
        
        Parameters:
            weapon (Weapon): The weapon to be placed on the tile.
        """
        self._weapon = weapon
    
    def remove_weapon(self) -> None:
        """
        Remove the weapon from the tile.
        """
        self._weapon = None

    def __str__(self) -> str:
        """
        Returns the symbol associated with this tile
        """
        return self._symbol
    
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to 
        construct an instance of Tile with the same symbol and is_blocking 
        status.
        """
        return f"{self.__class__.__name__}('{self._symbol}', {self._is_blocking})"

def create_tile(symbol: str) -> Tile:
    """
    Creates and returns an appropriate instance of Tile based on the symbol string.
    
    Parameters:
        symbol (str): The symbol representing the type of tile.
    
    Returns:
        Tile: An instance of the Tile class based on the symbol.
    """
    if symbol == WALL_TILE:
        # Wall tile (blocking)
        return Tile(WALL_TILE, True)
    
    elif symbol == FLOOR_TILE:
        # Floor tile (non-blocking)
        return Tile(FLOOR_TILE, False)
    
    elif symbol == GOAL_TILE:
        # Goal tile (non-blocking)
        return Tile(GOAL_TILE, False)
    
    elif symbol == POISON_DART_SYMBOL:
        # PoisonDart on a floor tile (non-blocking)
        tile = Tile(FLOOR_TILE, False)
        tile.set_weapon(PoisonDart())
        return tile
    
    elif symbol == POISON_SWORD_SYMBOL:
        # PoisonSword on a floor tile (non-blocking)
        tile = Tile(FLOOR_TILE, False)
        tile.set_weapon(PoisonSword())
        return tile
    
    elif symbol == HEALING_ROCK_SYMBOL:
        # HealingRock on a floor tile (non-blocking)
        tile = Tile(FLOOR_TILE, False)
        tile.set_weapon(HealingRock())
        return tile
    
    else:
        # Any other symbol represents a non-blocking floor tile
        return Tile(FLOOR_TILE, False) 

class Entity():
    """
    Abstract class representing an entity in the game (either Player or Slug)

    Attributes:
        - health: The current health of the entity.
        - poison: The current poison level of the entity.
        - max_health: The maximum health of the entity.
        - weapon: The weapon the entity is holding (if any).

    Methods:
        - get_symbol
        - get_name
        - get_health
        - get_poison
        - get_weapon
        - equip
        - get_weapon_target
        - get_weapon_effect
        - apply_effect
        - apply_poison
        - is_alive
    """
    def __init__(self, max_health: int) -> None:

        self._max_health = max_health
        self._health = max_health
        self._symbol = ENTITY_SYMBOL
        self._name = "Entity"
        self._poison = 0
        self._weapon = None

    # Returns the name of the entity
    def get_name(self)-> str:
        return self._name
    
    # Returns the symbol representing the Entity
    def get_symbol(self) -> str:
        return self._symbol
    
    # Returns the Entity's current health
    def get_health(self)->int:
        return self._health
    
    # Returns the entity's current posison level
    def get_poison(self)->int:
        return self._poison
    
    # Returns the weapon the entity is holding, or None if no weapon
    def get_weapon(self)-> Optional[Weapon]:
        return self._weapon
    
    # Equips the Entity with a weapon
    def equip(self, weapon:Weapon) -> None:
        self._weapon = weapon

    def get_weapon_targets(self, position: Position) -> list[Position]:
        """
        Returns the positions the entity can attack with its weapon from the 
        given position

        If the entity doesnt have a weapon this method should return an empty 
        list
        """
        if self._weapon:
            return self._weapon.get_targets(position)
        return[]

    # Returns the effect of Entity's weapon
    # If no weapon is helds, returns empty dictionary
    def get_weapon_effect(self) -> dict[str, int]:
        if self._weapon:
            return self._weapon.get_effect()
        return {}

    # Applies effect (damage, poison, healing) to the Entity
    def apply_effects(self, effects:dict[str, int]) -> None:
        for effect, value in effects.items():
            if effect == "healing":
                self._health = min(self._max_health, self._health + value)
            elif effect == "damage":
                self._health = max(0, self._health - value)
            elif effect == "poison":
                self._poison += value  
    
    # Reduces Entity's health by its poison amount & decreases poison by 1
    def apply_poison(self) -> None:
        """
        Reduces the entitys health by its poison amount
        """
        if self._poison > 0:
            self._health = max(0, self._health - self._poison)
            self._poison -= 1

    # Returns True if the Entity is alive (health > 0), otherwise False
    def is_alive(self) -> bool:
        """
        Returns True if the entity is still alive
        health > 0
        """
        return self._health > 0
    
    # Returns the name of the Entity
    def __str__(self) -> str:
        return self.get_name()
    
    # Returns a string representation of the entity
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._max_health})"

class Player(Entity):
    """
    Players inherits from Entity
    """
    def __init__(self, max_health: int) -> None:
        super().__init__(max_health)
        self._name = "Player"
        self._symbol = PLAYER_SYMBOL

class Slug(Entity):
    """
    Abstract class representing a slug Entity
    Slug inherits from Entity
    Slugs can only move every second turn
    """
    def __init__(self, max_health: int) -> None:
        super().__init__(max_health)
        self._name = "Slug"
        self._can_move = True
        self._symbol = SLUG_SYMBOL

    # Returns True if the slug can move this turn, otherwise False
    def can_move(self) -> bool:
        """
        Returns True if the slug can move on this turn and False otherwise
        """
        return self._can_move
    
    # Toggles the slug's ability to move
    def end_turn(self) -> None:
        self._can_move = not self._can_move
    
    # Abstract method to be implemented by child class
    def choose_move(self, coordinates: list[Position], 
                    current_position: Position, 
                    player_position: Position)->Position:
        # Slug subclasses must implement a choose_move method
        raise NotImplementedError("Slug subclasses must implement a choose_move method.")

class NiceSlug(Slug):
    """
    NiceSlug inherites from Slug
    Stays in place whenever it can move
    """
    def __init__(self) -> None:
        super().__init__(10)
        # Has a health = 10
        # NiceSlug starts with a Healing Rock
        self.equip(HealingRock())
        self._name = "NiceSlug"
        self._symbol = NICE_SLUG_SYMBOL
    
    def choose_move(self, coordinates: list[Position], 
                    current_position: Position, 
                    player_position: Position)->Position:
        # Slug subclasses must implement a choose_move method
        return current_position    
    
    def __repr__(self) -> str:
        return f"{self._name}()"

class AngrySlug(Slug):
    """
    AngrySlug inherits from Slug
    Tries to move towards the player when it can move
    """
    def __init__(self) -> None:
        super().__init__(5)
        # Angry slug health = 5
        # AngrySlug starts with a Poison Sword
        self.equip(PoisonSword())
        self._name = "AngrySlug"
        self._symbol = ANGRY_SLUG_SYMBOL
    
    def choose_move(self, coordinates: list[Position], 
                    current_position: Position, 
                    player_position: Position) -> Position:
        
        if not coordinates:
            return current_position

        x1 = player_position[0]
        y1 = player_position[1]
        distance = []
        
        for coordinate in coordinates:
            x2 = coordinate[0]
            y2 = coordinate[1]
            value = (x1-x2)**2 + (y1-y2)**2
            distance.append(value)
        # now list is ready with all euclidean distances
        index_min_distance = distance.index(min(distance))
        Position = coordinates[index_min_distance]
        
        return Position
    
    def __repr__(self) -> str:
        return f"{self._name}()"

class ScaredSlug(Slug):
    """
    Scared Slug inherits from Slug
    Moves away from the player when it can move
    """
    def __init__(self) -> None:
        super().__init__(3)
        # Scared Slug health = 3
        # Scared Slug starts with a PoisonDart
        self.equip(PoisonDart())
        self._name = "ScaredSlug"
        self._symbol = SCARED_SLUG_SYMBOL
    
    def choose_move(self, coordinates: list[Position], 
                    current_position: Position, 
                    player_position: Position) -> Position:
        
        if not coordinates:
            return current_position

        x1 = player_position[0]
        y1 = player_position[1]
        distance = []
        
        for coordinate in coordinates:
            x2 = coordinate[0]
            y2 = coordinate[1]
            value = (x1-x2)**2 + (y1-y2)**2
            distance.append(value)
        # now list is ready with all euclidean distances
        index_max_distance = distance.index(max(distance))
        Position = coordinates[index_max_distance]
        
        return Position
    
    def __repr__(self) -> str:
        return f"{self._name}()"
    
class SlugDungeonModel():
    """
    Logical state of the game

    Attributes:
        - tiles: list of Tile instances
        - slugs: Dictionry mapping slug positions
        - player: Player instance and player_position is the player's
          starting position

    Methods:
        - get_tiles
        - get_slugs
        - get_player
        - get_player_position
        - get_tile(self, position: Posiiton)-> Tiles
        - get_dimensions(Self) -> tuple[int, int]
        - get_valid_slug_position(self, slug: Slug) -> list[Position]

    """
    def __init__(self, tiles: list[list[Tile]], slugs: dict[Position, Slug], 
                 player: Player, player_position: Position) -> None:
        """
        Initialize the Slug Dungeon Model
        """
        self._tiles = tiles
        self._slugs = slugs.copy()
        self._player = player
        self._player_position = player_position
        # never change the order of slug dictionary
        # all operations should follow this order      

    def get_tiles(self)->list[list[Tile]]:
        return self._tiles
    
    def get_slugs(self)->dict[Position, Slug]:
        """
        Returns a dictionary mapping slug positions to the Slug instances at 
        those positions
        """
        return self._slugs
    
    def get_player(self)->Player:
        return self._player
    
    def get_player_position(self)->Position:
        return self._player_position
    
    def get_tile(self, position)->Tile:
        row, col = position
        return self._tiles[row][col]
    
    def get_dimensions(self) -> tuple[int, int]:
        return (len(self._tiles), len(self._tiles[0]))
    
    def get_valid_slug_positions(self, slug: Slug) -> list[Position]:
        """
        A list of valid positons that slug can move to from its current
        position in the next move
        A slug can move to:
            - It's current position
            - One position up, dpwn, left, or right of its current position
        If the slug cannot move on this turn, return []

        Parameters: 
            slug(Slug): The slug object

        Returns:
            valid_position = []
        """
        
        if slug.can_move() == False:
            return []
        
        for key, value in self._slugs.items():
            if value == slug:
                x = key[0]
                y = key [1]

        # Creating list of possible moves
        possible_moves = [(x-1, y),
                          (x+1, y),
                          (x, y-1),
                          (x, y+1)]
        
        valid_moves = [(x,y)]

        for move in possible_moves:
            row, col = move
            if 0 <= row < len(self._tiles) and 0 <= col < len(self._tiles[0]):
                tile = self.get_tile((row, col))
                if not tile.is_blocking() and (move not in self._slugs.keys()) and (move != self._player_position):
                    valid_moves.append(move)

        return valid_moves
        
    def perform_attack(self, entity: Entity, position: Position) -> None:
        """
        Perform an attack on the given Entity
        """

        weapon_effect = entity.get_weapon_effect()

        if not weapon_effect:
            return
        
        target_positions = entity.get_weapon_targets(position)
        # player attacks slugs, slugs attack the player

        if isinstance(entity, Player):
            # Player attacks slugs
            for target_position in target_positions:
                if target_position in self._slugs.keys():
                    slug = self._slugs[target_position]
                    slug.apply_effects(weapon_effect)

                    slug.apply_poison()
                    if not slug.is_alive():
                        self._tiles[target_position[0]][target_position[1]].set_weapon(slug.get_weapon())
                        # del self._activeslugs[target_position]
                        
        else:
            # Slug attacks player if player is in range
            if self._player_position in target_positions:
                self._player.apply_effects(weapon_effect)
             
    def end_turn(self) -> None:
        """
        Handle the player's movement based on the given position change.
        
        Parameters:
            position_delta (tuple): The change in position, e.g., (0, 1) for 
            moving right.
        """

        # Apply poison to the player
        self._player.apply_poison()

        # Apply poison to each slug
        for position, slug in list(self._slugs.items()):
            slug.apply_poison()

            row = position[0]
            col = position[1]
            # Remove slug if dead
            if not slug.is_alive():
                self._tiles[row][col].set_weapon(slug.get_weapon())
                del self._slugs[position]
                break

        # Move slugs if they can move
        for position, slug in list(self._slugs.items()):
            if slug.can_move():
                valid_moves = self.get_valid_slug_positions(slug)
                if valid_moves:
                    # choosing a new position based on slugs movement
                    new_position = slug.choose_move(valid_moves, position, self._player_position)
                    self._slugs[new_position] = self._slugs.pop(position)
        
        # Slug attacks the player after moving
        for position, slug in self._slugs.items():
            self.perform_attack(slug, position)
        
        # End the slugs turn
        for slug in self._slugs.values():
            slug.end_turn()

    def handle_player_move(self, position_delta: Position) -> None:
        """
        Move the player and handle the consequences of the move

        Parameters:
            position delta (support.py): Positions

        Retunrs:
            None
        """
        # Calculate the player's new position
        new_position = (self._player_position[0] + position_delta[0],
                        self._player_position[1] + position_delta[1])
        
        # Check if the move is valid
        if 0 <= new_position[0] < len(self._tiles) and 0 <= new_position[1] < len(self._tiles[0]):
            if not self._tiles[new_position[0]][new_position[1]].is_blocking() and new_position not in self._slugs:
                # update player's position
                self._player_position = new_position

                # if there's a weapon at the new position, pick it up
                tile = self._tiles[new_position[0]][new_position[1]]
                if tile.get_weapon() is not None:
                    self._player.equip(tile.get_weapon())
                    tile.remove_weapon()

                # Player performs an attack from their new position
                self.perform_attack(self._player, new_position)

                # End the turn, which includes handling slugs
                self.end_turn()

    def has_won(self) -> bool:
        """
        Check if the player has won
        (All slugs are dead and the player is on the goal tile)
        """
        for slug in self._slugs.values():
            if slug.is_alive():
                # If any slug is still alive, the player hasn't won
                return False
    
        # Check if the player is on a goal tile
        player_tile = self.get_tile(self._player_position)._symbol
        return player_tile == GOAL_TILE

    def has_lost(self) -> bool:
        # Logic for checking lose condition
        return not self._player.is_alive()

def load_level(filename:str) -> SlugDungeonModel:
    """
    Loads a level from a file and return a SlugDungeonModel instance.
    
    Parameters:
        filename (str): The path to the level file.
    
    Returns:
        SlugDungeonModel: An instance of the model initialized with the level 
        data.
    """

    with open(filename, 'r') as file:
        # Read the player's max health from first line
        max_health = int(file.readline().strip())

        tile = []    # 2D grid of tiles
        slugs = {}   # dictionary mapping slug position
        player = None  #will store the player object
        player_position = None #will store the player's starting position

        #Read the rest of the file line by line 
        for row_index, line in enumerate(file):
            row = []
            for col_index, symbol in enumerate(line.strip()):
                position = (row_index, col_index)

                if symbol == WALL_TILE:
                    row.append(create_tile(WALL_TILE))
                elif symbol == FLOOR_TILE:
                    row.append(create_tile(FLOOR_TILE))
                elif symbol == GOAL_TILE:
                    row.append(create_tile(GOAL_TILE))
                elif symbol == POISON_DART_SYMBOL:
                    row.append(create_tile(POISON_DART_SYMBOL))
                elif symbol == POISON_SWORD_SYMBOL:
                    row.append(create_tile(POISON_SWORD_SYMBOL))
                elif symbol == HEALING_ROCK_SYMBOL:
                    row.append(create_tile(HEALING_ROCK_SYMBOL))
                elif symbol == PLAYER_SYMBOL:  # Player's starting position
                    row.append(create_tile(FLOOR_TILE))
                    player = Player(max_health)
                    player_position = position
                elif symbol == NICE_SLUG_SYMBOL:  # NiceSlug
                    row.append(create_tile(FLOOR_TILE))
                    slugs[position] = NiceSlug()
                elif symbol == ANGRY_SLUG_SYMBOL:  # AngrySlug
                    row.append(create_tile(FLOOR_TILE))
                    slugs[position] = AngrySlug()
                elif symbol == SCARED_SLUG_SYMBOL:  # ScaredSlug
                    row.append(create_tile(FLOOR_TILE))
                    slugs[position] = ScaredSlug()
                else:
                    row.append(create_tile(FLOOR_TILE))  # Treat unknown symbols as empty tiles

            tile.append(row)

    # Create and return the SlugDungeonModel instance
    return SlugDungeonModel(tile, slugs, player, player_position)
   
class DungeonMap(AbstractGrid):
    """
    Represents the entity statistics in a grid. Inherits from AbstractGrid.
    """
    def __init__(self, master: tk.Tk | tk.Frame, dimensions: Position[int], size: Position[int], **kwargs) -> None:
        super().__init__(master, dimensions, size, **kwargs)
    
    def redraw(self, tiles: list[list[Tile]], player_position: Position, slugs: dict[Position, Slug]) -> None:
        """
        Redraws the dungeon map based on the current state of the game

        Arguments:
            -tiles: A list of Tile objects representing the game grid
            -player_position: The current position of the player
            -slugs: A dictionary of positions and their corresponding slug 
            entities
        """
        self.clear()

        # Running through the grid to draw the tiles
        for row in range(len(tiles)):
            for col in range(len(tiles[row])):
                tile = tiles[row][col]

                # Determine the color based on tile type
                if tile == '#':  # Wall
                    color = WALL_COLOUR
                elif tile == 'G':  # Goal
                    color = GOAL_COLOUR
                else:  # Floor tile
                    color = FLOOR_COLOUR

                # Draw the rectangle representing the tile
                self._draw_rectangle(row, col, color)

        

    # def __init__(self, master: tk.Tk | tk.Frame, dimensions: Position, 
    #             size: Position, **kwargs) -> None:
    #     """
    #     Initializes the Dungeon Map

    #     Arguments:
    #         - master: The root or frame where this widget is packed
    #         - dimensions: Number of rows and columns in the grid
    #         - size: Pixel size for width and height of the grid
    #     """
    #     super().__init__(master, dimensions, size, **kwargs)
    
    # def _draw_rectangle(self, row: int, col: int, color: str) -> None:
    #     """
    #     Draws a single tile on the grid.

    #     Args:
    #     - row: The row of the tile.
    #     - col: The column of the tile.
    #     - color: The color to fill the tile.
    #     """
    #     bbox = self.get_bbox((row, col))  # Get the bounding box for this cell
    #     self.create_rectangle(bbox, fill = color, outline = color)  # Draw the tile
    
    # def _draw_oval(self, position: 'Position', symbol: str, color: str) -> None:
    #     """
    #     Draws an oval (entity) at a given position on the grid.

    #     Args:
    #     - position: The position of the entity (row, column).
    #     - symbol: The symbol representing the entity (e.g., "P" for player).
    #     - color: The color of the oval.
    #     """
    #     bbox = self.get_bbox(position)  # Get the bounding box for the position
    #     self.create_oval(bbox, fill=color)  # Draw the oval
    #     self.annotate_position(position, symbol)  # Add the symbol (text) inside the oval

    # def _draw_weapon_symbol(self, row: int, col: int, symbol: str) -> None:
    #     """
    #     Draws the weapon symbol at the specified row and column.

    #     Args:
    #     - row: The row of the tile.
    #     - col: The column of the tile.
    #     - symbol: The symbol representing the weapon.
    #     """
    #     self.annotate_position((row, col), symbol)  # Add the weapon symbol    

    # def redraw(self, tiles: list[list["Tile"]], player_position: "Position", 
    #            slugs: dict["Position", "Slug"]) -> None:
    #     """
    #     Redraws the dungeon map based on the current state of the game

    #     Arguments:
    #         -tiles: A list of Tile objects representing the game grid
    #         -player_position: The current position of the player
    #         -slugs: A dictionary of positions and their corresponding slug 
    #         entities
    #     """
        
    #     self.clear()

    #     #Draw all the tiles
    #     for row in range(len(tiles)):
    #         for col in range(len(tiles[row])):
    #             tile = tiles[row][col]

    #             #Determine color based on the type of tile
    #             if tile.is_blocking():
    #                 color = WALL_COLOUR
    #             elif str(tile) == GOAL_TILE:
    #                 color = GOAL_COLOUR
    #             else:
    #                 color = FLOOR_COLOUR

    #             #Draw the rectangle (tile) on the grid
    #             self._draw_rectangle(row, col, color)

    #             #Check if there is a weapon on this tile
    #             weapon = tile.get_weapon()
    #             if weapon:
    #                 self._draw_weapon_symbol(row, col, weapon.get_symbol())

    #     #Draw the player as a blue oval
    #     self._draw_oval(player_position, PLAYER_SYMBOL, PLAYER_COLOUR)

    #     #Draw all slugs
    #     for slug_position, slug in slugs.items():
    #         color = "lightpink" if slug.can_move() else SLUG_COLOUR
    #         self._draw_oval(slug_position, slug.get_symbol(), color)

class DungeonInfo(AbstractGrid):
    """
    DungeonInfo is a view component that displays information about entities.
    It shows Name, Position, Weapon, Health, and Poison stats for the player and slugs.

    Inherits from AbstractGrid (provided in support.py)
    """
    def __init__(self, master: tk.Tk | tk.Frame, dimensions: Position, size: Position, **kwargs) -> None:
        """
        Initializes the DungeonInfo.

        Arguments:
            - master: The root or frame where this widget is packed.
            - dimensions: Number of rows and columns in the grid.
            - size: Pixel size for width and height of the grid.
        """
        super().__init__(master, dimensions, size, **kwargs)
    
    def _draw_header(self) -> None:
        """
        Draws the header row with column titles
        """
        headers = ["Name", "Position", "Weapon", "Health", "Poison"]
        for col, header in enumerate(headers):
            self.annotate_position((0, col), header)

    def _draw_entity_info(self, row: int, name: str, position: 'Position', weapon: 'Weapon', health: int, poison: int) -> None:
        """
        Draws entity information in a specific row of the grid.

        Arguments:
        - row: The row number to place the information.
        - name: The name of the entity (Player or Slug).
        - position: The position of the entity in the dungeon.
        - weapon: The weapon the entity is holding (or None).
        - health: The health stat of the entity.
        - poison: The poison stat of the entity.
        """
        # Display entity's name
        self.annotate_position((row, 0), name)

        # Display entity's position as a string
        self.annotate_position((row, 1), str(position))

        # Display weapon (if any), otherwise "None"
        weapon_name = weapon.get_name() if weapon else "None"
        self.annotate_position((row, 2), weapon_name)

        # Display health and poison stats
        self.annotate_position((row, 3), str(health))
        self.annotate_position((row, 4), str(poison))

    def redraw(self, entities: dict['Position', 'Entity']) -> None:
        """
        Redraws the entity information, including the player's and slugs' details.

        Arguments:
        - entities: A dictionary where the key is the position and the value is the entity (Player or Slug).
        """
        # Clear any existing content
        self.clear()

        # Draw the header row
        self._draw_header()

        # Start at row 1 for entity data (row 0 is the header)
        row = 1

        # Iterate through entities and display their information
        for position, entity in entities.items():
            # Extract entity information
            name = entity.get_name()
            weapon = entity.get_weapon()
            health = entity.get_health()
            poison = entity.get_poison()
            
            # Draw the information in the grid
            self._draw_entity_info(row, name, position, weapon, health, poison)
            row += 1

class ButtonPanel(tk.Frame):
    """
    ButtonPanel is a view component that contains buttons for loading a new game and quitting the game.
    
    Inherits from tk.Frame and provides two buttons:
        - Load Game: Allows the user to load a new game.
        - Quit: Exits the game.
        
    Arguments:
        - root: The parent widget.
        - on_load: The function to call when the Load Game button is clicked.
        - on_quit: The function to call when the Quit button is clicked.
    """
    def __init__(self, root, on_load, on_quit):
        """
        Initialize the ButtonPanel with 'Load Game' and 'Quit' buttons.
        :param root: The parent widget.
        :param on_load: The command to execute when the 'Load Game' button is pressed.
        :param on_quit: The command to execute when the 'Quit' button is pressed.
        """
        super().__init__(root)
        self.load_button = tk.Button(self, text="Load Game", command=on_load)
        self.load_button.pack(side="left", padx=10, pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=on_quit)
        self.quit_button.pack(side="right", padx=10, pady=10)

class SlugDungeon():
    """
    SlugDungeon is the controller for the game
    """

    pass

def play_game(root: tk.Tk, file_path: str) -> None:
    """
    Initialize and start the game by creating the controller and loading the 
    level file

    Arguments:
        - root (tk.Tk): The Tkinter root window
        - file_path(str): The file to the initial game level

    """
    root.title("Slug Dungeon")
 
    root.mainloop()

def main() -> None:
    """
    Initializes the game and starts the main event loop.
    Used to test the game locally.
    """
    root = tk.Tk()

    file_path = "levels.level1.txt"

    play_game(root, file_path)

if __name__ == "__main__":
    main()