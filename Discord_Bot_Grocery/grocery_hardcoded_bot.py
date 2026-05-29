import discord
from discord.ext import commands

# Define your bot's prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Hardcoded grocery lists and meal plans
stores = {
    "frys": {
        "40": {
            "groceries": [
                "2 large bags of dry beans (pinto or black)",
                "1 large bag of long-grain rice",
                "2 lbs dried pasta",
                "1 large canister of rolled oats",
                "1 dozen eggs",
                "1 large tub of peanut butter",
                "1 loaf of store-brand sandwich bread",
                "1 large bag of russet potatoes",
                "1 large bag of yellow onions",
                "1 bag of carrots",
                "2 cans of diced tomatoes",
                "1 gallon of milk",
                "Cooking oil and basic seasonings (salt, pepper, chili powder)"
            ],
            "meals": [
                "Beans and Rice: Simple, filling, and can be seasoned in many ways.",
                "Pasta with Tomato Sauce: A classic budget meal.",
                "Oatmeal for Breakfast: Topped with a little peanut butter for extra protein.",
                "Potato and Egg Scramble: A hearty breakfast or dinner with sautéed onions and potatoes.",
                "Peanut Butter Sandwiches: A quick and easy lunch option."
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Oatmeal with peanut butter",
                        "lunch": "Beans and rice with onions",
                        "dinner": "Pasta with tomato sauce"
                    },
                    "tuesday": {
                        "breakfast": "Potato and egg scramble",
                        "lunch": "Peanut butter sandwich with carrot sticks",
                        "dinner": "Rice and beans with sautéed onions"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Pasta with tomato and onion sauce"
                    },
                    "thursday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Rice and beans",
                        "dinner": "Potato hash with carrots and onions"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with peanut butter",
                        "lunch": "Peanut butter sandwich with carrots",
                        "dinner": "Beans and rice bowl"
                    },
                    "saturday": {
                        "breakfast": "Scrambled eggs with potatoes",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Pasta with tomato sauce"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Rice and beans",
                        "dinner": "Egg and potato scramble"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Oatmeal with peanut butter",
                        "lunch": "Beans and rice",
                        "dinner": "Pasta with tomato and onions"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Potato and carrot hash"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Rice and beans",
                        "dinner": "Beans and rice with sautéed onions"
                    },
                    "thursday": {
                        "breakfast": "Peanut butter toast",
                        "lunch": "Peanut butter sandwich with carrots",
                        "dinner": "Pasta with tomato sauce"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with peanut butter",
                        "lunch": "Rice and beans",
                        "dinner": "Egg and potato scramble"
                    },
                    "saturday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Beans and rice"
                    },
                    "sunday": {
                        "breakfast": "Scrambled eggs with potatoes",
                        "lunch": "Rice and beans",
                        "dinner": "Pasta with tomato sauce"
                    }
                }
            }
        },
        "60": {
            "groceries": [
                "1 large bag of rice",
                "1 bag of dried lentils",
                "2 bags of dried pasta",
                "1 large bag of potatoes",
                "1 large package of bone-in chicken thighs",
                "1 dozen eggs",
                "1 lb ground beef (or ground turkey)",
                "1 block of cheddar cheese",
                "1 bag of onions",
                "1 head of cabbage",
                "1 bag of carrots",
                "1 head of broccoli",
                "1 gallon of milk",
                "1 large can of diced tomatoes",
                "1 small bag of apples"
            ],
            "meals": [
                "Lentil Soup: A very filling, protein-rich soup.",
                "Sheet Pan Chicken and Veggies: A one-pan meal with roasted chicken, potatoes, and broccoli.",
                "Ground Beef Tacos: Use rice as a base instead of tortillas to save money.",
                "Fried Cabbage with Chicken: A simple and cheap meal that's very tasty."
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Scrambled eggs with potatoes",
                        "lunch": "Lentil soup",
                        "dinner": "Sheet pan chicken with potatoes and broccoli"
                    },
                    "tuesday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Ground beef and cabbage skillet",
                        "dinner": "Pasta with turkey sauce and carrots"
                    },
                    "wednesday": {
                        "breakfast": "Cheese and egg scramble",
                        "lunch": "Potato hash with onions",
                        "dinner": "Chicken and rice bowls with carrots and broccoli"
                    },
                    "thursday": {
                        "breakfast": "Peanut butter toast",
                        "lunch": "Lentil and rice bowl",
                        "dinner": "Ground beef taco bowls with cabbage and cheese"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Cabbage stir-fry with carrots",
                        "dinner": "Chicken stew with potatoes"
                    },
                    "saturday": {
                        "breakfast": "Eggs with fried potatoes",
                        "lunch": "Leftover lentil soup",
                        "dinner": "Pasta bake with tomatoes, cheese, and onions"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Rice and beans with cabbage slaw",
                        "dinner": "Chicken stir-fry over rice"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Egg and cheese omelet",
                        "lunch": "Potato and carrot soup",
                        "dinner": "Ground beef shepherd’s pie"
                    },
                    "tuesday": {
                        "breakfast": "Peanut butter with apples",
                        "lunch": "Lentil and rice bowl",
                        "dinner": "Chicken and cabbage stir-fry"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Egg fried rice with veggies",
                        "dinner": "Spaghetti with ground beef sauce and broccoli"
                    },
                    "thursday": {
                        "breakfast": "Cheese and scrambled eggs",
                        "lunch": "Potato and onion hash",
                        "dinner": "Baked chicken thighs with rice and cabbage"
                    },
                    "friday": {
                        "breakfast": "Peanut butter toast and apples",
                        "lunch": "Lentil soup leftovers",
                        "dinner": "Ground beef and veggie chili"
                    },
                    "saturday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Fried cabbage with rice",
                        "dinner": "Pasta with cheesy tomato sauce"
                    },
                    "sunday": {
                        "breakfast": "Eggs and fried potatoes",
                        "lunch": "Chicken rice bowls",
                        "dinner": "Leftover chili with baked potatoes"
                    }
                }
            }
        },
        "80": {
            "groceries": [
                "2 lbs of ground beef",
                "1 large package of chicken thighs",
                "1 dozen eggs",
                "1 large bag of potatoes",
                "2 lbs dried pasta",
                "1 large bag of rice",
                "1 jar of pasta sauce",
                "1 large block of cheese",
                "1 bag of onions",
                "2 bell peppers",
                "1 head of lettuce",
                "1 bag of apples",
                "1 jar of salsa",
                "1 can of black beans",
                "1 can of corn",
                "1 gallon of milk"
            ],
            "meals": [
                "Spaghetti with Meat Sauce",
                "Taco Salad/Taco Bowls",
                "Chicken and Veggie Stir-Fry",
                "Ground Beef Shepherd's Pie"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Ground beef taco salad",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "tuesday": {
                        "breakfast": "Egg and potato scramble",
                        "lunch": "Black bean and corn rice bowls",
                        "dinner": "Chicken stir-fry with peppers and onions"
                    },
                    "wednesday": {
                        "breakfast": "Cheese omelet",
                        "lunch": "Taco bowls with rice, beef, and salsa",
                        "dinner": "Shepherd’s pie with mashed potatoes"
                    },
                    "thursday": {
                        "breakfast": "Peanut butter toast",
                        "lunch": "Rice and beans with salsa",
                        "dinner": "Spaghetti with meat sauce and lettuce salad"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Chicken rice bowls",
                        "dinner": "Beef taco salad with corn"
                    },
                    "saturday": {
                        "breakfast": "Eggs with fried potatoes",
                        "lunch": "Ground beef and veggie stir-fry",
                        "dinner": "Shepherd’s pie"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Black beans and rice with salsa",
                        "dinner": "Chicken stir-fry with peppers and onions"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Cheese omelet",
                        "lunch": "Rice bowls with chicken and salsa",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "tuesday": {
                        "breakfast": "Egg and potato scramble",
                        "lunch": "Beef taco bowls",
                        "dinner": "Chicken stir-fry with peppers"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Black bean and corn tacos",
                        "dinner": "Shepherd’s pie"
                    },
                    "thursday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Chicken rice bowls",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "friday": {
                        "breakfast": "Cheese omelet",
                        "lunch": "Rice and beans with salsa",
                        "dinner": "Beef taco salad"
                    },
                    "saturday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Chicken stir-fry bowls",
                        "dinner": "Shepherd’s pie with potatoes"
                    },
                    "sunday": {
                        "breakfast": "Egg and cheese scramble",
                        "lunch": "Rice and beans with corn",
                        "dinner": "Spaghetti with meat sauce and lettuce"
                    }
                }
            }
        },
        "100": {
            "groceries": [
                "2 lbs of ground beef",
                "1 package of chicken breasts",
                "1 dozen eggs",
                "1 large block of cheese",
                "1 container of yogurt",
                "1 loaf of good quality bread",
                "1 bag of tortillas",
                "1 large bag of rice",
                "2 boxes of pasta",
                "1 bag of spinach",
                "1 head of lettuce",
                "1 bag of potatoes",
                "1 bag of carrots",
                "2 bell peppers",
                "1 bag of frozen mixed vegetables",
                "1 bag of apples",
                "1 jar of pasta sauce",
                "1 jar of salsa",
                "1 gallon of milk"
            ],
            "meals": [
                "Chili",
                "Quesadillas",
                "Chicken and Rice Bowls",
                "Chicken and Veggie Stir-Fry"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Yogurt with apples",
                        "lunch": "Quesadillas with cheese and spinach",
                        "dinner": "Ground beef chili"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover chili",
                        "dinner": "Chicken and veggie stir-fry with rice"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Chicken and rice bowls with carrots",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "thursday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Taco salad with ground beef and lettuce"
                    },
                    "friday": {
                        "breakfast": "Yogurt with bananas",
                        "lunch": "Leftover taco salad",
                        "dinner": "Quesadillas with chicken and peppers"
                    },
                    "saturday": {
                        "breakfast": "Eggs and fried potatoes",
                        "lunch": "Chicken and rice bowls with salsa",
                        "dinner": "Chili with potatoes"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Leftover chili",
                        "dinner": "Chicken stir-fry with frozen veggies"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Chicken and rice bowls",
                        "dinner": "Spaghetti with meat sauce and spinach"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Taco salad with beef, lettuce, and salsa"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Quesadillas with cheese and peppers",
                        "dinner": "Chili with rice"
                    },
                    "thursday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover chili",
                        "dinner": "Chicken and veggie stir-fry"
                    },
                    "friday": {
                        "breakfast": "Yogurt with bananas",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Quesadillas with chicken and cheese"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Chicken and rice bowls",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with fruit",
                        "lunch": "Leftover spaghetti",
                        "dinner": "Taco salad with beef and all the fixings"
                    }
                }
            }
        },
        "140": {
            "groceries": [
                "2 lbs of ground beef",
                "2 lbs of chicken breasts",
                "1 pack of Italian sausage",
                "1 dozen eggs",
                "1 large block of cheese",
                "1 container of Greek yogurt",
                "1 loaf of artisan bread",
                "1 large bag of rice",
                "2 boxes of pasta",
                "1 large bag of frozen vegetables",
                "A variety of fresh produce: potatoes, onions, spinach, bell peppers, broccoli, carrots",
                "A variety of fruits: apples, bananas, berries",
                "1 large jar of pasta sauce",
                "1 jar of salsa",
                "2 gallons of milk",
                "1 large box of oatmeal",
                "1 box of cereal"
            ],
            "meals": [
                "Spaghetti with Meatballs (using Italian sausage)",
                "Chicken and Broccoli Bake",
                "Stuffed Peppers",
                "Chicken Tacos"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover sausage pasta",
                        "dinner": "Spaghetti with Italian sausage meatballs"
                    },
                    "tuesday": {
                        "breakfast": "Oatmeal with berries",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and broccoli bake"
                    },
                    "wednesday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover bake",
                        "dinner": "Stuffed bell peppers with ground beef and rice"
                    },
                    "thursday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover stuffed peppers",
                        "dinner": "Chicken tacos with salsa and lettuce"
                    },
                    "friday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover tacos",
                        "dinner": "Sausage and veggie stir-fry with rice"
                    },
                    "saturday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Chicken and rice bowls with salsa"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with fruit",
                        "lunch": "Leftover chicken and rice bowls",
                        "dinner": "Spaghetti with meat sauce and cheese"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and broccoli bake"
                    },
                    "tuesday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover bake",
                        "dinner": "Stuffed peppers with ground beef"
                    },
                    "wednesday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover stuffed peppers",
                        "dinner": "Sausage and veggie pasta"
                    },
                    "thursday": {
                        "breakfast": "Oatmeal with berries",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken tacos with lettuce and salsa"
                    },
                    "friday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover tacos",
                        "dinner": "Chicken and veggie stir-fry over rice"
                    },
                    "saturday": {
                        "breakfast": "Eggs and bacon",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Ground beef chili"
                    },
                    "sunday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover chili",
                        "dinner": "Spaghetti with meat sauce"
                    }
                }
            }
        }
    },
    "walmart": {
        "40": {
            "groceries": [
                "1 large bag of rice",
                "1 bag of dried lentils",
                "1 large bag of potatoes",
                "1 dozen eggs",
                "1 large tub of peanut butter",
                "1 loaf of store-brand bread",
                "1 bag of yellow onions",
                "1 bag of carrots",
                "1 can of diced tomatoes",
                "1 can of black beans",
                "1 gallon of milk",
                "Cooking oil and basic seasonings"
            ],
            "meals": [
                "Lentil and Rice Bowls",
                "Lentil Soup",
                "Potato and Egg Scramble",
                "Peanut Butter Sandwiches"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Oatmeal",
                        "lunch": "Lentil soup",
                        "dinner": "Beans and rice with carrots and onions"
                    },
                    "tuesday": {
                        "breakfast": "Scrambled eggs",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Potato and egg scramble"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Leftover beans and rice",
                        "dinner": "Lentil soup with potatoes"
                    },
                    "thursday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Tomato and onion pasta"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Potato hash with onions",
                        "dinner": "Black beans and rice"
                    },
                    "saturday": {
                        "breakfast": "Eggs with potatoes",
                        "lunch": "Leftover black beans and rice",
                        "dinner": "Lentil soup"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Potato and egg scramble"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Lentil soup leftovers",
                        "dinner": "Black beans and rice"
                    },
                    "tuesday": {
                        "breakfast": "Oatmeal",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Potato hash with carrots and onions"
                    },
                    "wednesday": {
                        "breakfast": "Eggs and milk",
                        "lunch": "Leftover potato hash",
                        "dinner": "Beans and rice"
                    },
                    "thursday": {
                        "breakfast": "Peanut butter toast",
                        "lunch": "Black beans and rice",
                        "dinner": "Lentil soup"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Pasta with tomato sauce"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover pasta",
                        "dinner": "Lentil and rice bowls"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Potato and egg scramble"
                    }
                }
            }
        },
        "60": {
            "groceries": [
                "1 large bag of rice",
                "1 large bag of dried beans",
                "1 package of bone-in chicken thighs",
                "1 lb of ground turkey",
                "1 dozen eggs",
                "1 block of cheese",
                "1 large bag of potatoes",
                "1 bag of carrots",
                "1 head of cabbage",
                "1 bag of onions",
                "1 bag of apples",
                "1 gallon of milk",
                "1 jar of pasta sauce"
            ],
            "meals": [
                "Chicken and Rice",
                "Pasta with Turkey Sauce",
                "Cabbage and Turkey Skillet",
                "Breakfast Burritos"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover pasta",
                        "dinner": "Pasta with turkey sauce"
                    },
                    "tuesday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Leftover turkey pasta",
                        "dinner": "Chicken and rice with carrots"
                    },
                    "wednesday": {
                        "breakfast": "Breakfast burrito",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Cabbage and turkey skillet"
                    },
                    "thursday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover skillet",
                        "dinner": "Chicken and potato soup"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Leftover soup",
                        "dinner": "Turkey and rice bowls"
                    },
                    "saturday": {
                        "breakfast": "Scrambled eggs with potatoes",
                        "lunch": "Leftover turkey bowls",
                        "dinner": "Pasta with tomato sauce and cheese"
                    },
                    "sunday": {
                        "breakfast": "Breakfast burrito",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and veggie stir-fry with rice"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Cabbage and turkey skillet"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover skillet",
                        "dinner": "Chicken and rice"
                    },
                    "wednesday": {
                        "breakfast": "Breakfast burrito",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Pasta with turkey sauce"
                    },
                    "thursday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and potato stew"
                    },
                    "friday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover stew",
                        "dinner": "Ground turkey tacos"
                    },
                    "saturday": {
                        "breakfast": "Breakfast burrito",
                        "lunch": "Leftover tacos",
                        "dinner": "Pasta bake with cheese and tomatoes"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and rice"
                    }
                }
            }
        },
        "80": {
            "groceries": [
                "1 large bag of rice",
                "1 large bag of dried beans",
                "2 lbs of ground beef",
                "1 pack of chicken breasts",
                "1 dozen eggs",
                "1 block of cheese",
                "1 loaf of bread",
                "1 large bag of potatoes",
                "1 bag of frozen mixed vegetables",
                "1 large bag of onions",
                "1 head of broccoli",
                "1 bag of apples",
                "1 gallon of milk",
                "1 large can of diced tomatoes"
            ],
            "meals": [
                "Beef and Broccoli Stir-Fry",
                "Chili",
                "Chicken and Rice Soup",
                "Baked Potatoes"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover baked potatoes",
                        "dinner": "Beef and broccoli stir-fry with rice"
                    },
                    "tuesday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Ground beef chili"
                    },
                    "wednesday": {
                        "breakfast": "Toast with jam",
                        "lunch": "Leftover chili",
                        "dinner": "Chicken and rice soup with carrots"
                    },
                    "thursday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover soup",
                        "dinner": "Baked potatoes topped with chili and cheese"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Leftover baked potatoes",
                        "dinner": "Pasta with meat sauce and veggies"
                    },
                    "saturday": {
                        "breakfast": "Scrambled eggs with veggies",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and veggie stir-fry with rice"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Chili with a side of bread"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover chili",
                        "dinner": "Beef and broccoli stir-fry"
                    },
                    "tuesday": {
                        "breakfast": "Toast with jam",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Chicken and rice soup"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Leftover soup",
                        "dinner": "Baked potatoes with cheese and beans"
                    },
                    "thursday": {
                        "breakfast": "Eggs with cheese",
                        "lunch": "Leftover potatoes",
                        "dinner": "Pasta with meat sauce"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with apples",
                        "lunch": "Leftover pasta",
                        "dinner": "Ground beef and veggie stir-fry"
                    },
                    "saturday": {
                        "breakfast": "Scrambled eggs",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Chili with rice"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Leftover chili",
                        "dinner": "Chicken and veggie stir-fry"
                    }
                }
            }
        },
        "100": {
            "groceries": [
                "2 lbs of ground beef",
                "2 lbs of chicken thighs",
                "1 dozen eggs",
                "1 large bag of frozen meatballs",
                "1 block of cheese",
                "1 tub of Greek yogurt",
                "1 bag of tortillas",
                "1 large bag of rice",
                "1 box of pasta",
                "1 jar of pasta sauce",
                "1 large bag of frozen vegetables",
                "1 bag of potatoes",
                "1 head of lettuce",
                "1 bag of carrots",
                "1 bag of bananas",
                "1 gallon of milk",
                "1 box of cereal"
            ],
            "meals": [
                "Meatball Subs or Pasta",
                "Chicken and Vegetable Soup",
                "Taco Night",
                "Chicken and Rice Bowls"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover soup",
                        "dinner": "Chicken and vegetable soup"
                    },
                    "tuesday": {
                        "breakfast": "Yogurt with bananas",
                        "lunch": "Leftover soup",
                        "dinner": "Meatball pasta"
                    },
                    "wednesday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover meatballs",
                        "dinner": "Ground beef tacos"
                    },
                    "thursday": {
                        "breakfast": "Oatmeal",
                        "lunch": "Leftover tacos",
                        "dinner": "Chicken and rice bowls with veggies"
                    },
                    "friday": {
                        "breakfast": "Yogurt with bananas",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Meatball subs"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover subs",
                        "dinner": "Pasta with meat sauce"
                    },
                    "sunday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and veggie stir-fry"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Yogurt with bananas",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Ground beef chili"
                    },
                    "tuesday": {
                        "breakfast": "Oatmeal",
                        "lunch": "Leftover chili",
                        "dinner": "Taco night"
                    },
                    "wednesday": {
                        "breakfast": "Eggs and cheese",
                        "lunch": "Leftover tacos",
                        "dinner": "Meatball pasta"
                    },
                    "thursday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and rice bowls"
                    },
                    "friday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Pasta bake with cheese and veggies"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover pasta bake",
                        "dinner": "Taco salad"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal",
                        "lunch": "Leftover taco salad",
                        "dinner": "Chicken and vegetable soup"
                    }
                }
            }
        },
        "140": {
            "groceries": [
                "3 lbs of ground beef",
                "2 lbs of chicken breasts",
                "1 pack of Italian sausage",
                "2 dozen eggs",
                "2 gallons of milk",
                "1 large block of cheese",
                "1 tub of Greek yogurt",
                "A variety of fresh produce: potatoes, onions, carrots, bell peppers, leafy greens",
                "A variety of fruits: berries, apples, bananas",
                "2 large bags of rice",
                "2 boxes of pasta",
                "1 large bag of frozen vegetables",
                "1 large jar of pasta sauce",
                "1 bag of tortilla chips",
                "1 jar of salsa",
                "1 box of cereal",
                "Snack items (e.g., granola bars, crackers)"
            ],
            "meals": [
                "Lasagna or Baked Ziti",
                "Chicken Fajitas",
                "Beef Stroganoff",
                "Breakfast for Dinner"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover fajitas",
                        "dinner": "Lasagna with ground beef and veggies"
                    },
                    "tuesday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover lasagna",
                        "dinner": "Chicken fajitas"
                    },
                    "wednesday": {
                        "breakfast": "Scrambled eggs with sausage",
                        "lunch": "Leftover fajitas",
                        "dinner": "Ground beef stroganoff with pasta"
                    },
                    "thursday": {
                        "breakfast": "Oatmeal with berries",
                        "lunch": "Leftover stroganoff",
                        "dinner": "Chicken and veggie stir-fry"
                    },
                    "friday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Pasta with sausage and peppers"
                    },
                    "saturday": {
                        "breakfast": "Pancakes or eggs and sausage",
                        "lunch": "Leftover sausage pasta",
                        "dinner": "Taco night"
                    },
                    "sunday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover tacos",
                        "dinner": "Chicken fajitas"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover fajitas",
                        "dinner": "Beef stroganoff"
                    },
                    "tuesday": {
                        "breakfast": "Oatmeal with fruit",
                        "lunch": "Leftover stroganoff",
                        "dinner": "Pasta with sausage and veggies"
                    },
                    "wednesday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and veggie stir-fry"
                    },
                    "thursday": {
                        "breakfast": "Yogurt with berries",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Taco night with ground beef"
                    },
                    "friday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover tacos",
                        "dinner": "Baked ziti with ground beef and cheese"
                    },
                    "saturday": {
                        "breakfast": "Sausage and eggs",
                        "lunch": "Leftover baked ziti",
                        "dinner": "Chicken and veggie stir-fry"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with fruit",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Beef tacos"
                    }
                }
            }
        }
    },
    "safeway": {
        "40": {
            "groceries": [
                "1 large bag of long-grain rice",
                "1 large bag of dry pinto beans",
                "2 lbs of dried pasta",
                "1 dozen eggs",
                "1 large tub of peanut butter",
                "1 loaf of store-brand sandwich bread",
                "1 large bag of russet potatoes",
                "1 large bag of yellow onions",
                "1 bag of carrots",
                "1 large can of diced tomatoes",
                "1 gallon of milk",
                "Cooking oil and basic seasonings"
            ],
            "meals": [
                "Beans and Rice",
                "Pasta with Tomato Sauce",
                "Potato and Egg Scramble",
                "Peanut Butter Sandwiches"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Beans and rice",
                        "dinner": "Pasta with tomato sauce and onions"
                    },
                    "tuesday": {
                        "breakfast": "Potato and egg scramble",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Rice and beans"
                    },
                    "wednesday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Leftover beans and rice",
                        "dinner": "Pasta with tomato sauce"
                    },
                    "thursday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover pasta",
                        "dinner": "Potato hash with carrots and onions"
                    },
                    "friday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Beans and rice"
                    },
                    "saturday": {
                        "breakfast": "Scrambled eggs with potatoes",
                        "lunch": "Leftover beans and rice",
                        "dinner": "Pasta with tomato sauce and onions"
                    },
                    "sunday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Egg and potato scramble"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover scramble",
                        "dinner": "Beans and rice"
                    },
                    "tuesday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Leftover beans and rice",
                        "dinner": "Potato hash with carrots"
                    },
                    "wednesday": {
                        "breakfast": "Eggs and milk",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Pasta with tomato sauce"
                    },
                    "thursday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Leftover pasta",
                        "dinner": "Beans and rice"
                    },
                    "friday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover beans and rice",
                        "dinner": "Potato and egg scramble"
                    },
                    "saturday": {
                        "breakfast": "Oatmeal with milk",
                        "lunch": "Peanut butter sandwich",
                        "dinner": "Pasta with tomato sauce"
                    },
                    "sunday": {
                        "breakfast": "Scrambled eggs with potatoes",
                        "lunch": "Leftover pasta",
                        "dinner": "Beans and rice"
                    }
                }
            }
        },
        "60": {
            "groceries": [
                "1 large bag of rice",
                "1 bag of dried lentils",
                "1 package of bone-in chicken thighs",
                "1 lb ground turkey",
                "1 dozen eggs",
                "1 block of store-brand cheese",
                "1 bag of potatoes",
                "1 head of cabbage",
                "1 bag of carrots",
                "1 bag of onions",
                "1 gallon of milk",
                "1 large can of diced tomatoes"
            ],
            "meals": [
                "Lentil Soup",
                "Chicken and Rice with Cabbage",
                "Pasta with Ground Turkey Sauce",
                "Egg and Cheese Burritos"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover pasta",
                        "dinner": "Pasta with ground turkey sauce"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and milk",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and rice with carrots"
                    },
                    "wednesday": {
                        "breakfast": "Egg and cheese burritos",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Lentil soup with potatoes and onions"
                    },
                    "thursday": {
                        "breakfast": "Scrambled eggs",
                        "lunch": "Leftover lentil soup",
                        "dinner": "Ground turkey and cabbage skillet"
                    },
                    "friday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover skillet",
                        "dinner": "Chicken and potato stew"
                    },
                    "saturday": {
                        "breakfast": "Eggs and cheese",
                        "lunch": "Leftover stew",
                        "dinner": "Pasta bake with cheese and tomatoes"
                    },
                    "sunday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover pasta bake",
                        "dinner": "Lentil soup"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Eggs and cheese burritos",
                        "lunch": "Leftover lentil soup",
                        "dinner": "Chicken and rice with veggies"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and milk",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Ground turkey pasta"
                    },
                    "wednesday": {
                        "breakfast": "Scrambled eggs",
                        "lunch": "Leftover pasta",
                        "dinner": "Lentil and rice bowls with carrots"
                    },
                    "thursday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover bowls",
                        "dinner": "Ground turkey and cabbage stir-fry"
                    },
                    "friday": {
                        "breakfast": "Eggs and cheese",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Chicken and potato stew"
                    },
                    "saturday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover stew",
                        "dinner": "Pasta with tomatoes and cheese"
                    },
                    "sunday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and rice with cabbage"
                    }
                }
            }
        },
        "80": {
            "groceries": [
                "2 lbs of ground beef",
                "1 large package of chicken thighs",
                "1 dozen eggs",
                "1 block of cheese",
                "1 large bag of potatoes",
                "1 bag of apples",
                "1 bag of carrots",
                "1 bag of onions",
                "1 large can of diced tomatoes",
                "1 can of black beans",
                "1 can of corn",
                "1 gallon of milk",
                "1 large bag of rice",
                "1 box of pasta"
            ],
            "meals": [
                "Chili",
                "Chicken and Veggie Sheet Pan Dinner",
                "Spaghetti and Meat Sauce",
                "Black Bean Tostadas"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover chili",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "tuesday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and veggie sheet pan dinner"
                    },
                    "wednesday": {
                        "breakfast": "Eggs with milk",
                        "lunch": "Leftover sheet pan dinner",
                        "dinner": "Black bean tostadas with corn and cheese"
                    },
                    "thursday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover tostadas",
                        "dinner": "Ground beef chili"
                    },
                    "friday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover chili",
                        "dinner": "Chicken and rice bowls with carrots"
                    },
                    "saturday": {
                        "breakfast": "Eggs and cheese",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "sunday": {
                        "breakfast": "Eggs with potatoes",
                        "lunch": "Leftover pasta",
                        "dinner": "Chili with rice"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover chili",
                        "dinner": "Chicken and veggie sheet pan dinner"
                    },
                    "tuesday": {
                        "breakfast": "Eggs with milk",
                        "lunch": "Leftover sheet pan dinner",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "wednesday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover pasta",
                        "dinner": "Black bean tostadas"
                    },
                    "thursday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover tostadas",
                        "dinner": "Chili"
                    },
                    "friday": {
                        "breakfast": "Eggs with cheese",
                        "lunch": "Leftover chili",
                        "dinner": "Chicken and rice bowls"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover bowls",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "sunday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken and veggie sheet pan dinner"
                    }
                }
            }
        },
        "100": {
            "groceries": [
                "2 lbs of ground beef",
                "1 large package of chicken breasts",
                "1 dozen eggs",
                "1 large block of cheese",
                "1 tub of Greek yogurt",
                "1 loaf of bread",
                "1 bag of tortillas",
                "1 large bag of rice",
                "1 box of pasta",
                "1 bag of spinach",
                "1 head of lettuce",
                "1 bag of apples",
                "2 bell peppers",
                "1 bag of frozen mixed vegetables",
                "1 large jar of pasta sauce",
                "1 jar of salsa",
                "1 gallon of milk"
            ],
            "meals": [
                "Chicken Fajitas",
                "Spaghetti with Meat Sauce",
                "Chicken and Rice Bowls",
                "Taco Night"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Yogurt with apples",
                        "lunch": "Leftover pasta",
                        "dinner": "Chicken fajitas with rice"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover fajitas",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "wednesday": {
                        "breakfast": "Yogurt with spinach smoothie",
                        "lunch": "Leftover pasta",
                        "dinner": "Taco night with ground beef, lettuce, and cheese"
                    },
                    "thursday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover tacos",
                        "dinner": "Chicken and rice bowls with veggies"
                    },
                    "friday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover spaghetti",
                        "dinner": "Chicken fajitas"
                    },
                    "sunday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover fajitas",
                        "dinner": "Taco salad"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover salad",
                        "dinner": "Chicken and rice bowls with veggies"
                    },
                    "tuesday": {
                        "breakfast": "Yogurt with apples",
                        "lunch": "Leftover bowls",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "wednesday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover spaghetti",
                        "dinner": "Taco night"
                    },
                    "thursday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover tacos",
                        "dinner": "Chicken fajitas"
                    },
                    "friday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover fajitas",
                        "dinner": "Chicken and rice bowls with spinach"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover chicken and rice",
                        "dinner": "Taco salad"
                    },
                    "sunday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover salad",
                        "dinner": "Spaghetti with meat sauce"
                    }
                }
            }
        },
        "140": {
            "groceries": [
                "2 lbs of ground beef",
                "2 lbs of chicken breasts",
                "1 package of Italian sausage",
                "2 dozen eggs",
                "2 gallons of milk",
                "1 large block of cheese",
                "1 container of Greek yogurt",
                "1 loaf of artisan bread",
                "1 large bag of rice",
                "2 boxes of pasta",
                "1 large bag of frozen vegetables",
                "A variety of fresh produce: potatoes, onions, carrots, bell peppers, spinach",
                "A variety of fruits: apples, bananas, berries",
                "1 large jar of pasta sauce",
                "1 bag of tortilla chips",
                "1 jar of salsa",
                "1 box of cereal"
            ],
            "meals": [
                "Sausage and Peppers",
                "Chicken and Veggie Stir-Fry",
                "Homemade Pizza Night",
                "Taco Night"
            ],
            "mealplan": {
                "week1": {
                    "monday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover pasta",
                        "dinner": "Sausage and pepper pasta"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover sausage pasta",
                        "dinner": "Chicken and veggie stir-fry with rice"
                    },
                    "wednesday": {
                        "breakfast": "Yogurt with berries",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Homemade pizza with sausage and cheese"
                    },
                    "thursday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover pizza",
                        "dinner": "Taco night with ground beef and all the fixings"
                    },
                    "friday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover tacos",
                        "dinner": "Chicken and veggie stir-fry"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Sausage and pepper skillet with cheese"
                    },
                    "sunday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover sausage skillet",
                        "dinner": "Spaghetti with meat sauce"
                    }
                },
                "week2": {
                    "monday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover spaghetti",
                        "dinner": "Chicken and veggie stir-fry"
                    },
                    "tuesday": {
                        "breakfast": "Eggs and toast",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Taco night"
                    },
                    "wednesday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover tacos",
                        "dinner": "Sausage and pepper pasta"
                    },
                    "thursday": {
                        "breakfast": "Scrambled eggs with cheese",
                        "lunch": "Leftover sausage pasta",
                        "dinner": "Spaghetti with meat sauce"
                    },
                    "friday": {
                        "breakfast": "Cereal with milk",
                        "lunch": "Leftover spaghetti",
                        "dinner": "Chicken and veggie stir-fry"
                    },
                    "saturday": {
                        "breakfast": "Eggs and potatoes",
                        "lunch": "Leftover stir-fry",
                        "dinner": "Taco night"
                    },
                    "sunday": {
                        "breakfast": "Yogurt with fruit",
                        "lunch": "Leftover tacos",
                        "dinner": "Sausage and pepper skillet"
                    }
                }
            }
        }
    }
}


