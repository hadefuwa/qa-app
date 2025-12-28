from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Quiz data structure - each quiz has its own sections, reading material, and answers
quizzes = {
    'vikings': {
        'name': 'Vikings',
        'title': 'Vikings Quiz',
        'description': 'Learn about brave explorers, skilled sailors, and fierce warriors!',
        'emoji': '⚔️',
        'difficulty': 'easy',
        'total_questions': 30,
        'sections': {
            1: {
                'title': 'Part 1: Who Were the Vikings?',
                'questions': [
                    {
                        'number': 1,
                        'text': 'Where did the Vikings come from?',
                        'options': [
                            {'letter': 'A', 'text': 'The jungle'},
                            {'letter': 'B', 'text': 'Scandinavia (countries like Norway and Sweden)'},
                            {'letter': 'C', 'text': 'The desert'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'About how long ago did the Vikings live?',
                        'options': [
                            {'letter': 'A', 'text': '1,000 years ago'},
                            {'letter': 'B', 'text': '100 years ago'},
                            {'letter': 'C', 'text': '10 years ago'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'What was the main job for most Vikings?',
                        'options': [
                            {'letter': 'A', 'text': 'Astronauts'},
                            {'letter': 'B', 'text': 'Farmers'},
                            {'letter': 'C', 'text': 'Zoo keepers'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'What were Viking letters and writing called?',
                        'options': [
                            {'letter': 'A', 'text': 'ABCs'},
                            {'letter': 'B', 'text': 'Runes'},
                            {'letter': 'C', 'text': 'Scribbles'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'Where did Vikings usually carve their writing?',
                        'options': [
                            {'letter': 'A', 'text': 'On paper'},
                            {'letter': 'B', 'text': 'On stones and wood'},
                            {'letter': 'C', 'text': 'On computer screens'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'What did Vikings use to buy things before they had coins?',
                        'options': [
                            {'letter': 'A', 'text': 'Credit cards'},
                            {'letter': 'B', 'text': 'Silver jewelry (often cut into pieces)'},
                            {'letter': 'C', 'text': 'Paper money'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: Viking Homes and Daily Life',
                'questions': [
                    {
                        'number': 7,
                        'text': 'What were Viking houses called?',
                        'options': [
                            {'letter': 'A', 'text': 'Castles'},
                            {'letter': 'B', 'text': 'Longhouses'},
                            {'letter': 'C', 'text': 'Igloos'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'What were most Viking houses made out of?',
                        'options': [
                            {'letter': 'A', 'text': 'Wood, stone, or turf (grass and dirt)'},
                            {'letter': 'B', 'text': 'Bricks and cement'},
                            {'letter': 'C', 'text': 'Ice'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'Where was the fire usually placed in a Viking house?',
                        'options': [
                            {'letter': 'A', 'text': 'In the fireplace by the wall'},
                            {'letter': 'B', 'text': 'In the middle of the room on the floor'},
                            {'letter': 'C', 'text': 'Outside in the garden'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What material were Viking clothes mostly made from?',
                        'options': [
                            {'letter': 'A', 'text': 'Plastic'},
                            {'letter': 'B', 'text': 'Wool and linen'},
                            {'letter': 'C', 'text': 'Silk'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'What did Viking children do for fun?',
                        'options': [
                            {'letter': 'A', 'text': 'Played video games'},
                            {'letter': 'B', 'text': 'Played board games and wrestled'},
                            {'letter': 'C', 'text': 'Watched TV'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'Which of these animals did Vikings keep on their farms?',
                        'options': [
                            {'letter': 'A', 'text': 'Elephants'},
                            {'letter': 'B', 'text': 'Pigs, sheep, and chickens'},
                            {'letter': 'C', 'text': 'Tigers'}
                        ]
                    },
                    {
                        'number': 13,
                        'text': 'What did Vikings eat a lot of?',
                        'options': [
                            {'letter': 'A', 'text': 'Pizza and burgers'},
                            {'letter': 'B', 'text': 'Fish and meat stew'},
                            {'letter': 'C', 'text': 'Tacos'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Part 3: Ships and Travel',
                'questions': [
                    {
                        'number': 14,
                        'text': 'What were the famous Viking boats called?',
                        'options': [
                            {'letter': 'A', 'text': 'Speedboats'},
                            {'letter': 'B', 'text': 'Longships'},
                            {'letter': 'C', 'text': 'Canoes'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What scary animal head was often carved on the front of a Viking ship?',
                        'options': [
                            {'letter': 'A', 'text': 'A dragon or snake'},
                            {'letter': 'B', 'text': 'A bunny rabbit'},
                            {'letter': 'C', 'text': 'A horse'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'Why did they put dragon heads on their ships?',
                        'options': [
                            {'letter': 'A', 'text': 'To look pretty'},
                            {'letter': 'B', 'text': 'To scare away enemies and sea monsters'},
                            {'letter': 'C', 'text': 'To help the boat float'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'How did Viking ships move across the water?',
                        'options': [
                            {'letter': 'A', 'text': 'With a motor'},
                            {'letter': 'B', 'text': 'Using sails and oars (rowing)'},
                            {'letter': 'C', 'text': 'By swimming behind it'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'Vikings were great explorers. Which faraway place did they reach before Christopher Columbus?',
                        'options': [
                            {'letter': 'A', 'text': 'North America'},
                            {'letter': 'B', 'text': 'Australia'},
                            {'letter': 'C', 'text': 'The Moon'}
                        ]
                    },
                    {
                        'number': 19,
                        'text': 'How did Vikings find their way at sea?',
                        'options': [
                            {'letter': 'A', 'text': 'They used a GPS'},
                            {'letter': 'B', 'text': 'They looked at the sun, stars, and birds'},
                            {'letter': 'C', 'text': 'They asked for directions'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Part 4: Warriors and Weapons',
                'questions': [
                    {
                        'number': 20,
                        'text': 'Did real Viking helmets have horns on them?',
                        'options': [
                            {'letter': 'A', 'text': 'Yes, always'},
                            {'letter': 'B', 'text': 'No, never (that is just a myth!)'},
                            {'letter': 'C', 'text': 'Only on Tuesdays'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'What was the Viking\'s most common weapon?',
                        'options': [
                            {'letter': 'A', 'text': 'A laser sword'},
                            {'letter': 'B', 'text': 'An axe or a spear'},
                            {'letter': 'C', 'text': 'A water gun'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What did Vikings use to protect themselves in a fight?',
                        'options': [
                            {'letter': 'A', 'text': 'A round wooden shield'},
                            {'letter': 'B', 'text': 'An umbrella'},
                            {'letter': 'C', 'text': 'A pillow'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'What was a "Shield Wall"?',
                        'options': [
                            {'letter': 'A', 'text': 'A wall made of bricks'},
                            {'letter': 'B', 'text': 'When warriors stood close together with shields overlapping'},
                            {'letter': 'C', 'text': 'A painting of a shield on a wall'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'What were the very fierce Viking warriors called?',
                        'options': [
                            {'letter': 'A', 'text': 'Berserkers'},
                            {'letter': 'B', 'text': 'Ninjas'},
                            {'letter': 'C', 'text': 'Knights'}
                        ]
                    }
                ]
            },
            5: {
                'title': 'Part 5: Gods and Legends',
                'questions': [
                    {
                        'number': 25,
                        'text': 'Who was the Viking god of thunder?',
                        'options': [
                            {'letter': 'A', 'text': 'Spider-Man'},
                            {'letter': 'B', 'text': 'Thor'},
                            {'letter': 'C', 'text': 'Zeus'}
                        ]
                    },
                    {
                        'number': 26,
                        'text': 'What weapon did Thor carry?',
                        'options': [
                            {'letter': 'A', 'text': 'A magic hammer'},
                            {'letter': 'B', 'text': 'A magic wand'},
                            {'letter': 'C', 'text': 'A bow and arrow'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'Who was the king of all the Viking gods?',
                        'options': [
                            {'letter': 'A', 'text': 'Odin'},
                            {'letter': 'B', 'text': 'Loki'},
                            {'letter': 'C', 'text': 'Freya'}
                        ]
                    },
                    {
                        'number': 28,
                        'text': 'How many eyes did Odin have?',
                        'options': [
                            {'letter': 'A', 'text': 'Two'},
                            {'letter': 'B', 'text': 'One (he traded the other for wisdom)'},
                            {'letter': 'C', 'text': 'Three'}
                        ]
                    },
                    {
                        'number': 29,
                        'text': 'What was the name of the place where brave warriors went after they died?',
                        'options': [
                            {'letter': 'A', 'text': 'Valhalla'},
                            {'letter': 'B', 'text': 'Hogwarts'},
                            {'letter': 'C', 'text': 'Disneyland'}
                        ]
                    },
                    {
                        'number': 30,
                        'text': 'Which day of the week is named after the god Thor?',
                        'options': [
                            {'letter': 'A', 'text': 'Monday'},
                            {'letter': 'B', 'text': 'Wednesday'},
                            {'letter': 'C', 'text': 'Thursday (Thor\'s Day)'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {
            1: """
                <h2>Who Were the Vikings? 🏰</h2>
                <p>The Vikings were amazing people who lived about 1,000 years ago! They came from a place called <strong>Scandinavia</strong>, which includes the countries we now call Norway, Sweden, and Denmark. These lands were very cold with lots of forests, mountains, and beautiful fjords (deep water inlets).</p>
                
                <p>Most Vikings were actually <strong>farmers</strong>! They grew crops like barley, oats, and rye. They also raised animals like cows, sheep, pigs, and chickens. Farming was hard work, but it was how most Viking families got their food.</p>
                
                <p>Vikings had their own special way of writing called <strong>runes</strong>. These were special letters carved into stones, wood, and metal. Runes were not just for writing messages - they were also used for magic and telling fortunes! Vikings believed that runes had special powers.</p>
                
                <p>Before Vikings had coins like we do today, they used <strong>silver</strong> to buy things. They would cut pieces of silver jewelry or coins into smaller pieces to pay for items. This was called "hack silver" because they would hack (cut) the silver into the right size!</p>
                
                <p>The Viking Age lasted from about 793 AD to 1066 AD. During this time, Vikings explored, traded, and settled in many places across Europe and even reached North America!</p>
            """,
            2: """
                <h2>Viking Homes and Daily Life 🏠</h2>
                <p>Viking families lived in houses called <strong>longhouses</strong>. These were long, rectangular buildings that could be up to 250 feet long! The name "longhouse" makes perfect sense - they were very long!</p>
                
                <p>Longhouses were built from materials found nearby: <strong>wood, stone, and turf</strong> (grass and dirt). The walls were often made of wood planks or stone, and the roof was covered with turf or thatch (straw). This kept the house warm in the cold Scandinavian winters.</p>
                
                <p>Inside a longhouse, there was usually one big room where the whole family lived together. The fire was placed <strong>in the middle of the room</strong> on the floor. This fire was used for cooking, heating, and light. There was a hole in the roof to let the smoke out, but the house was often smoky inside!</p>
                
                <p>Viking clothes were made from <strong>wool and linen</strong>. Wool came from sheep, and linen came from flax plants. Vikings were skilled at spinning, weaving, and sewing. They made warm clothes to survive the cold winters. Both men and women wore tunics, and they often decorated their clothes with colorful patterns.</p>
                
                <p>Viking children had fun in many ways! They played <strong>board games</strong> like hnefatafl (a strategy game), and they loved to <strong>wrestle</strong> and play physical games. They also helped with chores like feeding animals, gathering firewood, and learning skills from their parents.</p>
                
                <p>Viking farms were busy places! They kept animals like <strong>pigs, sheep, and chickens</strong>. These animals provided food (meat, eggs, milk) and materials (wool, leather). Vikings also grew vegetables and fruits in their gardens.</p>
                
                <p>For meals, Vikings ate a lot of <strong>fish and meat stew</strong>. They also ate bread, cheese, vegetables, and fruits. They preserved food by drying, salting, or smoking it so they could eat it during the long winter months when fresh food wasn't available.</p>
            """,
            3: """
                <h2>Ships and Travel ⚓</h2>
                <p>Vikings were famous for their amazing ships called <strong>longships</strong>! These were incredible boats that could sail across oceans and also travel up shallow rivers. Longships were long and narrow, with beautiful curved ends that looked like a dragon's head and tail.</p>
                
                <p>The front of a Viking ship often had a <strong>dragon or snake head</strong> carved into it. This wasn't just for decoration - Vikings believed it would <strong>scare away enemies and sea monsters</strong>! When they came to peaceful places, they would remove the dragon head so people wouldn't be frightened.</p>
                
                <p>Viking ships moved using <strong>sails and oars</strong>. When there was wind, they would raise their big square sail. When there was no wind or they needed more speed, they would row with long oars. Some longships had up to 60 oarsmen!</p>
                
                <p>Vikings were incredible explorers! They traveled to many places including England, Ireland, France, Russia, and even <strong>North America</strong> - about 500 years before Christopher Columbus! A Viking explorer named Leif Erikson is believed to have reached North America around the year 1000 AD.</p>
                
                <p>How did Vikings find their way across the vast ocean without GPS or modern maps? They were expert navigators who used <strong>the sun, stars, and birds</strong> to guide them. They watched the position of the sun during the day and the stars at night. They also paid attention to birds - if they saw certain birds, they knew land was nearby!</p>
                
                <p>Viking ships were so well-built that they could handle rough seas and storms. The Vikings' skill at shipbuilding and navigation made them some of the greatest sailors of their time!</p>
            """,
            4: """
                <h2>Warriors and Weapons ⚔️</h2>
                <p>You might have seen pictures of Vikings with horns on their helmets, but here's a fun fact: <strong>real Viking helmets never had horns!</strong> This is just a myth that started much later. Real Viking helmets were simple, round, and made of iron or leather. They were designed to protect the head, not to look scary!</p>
                
                <p>The most common Viking weapons were <strong>axes and spears</strong>. Axes were useful because they could be used for chopping wood and also for fighting. Spears were long and could be thrown or used to stab enemies from a distance. Some Vikings also used swords, but these were expensive and only wealthy warriors could afford them.</p>
                
                <p>To protect themselves in battle, Vikings used <strong>round wooden shields</strong>. These shields were usually painted with bright colors and patterns. They were strong enough to block attacks, and Vikings were very skilled at using them!</p>
                
                <p>One famous Viking battle tactic was called the <strong>"Shield Wall"</strong>. Warriors would stand close together with their shields overlapping, creating a wall of protection. This made it very hard for enemies to break through! The shield wall was like a moving fortress.</p>
                
                <p>The most fierce Viking warriors were called <strong>Berserkers</strong>. These warriors were known for fighting with incredible strength and fearlessness. The word "berserker" might come from wearing bear skins, and they were said to fight like wild animals! However, most Vikings were actually farmers and traders, not warriors.</p>
                
                <p>Vikings didn't always fight - they were also great traders and explorers. But when they did need to defend themselves or their families, they were very skilled and brave warriors!</p>
            """,
            5: """
                <h2>Gods and Legends 🌩️</h2>
                <p>Vikings believed in many powerful gods and goddesses who lived in a place called Asgard. These stories are called <strong>Norse mythology</strong>, and they are full of exciting adventures!</p>
                
                <p>The most famous Viking god was <strong>Thor</strong>, the god of thunder. Thor was incredibly strong and carried a magical hammer called Mjölnir. When Thor threw his hammer, it would always return to his hand like a boomerang! Thor used his hammer to protect both gods and humans from giants and monsters. The sound of thunder was said to be Thor's hammer striking!</p>
                
                <p>The king of all the Viking gods was <strong>Odin</strong>. Odin was the god of wisdom, war, and poetry. He was very wise because he made a great sacrifice - he gave up one of his eyes to drink from a magical well of knowledge! So Odin had only <strong>one eye</strong>, but he gained incredible wisdom. Odin also had two ravens named Huginn (thought) and Muninn (memory) who would fly around the world and tell him everything that was happening.</p>
                
                <p>When brave Viking warriors died in battle, they believed they would go to a special place called <strong>Valhalla</strong>. This was a magnificent hall in Asgard where warriors would feast and train for the final battle. It was a great honor to go to Valhalla!</p>
                
                <p>Did you know that some of our days of the week are named after Viking gods? <strong>Thursday</strong> is named after Thor (Thor's Day)! Wednesday is named after Odin (Woden's Day), and Tuesday is named after Tyr, another Viking god. The Vikings' influence is still with us today!</p>
                
                <p>Viking mythology is full of amazing stories about gods, giants, dragons, and magical creatures. These stories were passed down through generations and helped explain the world around them. They believed their gods controlled things like the weather, the harvest, and even their luck in battle!</p>
            """
        },
        'correct_answers': {
            1: 'B', 2: 'A', 3: 'B', 4: 'B', 5: 'B', 6: 'B',
            7: 'B', 8: 'A', 9: 'B', 10: 'B', 11: 'B', 12: 'B', 13: 'B',
            14: 'B', 15: 'A', 16: 'B', 17: 'B', 18: 'A', 19: 'B',
            20: 'B', 21: 'B', 22: 'A', 23: 'B', 24: 'A',
            25: 'B', 26: 'A', 27: 'A', 28: 'B', 29: 'A', 30: 'C'
        }
    },
    'viking-shields': {
        'name': 'Viking Shields',
        'title': 'Viking Shields Quiz',
        'description': 'Discover how Viking shields were made, decorated, and used in battle!',
        'emoji': '🛡️',
        'difficulty': 'easy',
        'total_questions': 24,
        'sections': {
            1: {
                'title': 'Part 1: What Were Viking Shields Made Of?',
                'questions': [
                    {
                        'number': 1,
                        'text': 'What was the main material used to make Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Metal'},
                            {'letter': 'B', 'text': 'Wood'},
                            {'letter': 'C', 'text': 'Plastic'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'What type of wood was most commonly used for Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Oak, pine, or linden (lime wood)'},
                            {'letter': 'B', 'text': 'Bamboo'},
                            {'letter': 'C', 'text': 'Cedar'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'How thick were most Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'About 1 inch (2-3 cm) thick'},
                            {'letter': 'B', 'text': 'As thin as paper'},
                            {'letter': 'C', 'text': 'As thick as a tree trunk'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'What was placed on the front of the shield to make it stronger?',
                        'options': [
                            {'letter': 'A', 'text': 'A layer of leather'},
                            {'letter': 'B', 'text': 'A metal boss (round center piece)'},
                            {'letter': 'C', 'text': 'A sticker'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'What was the metal boss on a Viking shield used for?',
                        'options': [
                            {'letter': 'A', 'text': 'Just decoration'},
                            {'letter': 'B', 'text': 'Protection and to hold the shield together'},
                            {'letter': 'C', 'text': 'To make it shiny'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'What was the handle on a Viking shield usually made from?',
                        'options': [
                            {'letter': 'A', 'text': 'Plastic'},
                            {'letter': 'B', 'text': 'Leather or wood'},
                            {'letter': 'C', 'text': 'Rubber'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: How Were Shields Built?',
                'questions': [
                    {
                        'number': 7,
                        'text': 'How were the wooden planks for a shield usually arranged?',
                        'options': [
                            {'letter': 'A', 'text': 'Glued together side by side'},
                            {'letter': 'B', 'text': 'Planks placed together and held with glue or nails'},
                            {'letter': 'C', 'text': 'Carved from one big piece of wood'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'What shape were most Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Square'},
                            {'letter': 'B', 'text': 'Round'},
                            {'letter': 'C', 'text': 'Triangle'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'How big were Viking shields usually?',
                        'options': [
                            {'letter': 'A', 'text': 'About 2-3 feet (60-90 cm) across'},
                            {'letter': 'B', 'text': 'As big as a door'},
                            {'letter': 'C', 'text': 'As small as a plate'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What was sometimes added to the edge of a shield?',
                        'options': [
                            {'letter': 'A', 'text': 'A leather rim to protect the edges'},
                            {'letter': 'B', 'text': 'Spikes'},
                            {'letter': 'C', 'text': 'Bells'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'Why did Vikings make their shields from wood instead of metal?',
                        'options': [
                            {'letter': 'A', 'text': 'Wood was lighter and easier to carry'},
                            {'letter': 'B', 'text': 'They didn\'t know how to work metal'},
                            {'letter': 'C', 'text': 'Metal was too expensive'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'How long did it take to make a Viking shield?',
                        'options': [
                            {'letter': 'A', 'text': 'A skilled craftsman could make one in a few days'},
                            {'letter': 'B', 'text': 'One hour'},
                            {'letter': 'C', 'text': 'One year'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Part 3: Shield Decoration and Designs',
                'questions': [
                    {
                        'number': 13,
                        'text': 'What did Vikings use to paint their shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Markers'},
                            {'letter': 'B', 'text': 'Natural paints made from plants, minerals, and animal products'},
                            {'letter': 'C', 'text': 'Spray paint'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'What colors were commonly used on Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Red, yellow, black, and white'},
                            {'letter': 'B', 'text': 'Only blue'},
                            {'letter': 'C', 'text': 'Rainbow colors'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What patterns were often painted on Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Spirals, circles, and geometric shapes'},
                            {'letter': 'B', 'text': 'Cartoon characters'},
                            {'letter': 'C', 'text': 'Flowers and butterflies'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'Why did Vikings decorate their shields?',
                        'options': [
                            {'letter': 'A', 'text': 'To show which group they belonged to and to look impressive'},
                            {'letter': 'B', 'text': 'To make them lighter'},
                            {'letter': 'C', 'text': 'To hide scratches'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'What symbol was sometimes painted on shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Runes (Viking letters) or family symbols'},
                            {'letter': 'B', 'text': 'Emojis'},
                            {'letter': 'C', 'text': 'Modern logos'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'Were all Viking shields decorated the same way?',
                        'options': [
                            {'letter': 'A', 'text': 'No, each shield was unique'},
                            {'letter': 'B', 'text': 'Yes, they all looked the same'},
                            {'letter': 'C', 'text': 'Only some had decorations'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Part 4: Using Shields in Battle',
                'questions': [
                    {
                        'number': 19,
                        'text': 'How did Vikings hold their shields?',
                        'options': [
                            {'letter': 'A', 'text': 'With one hand using a handle on the back'},
                            {'letter': 'B', 'text': 'With both hands'},
                            {'letter': 'C', 'text': 'On their head'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'What was a "Shield Wall"?',
                        'options': [
                            {'letter': 'A', 'text': 'A wall made of bricks'},
                            {'letter': 'B', 'text': 'Warriors standing close together with shields overlapping'},
                            {'letter': 'C', 'text': 'Shields hanging on a wall'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'Could Viking shields be used to attack as well as defend?',
                        'options': [
                            {'letter': 'A', 'text': 'Yes, the metal boss could be used to punch'},
                            {'letter': 'B', 'text': 'No, they were only for blocking'},
                            {'letter': 'C', 'text': 'Only on Tuesdays'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What happened to shields during battle?',
                        'options': [
                            {'letter': 'A', 'text': 'They could get damaged, broken, or lost'},
                            {'letter': 'B', 'text': 'They never got damaged'},
                            {'letter': 'C', 'text': 'They turned into swords'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'How did Vikings carry their shields when not fighting?',
                        'options': [
                            {'letter': 'A', 'text': 'On their back or slung over their shoulder'},
                            {'letter': 'B', 'text': 'In their pocket'},
                            {'letter': 'C', 'text': 'They left them at home'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'Why were shields so important to Viking warriors?',
                        'options': [
                            {'letter': 'A', 'text': 'They were the main protection in battle'},
                            {'letter': 'B', 'text': 'They looked cool'},
                            {'letter': 'C', 'text': 'They were used as plates for eating'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {
            1: """
                <h2>What Were Viking Shields Made Of? 🛡️</h2>
                <p>Viking shields were mostly made from <strong>wood</strong>! This might surprise you, but wood was actually a great choice for shields. The Vikings used strong types of wood like <strong>oak, pine, or linden</strong> (also called lime wood). These woods were tough enough to protect warriors but light enough to carry easily.</p>
                
                <p>Most Viking shields were about <strong>1 inch (2-3 cm) thick</strong>. This was thick enough to stop arrows and sword strikes, but not so thick that it was too heavy to use in battle. The shields were made from wooden planks that were carefully fitted together.</p>
                
                <p>On the front of every shield, there was a special metal piece called a <strong>boss</strong>. This was a round, dome-shaped piece of iron or bronze that sat in the center. The boss wasn't just for decoration - it helped hold the shield together and protected the warrior's hand! It also made the shield stronger and could even be used to push or punch enemies.</p>
                
                <p>The handle on the back of the shield was usually made from <strong>leather or wood</strong>. It was attached to the shield so warriors could hold it firmly with one hand, leaving their other hand free to use a weapon like a sword or axe.</p>
            """,
            2: """
                <h2>How Were Shields Built? 🔨</h2>
                <p>Making a Viking shield was skilled work! Craftsmen would start by taking wooden planks and fitting them together. The planks were usually <strong>glued together or held with small nails</strong>. Sometimes they were also bound with leather strips to make them extra strong.</p>
                
                <p>Most Viking shields were <strong>round</strong>, which made them perfect for protecting the body. They were usually about <strong>2-3 feet (60-90 cm) across</strong> - big enough to cover most of a warrior's body, but not so big that they were hard to move around.</p>
                
                <p>To protect the edges of the shield from splitting, Vikings sometimes added a <strong>leather rim</strong> around the edge. This leather band helped keep the wood from cracking when the shield was hit by weapons. It also made the shield last longer!</p>
                
                <p>Vikings chose wood over metal for shields because <strong>wood was much lighter</strong>. A metal shield would be too heavy to carry and use effectively in battle. Wood shields were strong enough to protect warriors but light enough that they could be moved quickly to block attacks.</p>
                
                <p>A skilled craftsman could make a shield in just <strong>a few days</strong>. This was important because shields could break in battle, so warriors needed to be able to get new ones quickly!</p>
            """,
            3: """
                <h2>Shield Decoration and Designs 🎨</h2>
                <p>Viking shields weren't just plain wood - they were often beautifully decorated! Vikings used <strong>natural paints</strong> made from things they found in nature. They made paint from plants, minerals, and even animal products. These paints created bright, bold colors that could be seen from far away.</p>
                
                <p>The most common colors on Viking shields were <strong>red, yellow, black, and white</strong>. These colors stood out and made it easy to see which side a warrior was on during battle. Red was especially popular - it was a color of power and strength!</p>
                
                <p>Vikings painted all sorts of patterns on their shields. They loved <strong>spirals, circles, and geometric shapes</strong>. Some shields had simple designs, while others had complex patterns that covered the whole surface. The designs were often symmetrical, meaning they looked the same on both sides.</p>
                
                <p>Shields were decorated for important reasons! The designs helped warriors <strong>identify which group they belonged to</strong> during battle. They also made the shields look impressive and intimidating to enemies. Sometimes, shields even had <strong>runes (Viking letters) or family symbols</strong> painted on them.</p>
                
                <p>No two Viking shields were exactly the same! Each warrior's shield was unique, showing their own style and personality. Some warriors might have had simple designs, while others had elaborate artwork covering their shields.</p>
            """,
            4: """
                <h2>Using Shields in Battle ⚔️</h2>
                <p>Viking warriors held their shields <strong>with one hand using a handle on the back</strong>. This left their other hand free to hold a weapon like a sword, axe, or spear. Warriors needed to be able to move their shields quickly to block attacks from any direction!</p>
                
                <p>One of the most famous Viking battle tactics was the <strong>"Shield Wall"</strong>. Warriors would stand very close together with their shields overlapping, creating a wall of protection. This made it almost impossible for enemies to break through! The shield wall was like a moving fortress that could advance across the battlefield.</p>
                
                <p>Shields weren't just for blocking - they could also be used to attack! The <strong>metal boss in the center</strong> could be used to punch enemies. Warriors could also push with their shields to knock enemies off balance. A well-trained warrior could use their shield almost like a weapon!</p>
                
                <p>During battle, shields could get <strong>damaged, broken, or even lost</strong>. Arrows could stick in them, swords could cut through them, and they might split if hit hard enough. That's why it was important that shields could be made quickly - warriors might need a new one!</p>
                
                <p>When Vikings weren't fighting, they carried their shields <strong>on their back or slung over their shoulder</strong>. This kept their hands free for other tasks. The shields were an important part of a warrior's equipment, so they always kept them close.</p>
                
                <p>Shields were <strong>the main protection</strong> for Viking warriors in battle. Without a good shield, a warrior would be much more vulnerable to enemy attacks. That's why making and maintaining shields was so important to Viking society!</p>
            """
        },
        'correct_answers': {
            1: 'B', 2: 'A', 3: 'A', 4: 'B', 5: 'B', 6: 'B',
            7: 'B', 8: 'B', 9: 'A', 10: 'A', 11: 'A', 12: 'A',
            13: 'B', 14: 'A', 15: 'A', 16: 'A', 17: 'A', 18: 'A',
            19: 'A', 20: 'B', 21: 'A', 22: 'A', 23: 'A', 24: 'A'
        }
    },
    'vikings-medium': {
        'name': 'Vikings Advanced',
        'title': 'Vikings Quiz - Medium',
        'description': 'Dive deeper into Viking history, culture, and achievements!',
        'emoji': '⚔️',
        'difficulty': 'medium',
        'total_questions': 28,
        'sections': {
            1: {
                'title': 'Part 1: Viking Society and Government',
                'questions': [
                    {
                        'number': 1,
                        'text': 'What was the name of the Viking assembly where important decisions were made?',
                        'options': [
                            {'letter': 'A', 'text': 'Thing'},
                            {'letter': 'B', 'text': 'Meeting'},
                            {'letter': 'C', 'text': 'Council'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'What was a Jarl in Viking society?',
                        'options': [
                            {'letter': 'A', 'text': 'A noble or chieftain'},
                            {'letter': 'B', 'text': 'A type of ship'},
                            {'letter': 'C', 'text': 'A weapon'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'What were Viking slaves called?',
                        'options': [
                            {'letter': 'A', 'text': 'Thralls'},
                            {'letter': 'B', 'text': 'Servants'},
                            {'letter': 'C', 'text': 'Workers'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'What was the main social class of free Viking farmers and craftsmen called?',
                        'options': [
                            {'letter': 'A', 'text': 'Karls'},
                            {'letter': 'B', 'text': 'Nobles'},
                            {'letter': 'C', 'text': 'Warriors'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'What was a Viking law speaker responsible for?',
                        'options': [
                            {'letter': 'A', 'text': 'Reciting laws from memory at assemblies'},
                            {'letter': 'B', 'text': 'Building ships'},
                            {'letter': 'C', 'text': 'Cooking food'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'What was the Viking system of law and justice called?',
                        'options': [
                            {'letter': 'A', 'text': 'Blood feud or compensation system'},
                            {'letter': 'B', 'text': 'Trial by jury'},
                            {'letter': 'C', 'text': 'King\'s law'}
                        ]
                    },
                    {
                        'number': 7,
                        'text': 'What was outlawry in Viking society?',
                        'options': [
                            {'letter': 'A', 'text': 'Being banished from the community with no legal protection'},
                            {'letter': 'B', 'text': 'Being sent to prison'},
                            {'letter': 'C', 'text': 'Being made a slave'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: Viking Trade and Exploration',
                'questions': [
                    {
                        'number': 8,
                        'text': 'What was the name of the trade route that connected Scandinavia to the Byzantine Empire?',
                        'options': [
                            {'letter': 'A', 'text': 'The Varangian Route'},
                            {'letter': 'B', 'text': 'The Silk Road'},
                            {'letter': 'C', 'text': 'The Spice Route'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'What did Vikings trade from Scandinavia?',
                        'options': [
                            {'letter': 'A', 'text': 'Furs, amber, and slaves'},
                            {'letter': 'B', 'text': 'Gold and diamonds'},
                            {'letter': 'C', 'text': 'Spices and silk'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What was the name of the Viking settlement in Greenland?',
                        'options': [
                            {'letter': 'A', 'text': 'Brattahlíð'},
                            {'letter': 'B', 'text': 'Oslo'},
                            {'letter': 'C', 'text': 'Stockholm'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'What was the Viking name for the area they discovered in North America?',
                        'options': [
                            {'letter': 'A', 'text': 'Vinland'},
                            {'letter': 'B', 'text': 'Newland'},
                            {'letter': 'C', 'text': 'Greenland'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'Who was the famous Viking explorer who reached North America around 1000 AD?',
                        'options': [
                            {'letter': 'A', 'text': 'Leif Erikson'},
                            {'letter': 'B', 'text': 'Ragnar Lothbrok'},
                            {'letter': 'C', 'text': 'Harald Hardrada'}
                        ]
                    },
                    {
                        'number': 13,
                        'text': 'What was the name of the Viking trading center in Russia?',
                        'options': [
                            {'letter': 'A', 'text': 'Novgorod'},
                            {'letter': 'B', 'text': 'Moscow'},
                            {'letter': 'C', 'text': 'Kiev'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'What did Vikings call the Byzantine Empire?',
                        'options': [
                            {'letter': 'A', 'text': 'Miklagard (Great City)'},
                            {'letter': 'B', 'text': 'Rome'},
                            {'letter': 'C', 'text': 'Constantinople'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Part 3: Viking Ships and Navigation',
                'questions': [
                    {
                        'number': 15,
                        'text': 'What was the name of the special Viking navigation tool that used the sun?',
                        'options': [
                            {'letter': 'A', 'text': 'Sunstone'},
                            {'letter': 'B', 'text': 'Compass'},
                            {'letter': 'C', 'text': 'Sextant'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'What was the difference between a longship and a knarr?',
                        'options': [
                            {'letter': 'A', 'text': 'Knarrs were wider cargo ships, longships were for war'},
                            {'letter': 'B', 'text': 'They were the same thing'},
                            {'letter': 'C', 'text': 'Longships were bigger'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'What was the keel on a Viking ship used for?',
                        'options': [
                            {'letter': 'A', 'text': 'Stability and to prevent the ship from rolling'},
                            {'letter': 'B', 'text': 'Decoration'},
                            {'letter': 'C', 'text': 'To hold the sail'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'How did Vikings waterproof their ships?',
                        'options': [
                            {'letter': 'A', 'text': 'With tar made from pine trees'},
                            {'letter': 'B', 'text': 'With paint'},
                            {'letter': 'C', 'text': 'With wax'}
                        ]
                    },
                    {
                        'number': 19,
                        'text': 'What was the typical speed of a Viking longship?',
                        'options': [
                            {'letter': 'A', 'text': 'About 10-15 knots (12-17 mph) with good wind'},
                            {'letter': 'B', 'text': 'As fast as a car'},
                            {'letter': 'C', 'text': 'Very slow, like walking'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'What was the name of the steering oar on a Viking ship?',
                        'options': [
                            {'letter': 'A', 'text': 'Steerboard (which is where "starboard" comes from)'},
                            {'letter': 'B', 'text': 'Rudder'},
                            {'letter': 'C', 'text': 'Paddle'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Part 4: Viking Culture and Art',
                'questions': [
                    {
                        'number': 21,
                        'text': 'What was the name of the Viking art style with intricate animal patterns?',
                        'options': [
                            {'letter': 'A', 'text': 'Ringerike or Urnes style'},
                            {'letter': 'B', 'text': 'Modern art'},
                            {'letter': 'C', 'text': 'Cave paintings'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What were Viking poets called?',
                        'options': [
                            {'letter': 'A', 'text': 'Skalds'},
                            {'letter': 'B', 'text': 'Bards'},
                            {'letter': 'C', 'text': 'Singers'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'What was a saga?',
                        'options': [
                            {'letter': 'A', 'text': 'A long story about heroes and history'},
                            {'letter': 'B', 'text': 'A type of ship'},
                            {'letter': 'C', 'text': 'A weapon'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'What was the Viking board game hnefatafl?',
                        'options': [
                            {'letter': 'A', 'text': 'A strategy game like chess, with a king and attackers'},
                            {'letter': 'B', 'text': 'A dice game'},
                            {'letter': 'C', 'text': 'A card game'}
                        ]
                    },
                    {
                        'number': 25,
                        'text': 'What were Viking burial practices often like?',
                        'options': [
                            {'letter': 'A', 'text': 'Burial in ships or with grave goods'},
                            {'letter': 'B', 'text': 'Always cremation'},
                            {'letter': 'C', 'text': 'Simple ground burial only'}
                        ]
                    },
                    {
                        'number': 26,
                        'text': 'What was the Viking calendar based on?',
                        'options': [
                            {'letter': 'A', 'text': 'Lunar months and solar years'},
                            {'letter': 'B', 'text': 'Only the sun'},
                            {'letter': 'C', 'text': 'Only the moon'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'What was a Viking "thing" used for?',
                        'options': [
                            {'letter': 'A', 'text': 'Making laws, settling disputes, and choosing leaders'},
                            {'letter': 'B', 'text': 'Trading'},
                            {'letter': 'C', 'text': 'Religious ceremonies only'}
                        ]
                    },
                    {
                        'number': 28,
                        'text': 'What was the Viking Age approximately?',
                        'options': [
                            {'letter': 'A', 'text': '793 AD to 1066 AD'},
                            {'letter': 'B', 'text': '500 AD to 800 AD'},
                            {'letter': 'C', 'text': '1200 AD to 1500 AD'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {
            1: """
                <h2>Viking Society and Government 🏛️</h2>
                <p>Viking society was organized into three main social classes. At the top were the <strong>Jarls</strong> (nobles or chieftains) who were wealthy landowners and leaders. The middle class were the <strong>Karls</strong> - free farmers, craftsmen, and traders who made up most of Viking society. At the bottom were the <strong>Thralls</strong> (slaves) who had no rights and were considered property.</p>
                
                <p>Vikings didn't have kings ruling everything at first. Instead, they had local assemblies called <strong>Things</strong> (or "Tings"). These were meetings where free men gathered to make laws, settle disputes, and make important decisions. Things were held at special places, often marked by stones or in natural amphitheaters.</p>
                
                <p>At these assemblies, a special person called a <strong>law speaker</strong> would recite all the laws from memory! There were no written law books, so the law speaker had to remember everything. This was a very important job because everyone needed to know the laws.</p>
                
                <p>Viking law was based on a system of <strong>blood feuds and compensation</strong>. If someone was harmed, their family could seek revenge, but they could also accept payment (called "wergild" or "man-price") instead. This helped prevent endless cycles of violence.</p>
                
                <p>One of the most serious punishments in Viking society was <strong>outlawry</strong>. An outlaw was banished from the community and had no legal protection. Anyone could harm an outlaw without breaking the law. This was often a death sentence because outlaws had to survive alone in the harsh Scandinavian wilderness!</p>
            """,
            2: """
                <h2>Viking Trade and Exploration 🌍</h2>
                <p>Vikings were not just raiders - they were also excellent <strong>traders</strong>! They established trade routes that stretched from Scandinavia all the way to the Middle East and beyond. One famous route was <strong>the Varangian Route</strong>, which went through Russia to the Byzantine Empire (modern-day Turkey and surrounding areas).</p>
                
                <p>From Scandinavia, Vikings traded <strong>furs, amber, and slaves</strong>. They brought back silver, silk, spices, and other luxury goods. Amber was especially valuable - it's a golden fossilized tree resin that was used for jewelry and decoration.</p>
                
                <p>Vikings established trading centers throughout Europe. In Russia, they founded <strong>Novgorod</strong>, which became a major trading city. They also traded in places like Dublin (Ireland), York (England), and many other locations.</p>
                
                <p>Vikings called the Byzantine Empire <strong>Miklagard</strong>, which means "Great City" (referring to Constantinople, now Istanbul). Many Vikings served as elite guards for the Byzantine emperor - these were called the Varangian Guard!</p>
                
                <p>Vikings were incredible explorers. They settled in <strong>Greenland</strong>, with the main settlement called <strong>Brattahlíð</strong>. From there, they explored even further west and discovered <strong>Vinland</strong> (parts of modern-day Canada and possibly the northeastern United States).</p>
                
                <p>The most famous Viking explorer was <strong>Leif Erikson</strong> (also called Leif the Lucky). Around the year 1000 AD, he led an expedition to Vinland, making Vikings the first Europeans to reach North America - about 500 years before Christopher Columbus!</p>
            """,
            3: """
                <h2>Viking Ships and Navigation 🚢</h2>
                <p>Vikings built different types of ships for different purposes. <strong>Longships</strong> were fast, narrow warships designed for raiding and battle. They could sail in shallow water and even be carried over land! <strong>Knarrs</strong> were wider, deeper cargo ships used for trading and carrying supplies. They were slower but could carry much more.</p>
                
                <p>Viking ships were incredibly well-designed. The <strong>keel</strong> (the bottom center beam) was very important - it gave the ship stability and prevented it from rolling over in rough seas. Viking ships had a shallow draft, meaning they didn't need deep water, which allowed them to sail up rivers and land on beaches.</p>
                
                <p>To make their ships waterproof, Vikings used <strong>tar made from pine trees</strong>. They would heat the tar and spread it between the planks to seal them. The ships were also built with overlapping planks (called clinker-built) that made them very strong and flexible.</p>
                
                <p>Viking longships could reach speeds of about <strong>10-15 knots</strong> (12-17 miles per hour) with good wind. They could also be rowed when there was no wind. The steering was done with a special oar called a <strong>steerboard</strong> (always on the right side), which is where we get the word "starboard" from!</p>
                
                <p>Vikings were expert navigators. They used the sun, stars, and even special crystals called <strong>sunstones</strong> to find their way. Sunstones could help them locate the sun even on cloudy days by using polarized light. They also watched for birds, whales, and changes in water color to know when land was nearby.</p>
            """,
            4: """
                <h2>Viking Culture and Art 🎨</h2>
                <p>Vikings created beautiful art with intricate patterns. Their art styles are named after places where artifacts were found, like <strong>Ringerike</strong> and <strong>Urnes</strong> styles. These featured complex designs with animals, knots, and geometric patterns. Viking art decorated everything from jewelry to weapons to ships!</p>
                
                <p>Vikings loved stories and poetry. Professional poets called <strong>Skalds</strong> would compose and recite poems about heroes, gods, and important events. These poems were often very long and had special rules about rhythm and rhyme. Skalds were highly respected and could travel from place to place performing their poetry.</p>
                
                <p><strong>Sagas</strong> were long stories written in Iceland about Viking heroes, kings, and families. The most famous sagas tell about real and legendary Vikings, their adventures, battles, and journeys. Sagas are like historical novels that teach us a lot about Viking life and beliefs.</p>
                
                <p>Vikings enjoyed games! <strong>Hnefatafl</strong> was a popular strategy board game, similar to chess. One player had a king and defenders, while the other had attackers trying to capture the king. The game required skill and strategy, and Vikings would play it for fun and to practice thinking skills.</p>
                
                <p>Viking burial practices varied, but many important Vikings were buried in <strong>ships</strong> or with ship-shaped graves. They were buried with their weapons, jewelry, and other valuable items because Vikings believed they would need these things in the afterlife. Some Vikings were cremated (burned), while others were buried in the ground.</p>
                
                <p>The Viking calendar was based on <strong>lunar months and solar years</strong>. They divided the year into seasons and had special celebrations. Vikings were very aware of the changing seasons because farming and sailing depended on knowing the right times of year.</p>
                
                <p>The <strong>Viking Age</strong> is generally considered to have lasted from <strong>793 AD to 1066 AD</strong>. It began with the raid on Lindisfarne monastery in England and ended with the Battle of Stamford Bridge, where the last major Viking invasion was defeated. During this time, Vikings had a huge impact on Europe through exploration, trade, and settlement!</p>
            """
        },
        'correct_answers': {
            1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'A', 6: 'A', 7: 'A',
            8: 'A', 9: 'A', 10: 'A', 11: 'A', 12: 'A', 13: 'A', 14: 'A',
            15: 'A', 16: 'A', 17: 'A', 18: 'A', 19: 'A', 20: 'A',
            21: 'A', 22: 'A', 23: 'A', 24: 'A', 25: 'A', 26: 'A', 27: 'A', 28: 'A'
        }
    },
    'vikings-religion-hard': {
        'name': 'Viking Religion',
        'title': 'Viking Religion Quiz - Hard',
        'description': 'Master the complex world of Norse mythology, gods, and religious practices!',
        'emoji': '🔮',
        'difficulty': 'hard',
        'total_questions': 30,
        'sections': {
            1: {
                'title': 'Part 1: The Nine Worlds and Yggdrasil',
                'questions': [
                    {
                        'number': 1,
                        'text': 'What was the name of the great world tree that connected all the Nine Worlds?',
                        'options': [
                            {'letter': 'A', 'text': 'Yggdrasil'},
                            {'letter': 'B', 'text': 'Oak Tree'},
                            {'letter': 'C', 'text': 'Tree of Life'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'How many worlds were there in Norse mythology?',
                        'options': [
                            {'letter': 'A', 'text': 'Nine'},
                            {'letter': 'B', 'text': 'Seven'},
                            {'letter': 'C', 'text': 'Twelve'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'What was the name of the world where the gods lived?',
                        'options': [
                            {'letter': 'A', 'text': 'Asgard'},
                            {'letter': 'B', 'text': 'Midgard'},
                            {'letter': 'C', 'text': 'Jotunheim'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'What was Midgard?',
                        'options': [
                            {'letter': 'A', 'text': 'The world of humans (Middle Earth)'},
                            {'letter': 'B', 'text': 'The world of the dead'},
                            {'letter': 'C', 'text': 'The world of giants'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'What was the name of the world of the dead, ruled by Hel?',
                        'options': [
                            {'letter': 'A', 'text': 'Helheim'},
                            {'letter': 'B', 'text': 'Valhalla'},
                            {'letter': 'C', 'text': 'Niflheim'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'What creature lived at the roots of Yggdrasil and gnawed at it?',
                        'options': [
                            {'letter': 'A', 'text': 'Nidhogg (a dragon)'},
                            {'letter': 'B', 'text': 'A squirrel'},
                            {'letter': 'C', 'text': 'A snake'}
                        ]
                    },
                    {
                        'number': 7,
                        'text': 'What was the name of the well of wisdom at the roots of Yggdrasil?',
                        'options': [
                            {'letter': 'A', 'text': 'Mímir\'s Well'},
                            {'letter': 'B', 'text': 'The Well of Life'},
                            {'letter': 'C', 'text': 'The Sacred Spring'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'What was Jotunheim?',
                        'options': [
                            {'letter': 'A', 'text': 'The world of the giants'},
                            {'letter': 'B', 'text': 'The world of the gods'},
                            {'letter': 'C', 'text': 'The world of the dwarves'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: Major Gods and Goddesses',
                'questions': [
                    {
                        'number': 9,
                        'text': 'What was the name of Odin\'s magical spear?',
                        'options': [
                            {'letter': 'A', 'text': 'Gungnir'},
                            {'letter': 'B', 'text': 'Mjölnir'},
                            {'letter': 'C', 'text': 'Gram'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What were the names of Odin\'s two ravens?',
                        'options': [
                            {'letter': 'A', 'text': 'Huginn (Thought) and Muninn (Memory)'},
                            {'letter': 'B', 'text': 'Raven and Crow'},
                            {'letter': 'C', 'text': 'Odin and Loki'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'What was the name of Odin\'s eight-legged horse?',
                        'options': [
                            {'letter': 'A', 'text': 'Sleipnir'},
                            {'letter': 'B', 'text': 'Pegasus'},
                            {'letter': 'C', 'text': 'Shadowfax'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'What was the name of Thor\'s hammer?',
                        'options': [
                            {'letter': 'A', 'text': 'Mjölnir'},
                            {'letter': 'B', 'text': 'Gungnir'},
                            {'letter': 'C', 'text': 'Excalibur'}
                        ]
                    },
                    {
                        'number': 13,
                        'text': 'Who was the goddess of love, beauty, and fertility?',
                        'options': [
                            {'letter': 'A', 'text': 'Freya'},
                            {'letter': 'B', 'text': 'Frigg'},
                            {'letter': 'C', 'text': 'Hel'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'What was the name of the hall in Asgard where warriors who died in battle went?',
                        'options': [
                            {'letter': 'A', 'text': 'Valhalla'},
                            {'letter': 'B', 'text': 'Helheim'},
                            {'letter': 'C', 'text': 'Folkvangr'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'Who was the trickster god, known for causing trouble?',
                        'options': [
                            {'letter': 'A', 'text': 'Loki'},
                            {'letter': 'B', 'text': 'Odin'},
                            {'letter': 'C', 'text': 'Tyr'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'What was the name of Freya\'s hall where half of the warriors who died in battle went?',
                        'options': [
                            {'letter': 'A', 'text': 'Folkvangr'},
                            {'letter': 'B', 'text': 'Valhalla'},
                            {'letter': 'C', 'text': 'Asgard'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Part 3: Ragnarok and End Times',
                'questions': [
                    {
                        'number': 17,
                        'text': 'What was Ragnarok?',
                        'options': [
                            {'letter': 'A', 'text': 'The final battle and end of the world in Norse mythology'},
                            {'letter': 'B', 'text': 'A type of ship'},
                            {'letter': 'C', 'text': 'A Viking festival'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'What was the name of the giant wolf that would break free during Ragnarok?',
                        'options': [
                            {'letter': 'A', 'text': 'Fenrir'},
                            {'letter': 'B', 'text': 'Garm'},
                            {'letter': 'C', 'text': 'Nidhogg'}
                        ]
                    },
                    {
                        'number': 19,
                        'text': 'Who was destined to kill Odin during Ragnarok?',
                        'options': [
                            {'letter': 'A', 'text': 'Fenrir the wolf'},
                            {'letter': 'B', 'text': 'Loki'},
                            {'letter': 'C', 'text': 'Thor'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'What was the name of the giant serpent that Thor would fight during Ragnarok?',
                        'options': [
                            {'letter': 'A', 'text': 'Jormungandr (the Midgard Serpent)'},
                            {'letter': 'B', 'text': 'Nidhogg'},
                            {'letter': 'C', 'text': 'Fafnir'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'What would happen after Ragnarok according to Norse mythology?',
                        'options': [
                            {'letter': 'A', 'text': 'A new world would rise, and some gods would survive'},
                            {'letter': 'B', 'text': 'Everything would end forever'},
                            {'letter': 'C', 'text': 'The gods would win and rule forever'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What was the name of the ship made from dead men\'s fingernails that would sail during Ragnarok?',
                        'options': [
                            {'letter': 'A', 'text': 'Naglfari'},
                            {'letter': 'B', 'text': 'Longship'},
                            {'letter': 'C', 'text': 'Death Ship'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'Who would sound the horn to signal the start of Ragnarok?',
                        'options': [
                            {'letter': 'A', 'text': 'Heimdall'},
                            {'letter': 'B', 'text': 'Odin'},
                            {'letter': 'C', 'text': 'Loki'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Part 4: Religious Practices and Beliefs',
                'questions': [
                    {
                        'number': 24,
                        'text': 'What was a blót?',
                        'options': [
                            {'letter': 'A', 'text': 'A religious sacrifice ceremony to honor the gods'},
                            {'letter': 'B', 'text': 'A type of weapon'},
                            {'letter': 'C', 'text': 'A Viking festival'}
                        ]
                    },
                    {
                        'number': 25,
                        'text': 'What animals were commonly sacrificed in blóts?',
                        'options': [
                            {'letter': 'A', 'text': 'Horses, cattle, and pigs'},
                            {'letter': 'B', 'text': 'Only chickens'},
                            {'letter': 'C', 'text': 'Wild animals'}
                        ]
                    },
                    {
                        'number': 26,
                        'text': 'What was a hof?',
                        'options': [
                            {'letter': 'A', 'text': 'A temple or sacred building for worship'},
                            {'letter': 'B', 'text': 'A type of ship'},
                            {'letter': 'C', 'text': 'A weapon'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'What was the name of the special day of the week named after Odin?',
                        'options': [
                            {'letter': 'A', 'text': 'Wednesday (Woden\'s Day)'},
                            {'letter': 'B', 'text': 'Thursday'},
                            {'letter': 'C', 'text': 'Friday'}
                        ]
                    },
                    {
                        'number': 28,
                        'text': 'What was seidr?',
                        'options': [
                            {'letter': 'A', 'text': 'A form of magic and prophecy, often practiced by women'},
                            {'letter': 'B', 'text': 'A type of weapon'},
                            {'letter': 'C', 'text': 'A religious ceremony'}
                        ]
                    },
                    {
                        'number': 29,
                        'text': 'What was the name of the afterlife for those who didn\'t die in battle?',
                        'options': [
                            {'letter': 'A', 'text': 'Helheim (ruled by the goddess Hel)'},
                            {'letter': 'B', 'text': 'Valhalla'},
                            {'letter': 'C', 'text': 'Asgard'}
                        ]
                    },
                    {
                        'number': 30,
                        'text': 'What was the name of the bridge that connected Midgard to Asgard?',
                        'options': [
                            {'letter': 'A', 'text': 'Bifrost (the rainbow bridge)'},
                            {'letter': 'B', 'text': 'The Golden Bridge'},
                            {'letter': 'C', 'text': 'The Bridge of Gods'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {
            1: """
                <h2>The Nine Worlds and Yggdrasil 🌳</h2>
                <p>Norse mythology describes the universe as having <strong>Nine Worlds</strong>, all connected by a massive tree called <strong>Yggdrasil</strong> (pronounced IG-druh-sill). This world tree was an ash tree so enormous that its branches reached into the heavens and its roots went deep into the underworld.</p>
                
                <p>The most important world was <strong>Asgard</strong>, the home of the Aesir gods (like Odin, Thor, and Frigg). It was a beautiful realm with golden halls and was connected to Midgard by a rainbow bridge called Bifrost. <strong>Midgard</strong> (which means "Middle Earth") was the world of humans - our world! It was surrounded by a great ocean where the Midgard Serpent lived.</p>
                
                <p><strong>Jotunheim</strong> was the world of the giants (Jotuns), who were often enemies of the gods. <strong>Helheim</strong> (or just Hel) was the cold, dark world of the dead, ruled by the goddess Hel. This was where people who didn't die in battle went after death.</p>
                
                <p>At the roots of Yggdrasil were three wells. One was <strong>Mímir's Well</strong>, the well of wisdom. Odin gave up one of his eyes to drink from this well and gain incredible knowledge! Another well was the Well of Urd, where the Norns (fate goddesses) lived and wove the threads of destiny.</p>
                
                <p>A terrible dragon named <strong>Nidhogg</strong> lived at the roots of Yggdrasil and constantly gnawed at them, trying to destroy the tree. A squirrel named Ratatoskr ran up and down the tree carrying messages between Nidhogg and an eagle at the top, often spreading gossip and causing trouble!</p>
            """,
            2: """
                <h2>Major Gods and Goddesses ⚡</h2>
                <p><strong>Odin</strong> was the All-Father, the king of the gods. He was the god of wisdom, war, poetry, and magic. Odin had many special items: his magical spear <strong>Gungnir</strong> that never missed its target, his eight-legged horse <strong>Sleipnir</strong> that could travel between worlds, and two ravens named <strong>Huginn</strong> (Thought) and <strong>Muninn</strong> (Memory) who flew around the world each day and told him everything they saw.</p>
                
                <p><strong>Thor</strong> was the god of thunder and strength. His famous hammer was called <strong>Mjölnir</strong> (pronounced MYOL-neer), and it always returned to his hand after he threw it. Thor also had a magical belt that doubled his strength and iron gloves that let him catch his hammer. He was the protector of both gods and humans.</p>
                
                <p><strong>Freya</strong> was the goddess of love, beauty, fertility, and war. She was incredibly powerful and had her own hall called <strong>Folkvangr</strong>, where she received half of all warriors who died in battle (the other half went to Odin's Valhalla). Freya could also practice seidr magic and had a cloak of falcon feathers that let her transform into a bird.</p>
                
                <p><strong>Loki</strong> was the trickster god, known for causing problems but also helping the gods when needed. He was a shape-shifter and could change into different animals. Loki was responsible for many of the gods' troubles, including the death of the beloved god Baldr, which led to his punishment.</p>
                
                <p><strong>Valhalla</strong> was Odin's great hall in Asgard. Warriors who died bravely in battle were chosen by the Valkyries (warrior maidens) to go to Valhalla, where they would feast and train every day until Ragnarok. The hall was so large it had 540 doors, and each door was wide enough for 800 warriors to march through side by side!</p>
            """,
            3: """
                <h2>Ragnarok and End Times 🔥</h2>
                <p><strong>Ragnarok</strong> (pronounced RAG-nuh-rok) was the prophesied end of the world in Norse mythology. It means "Twilight of the Gods" or "Fate of the Gods." This was not just a battle - it was a series of disasters that would destroy the entire world.</p>
                
                <p>The events of Ragnarok would begin when <strong>Loki</strong> and his children broke free from their bonds. <strong>Fenrir</strong>, the giant wolf that the gods had chained up, would break free and grow so large that his upper jaw touched the sky and his lower jaw touched the earth. He would kill Odin during the final battle.</p>
                
                <p><strong>Jormungandr</strong>, the Midgard Serpent, was so large it encircled the entire world. During Ragnarok, it would rise from the ocean and fight Thor. Thor would kill the serpent but would die from its poison shortly after. This shows that even the gods were not immortal - they could die.</p>
                
                <p><strong>Heimdall</strong>, the watchman of the gods, would blow his horn Gjallarhorn to signal the start of Ragnarok. A ship called <strong>Naglfari</strong>, made from the fingernails of dead men, would sail with an army of the dead. The world would be consumed by fire, and almost all the gods and creatures would die.</p>
                
                <p>But Ragnarok was not the complete end! After the destruction, a new world would rise from the sea. Some gods would survive (including Thor's sons and Odin's sons), and a new generation of humans would repopulate the world. This shows that Norse mythology believed in cycles - death and rebirth, not just destruction.</p>
            """,
            4: """
                <h2>Religious Practices and Beliefs 🕯️</h2>
                <p>Vikings practiced their religion through ceremonies called <strong>blóts</strong> (pronounced BLOATS). These were sacrifice ceremonies where animals (usually horses, cattle, or pigs) were killed and offered to the gods. The meat would be cooked and shared in a feast, and the blood would be sprinkled on altars, idols, and participants. Blóts were held at special times of the year, like the beginning of winter or summer.</p>
                
                <p>Vikings built <strong>hofs</strong> (temples) for worship, though many ceremonies were also held outdoors at sacred groves, stones, or other natural places. These temples were wooden buildings with altars and statues of the gods. Some were quite elaborate, while others were simple structures.</p>
                
                <p><strong>Seidr</strong> (pronounced SAY-thur) was a form of magic and prophecy. It was often practiced by women called "volvas" or "seidr-workers." Seidr could be used to see the future, influence events, or even change someone's fate. Odin learned seidr, but it was considered a feminine practice, so male gods who used it were sometimes looked down upon.</p>
                
                <p>Vikings believed in an afterlife, but where you went depended on how you died. Warriors who died in battle went to either <strong>Valhalla</strong> (Odin's hall) or <strong>Folkvangr</strong> (Freya's hall). Everyone else went to <strong>Helheim</strong>, the cold realm ruled by the goddess Hel. Helheim wasn't necessarily a place of punishment - it was just where most dead people went, and it was described as being cold and dark.</p>
                
                <p>The <strong>Bifrost</strong> was the rainbow bridge that connected Midgard (the human world) to Asgard (the world of the gods). It was guarded by Heimdall, who could see and hear everything. The bridge was said to be red, yellow, and blue, and it would break during Ragnarok when the armies of the dead tried to cross it.</p>
                
                <p>Many of our days of the week are named after Norse gods! <strong>Wednesday</strong> comes from "Woden's Day" (Woden is another name for Odin). <strong>Thursday</strong> is "Thor's Day," <strong>Friday</strong> comes from "Frigg's Day" (or possibly Freya's Day), and <strong>Tuesday</strong> is named after Tyr, the god of war and justice. This shows how deeply Viking religion influenced our modern culture!</p>
            """
        },
        'correct_answers': {
            1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'A', 6: 'A', 7: 'A', 8: 'A',
            9: 'A', 10: 'A', 11: 'A', 12: 'A', 13: 'A', 14: 'A', 15: 'A', 16: 'A',
            17: 'A', 18: 'A', 19: 'A', 20: 'A', 21: 'A', 22: 'A', 23: 'A',
            24: 'A', 25: 'A', 26: 'A', 27: 'A', 28: 'A', 29: 'A', 30: 'A'
        }
    },
    'viking-queen-journal': {
        'name': 'Queen Astrid\'s Journal',
        'title': 'Queen Astrid\'s Journal - Hard',
        'description': 'Read a Viking queen\'s journal and use inference to answer challenging questions!',
        'emoji': '📜',
        'difficulty': 'hard',
        'total_questions': 25,
        'sections': {
            1: {
                'title': 'Part 1: Daily Life and Responsibilities',
                'questions': [
                    {
                        'number': 1,
                        'text': 'Based on the journal, what was Queen Astrid\'s main concern about the upcoming winter?',
                        'options': [
                            {'letter': 'A', 'text': 'Having enough preserved food to last through the cold months'},
                            {'letter': 'B', 'text': 'The weather being too warm'},
                            {'letter': 'C', 'text': 'Having too much food'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'What can we infer about the relationship between Queen Astrid and her husband?',
                        'options': [
                            {'letter': 'A', 'text': 'She has no say in important matters'},
                            {'letter': 'B', 'text': 'They share responsibilities and make decisions together'},
                            {'letter': 'C', 'text': 'They never speak to each other'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'What does the journal suggest about Viking women\'s roles?',
                        'options': [
                            {'letter': 'A', 'text': 'They only cooked and cleaned'},
                            {'letter': 'B', 'text': 'They had important responsibilities in managing the household and community'},
                            {'letter': 'C', 'text': 'They had no responsibilities'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'Based on the journal entry, what was the Thing used for?',
                        'options': [
                            {'letter': 'A', 'text': 'Making important community decisions and settling disputes'},
                            {'letter': 'B', 'text': 'Only for trading'},
                            {'letter': 'C', 'text': 'Just a social gathering'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'What can we infer about how Vikings preserved food?',
                        'options': [
                            {'letter': 'A', 'text': 'They used methods like drying, salting, and smoking'},
                            {'letter': 'B', 'text': 'They used freezers'},
                            {'letter': 'C', 'text': 'They didn\'t preserve food'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'What does the journal suggest about Viking children?',
                        'options': [
                            {'letter': 'A', 'text': 'They helped with important tasks and learned skills from adults'},
                            {'letter': 'B', 'text': 'They did nothing all day'},
                            {'letter': 'C', 'text': 'They only played games'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: Trade and Economy',
                'questions': [
                    {
                        'number': 7,
                        'text': 'Based on the journal, what can we infer about Viking trade?',
                        'options': [
                            {'letter': 'A', 'text': 'They traded with distant places and valued foreign goods'},
                            {'letter': 'B', 'text': 'They never traded'},
                            {'letter': 'C', 'text': 'They only traded locally'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'What does the journal suggest about how Vikings valued items?',
                        'options': [
                            {'letter': 'A', 'text': 'They only used paper money'},
                            {'letter': 'B', 'text': 'They measured value by weight and quality, not just coins'},
                            {'letter': 'C', 'text': 'They didn\'t value anything'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'What can we infer about Viking craftsmanship?',
                        'options': [
                            {'letter': 'A', 'text': 'They bought everything from stores'},
                            {'letter': 'B', 'text': 'They were skilled at making and repairing tools and items'},
                            {'letter': 'C', 'text': 'They couldn\'t make anything'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'Based on the journal, what was important in Viking trade?',
                        'options': [
                            {'letter': 'A', 'text': 'Fair exchange and building relationships with traders'},
                            {'letter': 'B', 'text': 'Cheating people'},
                            {'letter': 'C', 'text': 'Only trading with family'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'What does the journal suggest about Viking communities?',
                        'options': [
                            {'letter': 'A', 'text': 'They worked together and supported each other'},
                            {'letter': 'B', 'text': 'Everyone worked alone'},
                            {'letter': 'C', 'text': 'They never helped each other'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Part 3: Social Structure and Leadership',
                'questions': [
                    {
                        'number': 12,
                        'text': 'Based on the journal, what can we infer about Viking leadership?',
                        'options': [
                            {'letter': 'A', 'text': 'Leaders had to earn respect and make good decisions for their people'},
                            {'letter': 'B', 'text': 'Anyone could be a leader'},
                            {'letter': 'C', 'text': 'Leaders didn\'t need to do anything'}
                        ]
                    },
                    {
                        'number': 13,
                        'text': 'What does the journal suggest about how disputes were resolved?',
                        'options': [
                            {'letter': 'A', 'text': 'By fighting immediately'},
                            {'letter': 'B', 'text': 'Through discussion and finding fair solutions at the Thing'},
                            {'letter': 'C', 'text': 'They were never resolved'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'What can we infer about the relationship between different Viking families?',
                        'options': [
                            {'letter': 'A', 'text': 'They formed alliances and worked together for mutual benefit'},
                            {'letter': 'B', 'text': 'They were always enemies'},
                            {'letter': 'C', 'text': 'They never interacted'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'Based on the journal, what was important for maintaining a good reputation?',
                        'options': [
                            {'letter': 'A', 'text': 'Keeping promises, being fair, and treating others well'},
                            {'letter': 'B', 'text': 'Being dishonest'},
                            {'letter': 'C', 'text': 'Not caring about others'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'What does the journal suggest about Viking honor?',
                        'options': [
                            {'letter': 'A', 'text': 'Honor was very important and affected how people were treated'},
                            {'letter': 'B', 'text': 'Honor didn\'t matter'},
                            {'letter': 'C', 'text': 'Only men had honor'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Part 4: Culture and Beliefs',
                'questions': [
                    {
                        'number': 17,
                        'text': 'Based on the journal, what can we infer about Viking religious practices?',
                        'options': [
                            {'letter': 'A', 'text': 'They made offerings to the gods and believed the gods influenced their lives'},
                            {'letter': 'B', 'text': 'They didn\'t believe in gods'},
                            {'letter': 'C', 'text': 'They only prayed once a year'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'What does the journal suggest about how Vikings viewed the future?',
                        'options': [
                            {'letter': 'A', 'text': 'They believed in preparing for the future but also accepted fate'},
                            {'letter': 'B', 'text': 'They never thought about the future'},
                            {'letter': 'C', 'text': 'They believed they could control everything'}
                        ]
                    },
                    {
                        'number': 19,
                        'text': 'What can we infer about Viking storytelling?',
                        'options': [
                            {'letter': 'A', 'text': 'Stories were important for teaching, entertainment, and preserving history'},
                            {'letter': 'B', 'text': 'They never told stories'},
                            {'letter': 'C', 'text': 'Stories were only for children'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'Based on the journal, what was the role of runes?',
                        'options': [
                            {'letter': 'A', 'text': 'They were just decorations'},
                            {'letter': 'B', 'text': 'They were used for writing, magic, and marking important items'},
                            {'letter': 'C', 'text': 'They were never used'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'What does the journal suggest about Viking views on nature?',
                        'options': [
                            {'letter': 'A', 'text': 'They respected nature and understood its cycles and importance'},
                            {'letter': 'B', 'text': 'They didn\'t care about nature'},
                            {'letter': 'C', 'text': 'They feared all nature'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What can we infer about Viking celebrations?',
                        'options': [
                            {'letter': 'A', 'text': 'They marked important times and brought the community together'},
                            {'letter': 'B', 'text': 'They never celebrated'},
                            {'letter': 'C', 'text': 'Only leaders celebrated'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'Based on the journal, what was important in Viking education?',
                        'options': [
                            {'letter': 'A', 'text': 'Teaching practical skills, stories, and values to the next generation'},
                            {'letter': 'B', 'text': 'Children learned nothing'},
                            {'letter': 'C', 'text': 'Only boys were educated'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'What does the journal suggest about Viking views on hard work?',
                        'options': [
                            {'letter': 'A', 'text': 'Hard work was valued and necessary for survival and success'},
                            {'letter': 'B', 'text': 'They avoided work'},
                            {'letter': 'C', 'text': 'Only slaves worked'}
                        ]
                    },
                    {
                        'number': 25,
                        'text': 'What can we infer about how Vikings viewed their place in the world?',
                        'options': [
                            {'letter': 'A', 'text': 'They saw themselves as part of a larger community and world, connected to gods and nature'},
                            {'letter': 'B', 'text': 'They thought they were alone'},
                            {'letter': 'C', 'text': 'They didn\'t think about it'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {
            1: """
                <h2>Queen Astrid's Journal Entry 📜</h2>
                <div style="background: #f4e4bc; padding: 30px; border: 5px solid #8b5a3c; border-radius: 0; font-style: italic; line-height: 1.8; color: #3d2817; margin: 20px 0;">
                    <p><strong>Autumn, Year of the Great Harvest</strong></p>
                    
                    <p>Today I sit by the fire in our longhouse, the smoke rising through the hole in the roof. My husband Ragnar and I have spent the day preparing for the Thing that will be held at the full moon. Many families from our region will gather to discuss the dispute between the Jarlsson and Eriksson families over the grazing lands. I have been helping Ragnar think through what would be a fair solution - one that honors both families and prevents a blood feud.</p>
                    
                    <p>The children have been busy today. My daughter Ingrid, who is twelve winters old, has been learning to spin wool with the other girls. She is becoming quite skilled, and I am proud. My son Bjorn, who is ten, helped his father repair the fishing nets this morning, then spent the afternoon practicing with a small wooden sword. He dreams of becoming a great warrior like his grandfather, but I remind him that most Vikings are farmers first, and he must learn all the skills needed to survive.</p>
                    
                    <p>We have been preserving food for the winter. The thralls have been salting fish and smoking meat. I oversaw the drying of berries and the storage of grains in our underground storage pit. If we do not prepare well now, we will suffer when the snow comes and the fjords freeze. Last winter was harsh, and three families in our settlement lost members to the cold and hunger. I will not let that happen to our people if I can help it.</p>
                    
                    <p>Yesterday, traders from the east arrived. They brought beautiful amber, fine cloth, and silver coins from the lands beyond the great rivers. I traded some of our furs and the fine wool cloth that the women of our household have woven. The traders were fair, and we both left satisfied. I made sure to get a good weight of silver - not just coins, but also some jewelry that can be cut into pieces for smaller trades. This is the way of our people - we measure value carefully.</p>
                    
                    <p>Tonight, after the evening meal, the skalds will tell stories of the gods. They will speak of Odin's wisdom, Thor's strength, and the great deeds of heroes from times past. The children love these stories, and I believe they learn important lessons from them - about honor, courage, and the consequences of one's actions. I have asked the skalds to tell the story of how Odin gained wisdom by sacrificing his eye at Mímir's Well. It is a story that teaches that great knowledge comes at a price.</p>
                    
                    <p>I have been practicing my runes. I carved a blessing into the doorframe of our longhouse, asking the gods to protect our home and bring good fortune. Runes are powerful - they are not just letters, but symbols that can bring protection, luck, or even magic. My mother taught me this, and I will teach my daughter as well.</p>
                    
                    <p>As I write this, I think about the responsibilities I carry. As a queen, I must help my husband make wise decisions. I must ensure our people are fed, our children are educated, and our community remains strong. I must maintain good relationships with other families and settlements. Honor is everything - if we lose our honor, we lose everything.</p>
                    
                    <p>The seasons turn, and we must turn with them. We prepare for winter, knowing that spring will come again. We work hard, knowing that our efforts will be rewarded. We honor the gods, knowing that they watch over us. This is the way of our people, and I am proud to be part of it.</p>
                    
                    <p style="text-align: right; margin-top: 20px;"><strong>- Queen Astrid</strong></p>
                </div>
                
                <p style="margin-top: 20px; font-weight: bold; color: #6b4423;">Read the journal entry carefully above. Then answer the questions below by inferring information from what Queen Astrid wrote. You'll need to think about what she says and what it tells us about Viking life!</p>
            """,
            2: """
                <h2>Continue Reading the Journal 📜</h2>
                <p style="font-weight: bold; color: #6b4423;">Use the journal entry from Part 1 to answer these questions about trade and economy.</p>
            """,
            3: """
                <h2>Continue Reading the Journal 📜</h2>
                <p style="font-weight: bold; color: #6b4423;">Use the journal entry from Part 1 to answer these questions about social structure and leadership.</p>
            """,
            4: """
                <h2>Continue Reading the Journal 📜</h2>
                <p style="font-weight: bold; color: #6b4423;">Use the journal entry from Part 1 to answer these questions about culture and beliefs.</p>
            """
        },
        'correct_answers': {
            1: 'A', 2: 'B', 3: 'B', 4: 'A', 5: 'A', 6: 'A',
            7: 'A', 8: 'B', 9: 'B', 10: 'A', 11: 'A',
            12: 'A', 13: 'B', 14: 'A', 15: 'A', 16: 'A',
            17: 'A', 18: 'A', 19: 'A', 20: 'B', 21: 'A', 22: 'A', 23: 'A', 24: 'A', 25: 'A'
        }
    }
}

@app.route('/')
def home():
    # Organize quizzes by difficulty
    quizzes_by_difficulty = {
        'easy': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'easy'},
        'medium': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'medium'},
        'hard': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'hard'}
    }
    return render_template('home.html', quizzes_by_difficulty=quizzes_by_difficulty)

@app.route('/quiz/<quiz_id>')
def quiz_index(quiz_id):
    if quiz_id not in quizzes:
        return "Quiz not found", 404
    quiz = quizzes[quiz_id]
    return render_template('index.html', quiz=quiz, quiz_id=quiz_id)

@app.route('/quiz/<quiz_id>/section/<int:section_num>')
def section(quiz_id, section_num):
    if quiz_id not in quizzes:
        return "Quiz not found", 404
    quiz = quizzes[quiz_id]
    if section_num not in quiz['sections']:
        return "Section not found", 404
    section_data = quiz['sections'][section_num]
    reading = quiz['reading_material'].get(section_num, '')
    return render_template('section.html', 
                         quiz_id=quiz_id,
                         quiz=quiz,
                         section_num=section_num,
                         section_title=section_data['title'],
                         questions=section_data['questions'],
                         reading=reading,
                         total_sections=len(quiz['sections']))

@app.route('/quiz/<quiz_id>/check_answer', methods=['POST'])
def check_answer(quiz_id):
    if quiz_id not in quizzes:
        return jsonify({'error': 'Quiz not found'}), 404
    quiz = quizzes[quiz_id]
    data = request.json
    question_num = int(data.get('question_num'))
    selected_answer = data.get('answer')
    
    correct = quiz['correct_answers'].get(question_num)
    is_correct = selected_answer == correct
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': correct
    })

@app.route('/quiz/<quiz_id>/results')
def results(quiz_id):
    if quiz_id not in quizzes:
        return "Quiz not found", 404
    quiz = quizzes[quiz_id]
    return render_template('results.html', quiz=quiz, quiz_id=quiz_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
