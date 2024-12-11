from os.path import dirname, join
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

class Potter:

    def __init__(self):
        # Initialize house points
        self.house_points = {
            "Gryffindor": 0,
            "Slytherin": 0,
            "Ravenclaw": 0,
            "Hufflepuff": 0
        }
        #Houses get added to set when command invisibility cloak is used
        self.invisibility_cloak = set()

    def get_house_points(self):
        return self.house_points

    #Interpreter
    def interpret(self, model):
        for command in model.commands:
            if command.__class__.__name__ == "Spell":
                self.apply_spell(command)
            elif command.__class__.__name__ == "Charm":
                self.apply_charm(command)
            elif command.__class__.__name__ == "Jinx":
                self.apply_jinx(command)
            elif command.__class__.__name__ == "Curse":
                self.apply_curse(command)
            elif command.__class__.__name__ == "Snitch":
                self.apply_snitch(command)
                print("Game ends! The Golden Snitch has been caught!")
                break
            elif command.__class__.__name__ == "Cloak":
                self.apply_cloak(command)
        
            

    #Points added/lost for spells
    def apply_spell(self, command):
        print(f"Casting spell: {command.spell}")
        if(command.spell=="APPARATE"):
            self.update_points(command.houses, gainPoint=60, losePoints=0)
        elif(command.spell=="ANAPNEO"):
            self.update_points(command.houses, gainPoints=50, losePoints=0)
        elif(command.spell=="BRACKIUM EMENDO"):
            self.update_points(command.houses, gainPoints=70, losePoints=0)
        else:
            print("Not a valid spell")

    #Points added/lost for charms
    def apply_charm(self, command):
        print(f"Casting charm: {command.charm}")
        if(command.charm=="ASCENDIO"):
            self.update_points(command.houses, gainPoints=50, losePoints=50)
        elif(command.charm=="LUMOS"):
            self.update_points(command.houses, gainPoints=20, losePoints=0)
        elif(command.charm=="PROTEGO"):
            self.update_points(command.houses, gainPoints=75, losePoints=0)
        elif(command.charm=="EXPECTO PATRONUM"):
            self.update_points(command.houses, gainPoints=100, losePoints=0)
        elif(command.charm=="EPISKEY"):
            self.update_points(command.houses, gainPoints=30, losePoints=0)
        elif(command.charm=="FERULA"):
            self.update_points(command.houses, gainPoints=40, losePoints=0)
        elif(command.charm=="EXPELLIARMUS"):
            self.update_points(command.houses, gainPoints=50, losePoints=50)
        elif(command.charm=="CONFUNDO"):
            self.update_points(command.houses, gainPoints=40, losePoints=40)
        elif(command.charm=="BOMBARDO"):
            self.update_points(command.houses, gainPoints=60, losePoints=60)
        elif(command.charm=="APPARECIUM"):
            self.update_points(command.houses, gainPoints=30, losePoints=0)
        else:
            print("Not a valid charm")


    #Points added/lost for jinxs
    def apply_jinx(self, command):
        print(f"Casting jinx: {command.jinx}")
        if(command.jinx=="OPPUGNO"):
            self.update_points(command.houses, gainPoints=100, losePoints=100)
        elif(command.jinx=="BROOM JINX"):
            self.update_points(command.houses, gainPoints=75, losePoints=75)
        else:
            print("Not a valid jinx")

    #Points added/lost for curse
    def apply_curse(self, command):
        print(f"Casting curse: CRUCIO")
        if command.house:
            self.update_points([command.house], gainPoints=-1000, losePoints=0)
        else:
            self.update_points(self.house_points.keys(), gainPoints=-1000, losePoints=0)

    ##Points added for catching golden snitch - game over
    def apply_snitch(self, command):
        print(f"Catching the GOLDEN SNITCH")
        if command.house:
            self.update_points([command.house], gainPoints=1000, losePoints=0)
        else:
            self.update_points(self.house_points.keys(), gainPoints=1000, losePoints=0)

    def apply_cloak(self,command):
        print(f"{command.house} wearing the Invisibility Cloak")
        if command.house:
            self.invisibility_cloak.add(command.house)
        else:
            print("No house specified for the Invisibility Cloak.")


    #Update points
    def update_points(self, houses, gainPoints, losePoints):
        if houses:
            for i, house in enumerate(houses):
                # Gain points for the first house
                if i == 0:
                    self.house_points[house] += gainPoints
                # Lose points for subsequent houses
                elif house not in self.invisibility_cloak:
                    self.house_points[house] -= losePoints

            print("Updated points:", end=" ")
            for i, house in enumerate(houses):
                if i == 0:
                    print(f"{house} +{gainPoints}", end=" ")
                #Lose points if house has not used invisibility cloak command
                elif house not in self.invisibility_cloak:
                    print(f"{house} -{losePoints}", end=" ")
            print()
        else:
            print("No houses specified for this command.")


def main(debug=False):
    this_folder = dirname(__file__)

    # Load the Potter metamodel
    potter_mm = metamodel_from_file(join(this_folder, 'potter.tx'), debug=debug)
    metamodel_export(potter_mm, join(this_folder, 'potter_meta.dot'))

    # Load and parse the Potter program
    potter_model = potter_mm.model_from_file(join(this_folder, 'program1.potter'))
    model_export(potter_model, join(this_folder, 'potter_model.dot'))

    # Interpret the model
    game = Potter()
    game.interpret(potter_model)

    print("Final House Points:")

    house_points = game.get_house_points()
    gryffindor_points = house_points["Gryffindor"]
    slytherin_points = house_points["Slytherin"]
    ravenclaw_points = house_points["Ravenclaw"]
    hufflepuff_points = house_points["Hufflepuff"]

    house_points = {
        "Gryffindor": gryffindor_points,
        "Slytherin": slytherin_points,
        "Ravenclaw": ravenclaw_points,
        "Hufflepuff": hufflepuff_points
    }

    winner = max(house_points, key=house_points.get)

    for house, points in house_points.items():
        print(f"{house}: {points}")

    print(f"The winner is: {winner}")


if __name__ == "__main__":
    main()