# Welcome message and store selection
@bot.command(name='frys')
async def frys_budget(ctx, budget: str):
    budget_key = budget.lstrip('$')
    if budget_key in stores['frys']:
        store_data = stores['frys'][budget_key]
        
        # Split the response into two parts
        groceries_message = f"**Fry's ${budget_key} Shopping List:**\n"
        groceries_message += "\n".join([f"- {item}" for item in store_data['groceries']])
        
        mealplan_message = "**Weekly Meal Plan:**\n"
        for week, days in store_data['mealplan'].items():
            mealplan_message += f"**{week.capitalize()}:**\n"
            for day, meals in days.items():
                mealplan_message += f"  - **{day.capitalize()}:**\n"
                mealplan_message += f"    - Breakfast: {meals['breakfast']}\n"
                mealplan_message += f"    - Lunch: {meals['lunch']}\n"
                mealplan_message += f"    - Dinner: {meals['dinner']}\n"

        await ctx.send(groceries_message)
        await ctx.send(mealplan_message)
    else:
        await ctx.send("Sorry, that's not a valid budget option for Fry's. Please choose from $40, $60, $80, $100, or $140.")

@bot.command(name='walmart')
async def walmart_budget(ctx, budget: str):
    budget_key = budget.lstrip('$')
    if budget_key in stores['walmart']:
        store_data = stores['walmart'][budget_key]

        groceries_message = f"**Walmart ${budget_key} Shopping List:**\n"
        groceries_message += "\n".join([f"- {item}" for item in store_data['groceries']])
        
        mealplan_message = "**Weekly Meal Plan:**\n"
        for week, days in store_data['mealplan'].items():
            mealplan_message += f"**{week.capitalize()}:**\n"
            for day, meals in days.items():
                mealplan_message += f"  - **{day.capitalize()}:**\n"
                mealplan_message += f"    - Breakfast: {meals['breakfast']}\n"
                mealplan_message += f"    - Lunch: {meals['lunch']}\n"
                mealplan_message += f"    - Dinner: {meals['dinner']}\n"
        
        await ctx.send(groceries_message)
        await ctx.send(mealplan_message)
    else:
        await ctx.send("Sorry, that's not a valid budget option for Walmart. Please choose from $40, $60, $80, $100, or $140.")

@bot.command(name='safeway')
async def safeway_budget(ctx, budget: str):
    budget_key = budget.lstrip('$')
    if budget_key in stores['safeway']:
        store_data = stores['safeway'][budget_key]
        
        groceries_message = f"**Safeway ${budget_key} Shopping List:**\n"
        groceries_message += "\n".join([f"- {item}" for item in store_data['groceries']])
        
        mealplan_message = "**Weekly Meal Plan:**\n"
        for week, days in store_data['mealplan'].items():
            mealplan_message += f"**{week.capitalize()}**\n"
            for day, meals in days.items():
                mealplan_message += f"  - **{day.capitalize()}:**\n"
                mealplan_message += f"    - Breakfast: {meals['breakfast']}\n"
                mealplan_message += f"    - Lunch: {meals['lunch']}\n"
                mealplan_message += f"    - Dinner: {meals['dinner']}\n"
        
        await ctx.send(groceries_message)
        await ctx.send(mealplan_message)
    else:
        await ctx.send("Sorry, that's not a valid budget option for Safeway. Please choose from $40, $60, $80, $100, or $140.")


bot.run('redacted')
