from flask import Flask, render_template, request, jsonify
import sys
import os

# Handle PyInstaller bundle path for templates
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    template_folder = os.path.join(sys._MEIPASS, 'templates')
else:
    # Running as script
    template_folder = 'templates'

app = Flask(__name__, template_folder=template_folder)

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
                            {'letter': 'A', 'text': 'The Mediterranean region'},
                            {'letter': 'B', 'text': 'Scandinavia (countries like Norway and Sweden)'},
                            {'letter': 'C', 'text': 'Central Europe'}
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
                            {'letter': 'A', 'text': 'Merchants'},
                            {'letter': 'B', 'text': 'Farmers'},
                            {'letter': 'C', 'text': 'Craftsmen'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'What were Viking letters and writing called?',
                        'options': [
                            {'letter': 'A', 'text': 'Latin'},
                            {'letter': 'B', 'text': 'Runes'},
                            {'letter': 'C', 'text': 'Greek'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'Where did Vikings usually carve their writing?',
                        'options': [
                            {'letter': 'A', 'text': 'On parchment'},
                            {'letter': 'B', 'text': 'On stones and wood'},
                            {'letter': 'C', 'text': 'On clay tablets'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'What did Vikings use to buy things before they had coins?',
                        'options': [
                            {'letter': 'A', 'text': 'Gold coins'},
                            {'letter': 'B', 'text': 'Silver jewelry (often cut into pieces)'},
                            {'letter': 'C', 'text': 'Bartering (trading goods for goods)'}
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
                            {'letter': 'C', 'text': 'Cottages'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'What were most Viking houses made out of?',
                        'options': [
                            {'letter': 'A', 'text': 'Wood, stone, or turf (grass and dirt)'},
                            {'letter': 'B', 'text': 'Bricks and cement'},
                            {'letter': 'C', 'text': 'Clay and mud'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'Where was the fire usually placed in a Viking house?',
                        'options': [
                            {'letter': 'A', 'text': 'In the fireplace by the wall'},
                            {'letter': 'B', 'text': 'In the middle of the room on the floor'},
                            {'letter': 'C', 'text': 'In a separate kitchen room'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What material were Viking clothes mostly made from?',
                        'options': [
                            {'letter': 'A', 'text': 'Cotton'},
                            {'letter': 'B', 'text': 'Wool and linen'},
                            {'letter': 'C', 'text': 'Leather'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'What did Viking children do for fun?',
                        'options': [
                            {'letter': 'A', 'text': 'Played with toys and dolls'},
                            {'letter': 'B', 'text': 'Played board games and wrestled'},
                            {'letter': 'C', 'text': 'Read books'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'Which of these animals did Vikings keep on their farms?',
                        'options': [
                            {'letter': 'A', 'text': 'Horses'},
                            {'letter': 'B', 'text': 'Pigs, sheep, and chickens'},
                            {'letter': 'C', 'text': 'Goats'}
                        ]
                    },
                    {
                        'number': 13,
                        'text': 'What did Vikings eat a lot of?',
                        'options': [
                            {'letter': 'A', 'text': 'Bread and cheese'},
                            {'letter': 'B', 'text': 'Fish and meat stew'},
                            {'letter': 'C', 'text': 'Fruits and vegetables'}
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
                            {'letter': 'A', 'text': 'Galleys'},
                            {'letter': 'B', 'text': 'Longships'},
                            {'letter': 'C', 'text': 'Skiffs'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What scary animal head was often carved on the front of a Viking ship?',
                        'options': [
                            {'letter': 'A', 'text': 'A dragon or snake'},
                            {'letter': 'B', 'text': 'A wolf'},
                            {'letter': 'C', 'text': 'A bear'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'Why did they put dragon heads on their ships?',
                        'options': [
                            {'letter': 'A', 'text': 'To show which family owned the ship'},
                            {'letter': 'B', 'text': 'To scare away enemies and sea monsters'},
                            {'letter': 'C', 'text': 'To honor the gods'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'How did Viking ships move across the water?',
                        'options': [
                            {'letter': 'A', 'text': 'With paddles only'},
                            {'letter': 'B', 'text': 'Using sails and oars (rowing)'},
                            {'letter': 'C', 'text': 'With a sail only'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'Vikings were great explorers. Which faraway place did they reach before Christopher Columbus?',
                        'options': [
                            {'letter': 'A', 'text': 'North America'},
                            {'letter': 'B', 'text': 'South America'},
                            {'letter': 'C', 'text': 'Asia'}
                        ]
                    },
                    {
                        'number': 19,
                        'text': 'How did Vikings find their way at sea?',
                        'options': [
                            {'letter': 'A', 'text': 'They used compasses'},
                            {'letter': 'B', 'text': 'They looked at the sun, stars, and birds'},
                            {'letter': 'C', 'text': 'They followed other ships'}
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
                            {'letter': 'C', 'text': 'Only for special ceremonies'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'What was the Viking\'s most common weapon?',
                        'options': [
                            {'letter': 'A', 'text': 'A sword'},
                            {'letter': 'B', 'text': 'An axe or a spear'},
                            {'letter': 'C', 'text': 'A bow and arrow'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What did Vikings use to protect themselves in a fight?',
                        'options': [
                            {'letter': 'A', 'text': 'A round wooden shield'},
                            {'letter': 'B', 'text': 'A metal shield'},
                            {'letter': 'C', 'text': 'Armor made of chainmail'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'What was a "Shield Wall"?',
                        'options': [
                            {'letter': 'A', 'text': 'A defensive wall around a village'},
                            {'letter': 'B', 'text': 'When warriors stood close together with shields overlapping'},
                            {'letter': 'C', 'text': 'A formation where shields were stacked'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'What were the very fierce Viking warriors called?',
                        'options': [
                            {'letter': 'A', 'text': 'Berserkers'},
                            {'letter': 'B', 'text': 'Jarls'},
                            {'letter': 'C', 'text': 'Huscarls'}
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
                            {'letter': 'A', 'text': 'Loki'},
                            {'letter': 'B', 'text': 'Thor'},
                            {'letter': 'C', 'text': 'Odin'}
                        ]
                    },
                    {
                        'number': 26,
                        'text': 'What weapon did Thor carry?',
                        'options': [
                            {'letter': 'A', 'text': 'A magic hammer'},
                            {'letter': 'B', 'text': 'A sword'},
                            {'letter': 'C', 'text': 'An axe'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'Who was the king of all the Viking gods?',
                        'options': [
                            {'letter': 'A', 'text': 'Odin'},
                            {'letter': 'B', 'text': 'Thor'},
                            {'letter': 'C', 'text': 'Tyr'}
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
                            {'letter': 'B', 'text': 'Asgard'},
                            {'letter': 'C', 'text': 'Helheim'}
                        ]
                    },
                    {
                        'number': 30,
                        'text': 'Which day of the week is named after the god Thor?',
                        'options': [
                            {'letter': 'A', 'text': 'Tuesday'},
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
                            {'letter': 'C', 'text': 'Leather'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'What type of wood was most commonly used for Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Oak, pine, or linden (lime wood)'},
                            {'letter': 'B', 'text': 'Birch'},
                            {'letter': 'C', 'text': 'Ash'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'How thick were most Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'About 1 inch (2-3 cm) thick'},
                            {'letter': 'B', 'text': 'About half an inch (1 cm) thick'},
                            {'letter': 'C', 'text': 'About 2-3 inches (5-7 cm) thick'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'What was placed on the front of the shield to make it stronger?',
                        'options': [
                            {'letter': 'A', 'text': 'A layer of leather'},
                            {'letter': 'B', 'text': 'A metal boss (round center piece)'},
                            {'letter': 'C', 'text': 'Metal strips around the edge'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'What was the metal boss on a Viking shield used for?',
                        'options': [
                            {'letter': 'A', 'text': 'Just decoration'},
                            {'letter': 'B', 'text': 'Protection and to hold the shield together'},
                            {'letter': 'C', 'text': 'To identify the owner'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'What was the handle on a Viking shield usually made from?',
                        'options': [
                            {'letter': 'A', 'text': 'Metal'},
                            {'letter': 'B', 'text': 'Leather or wood'},
                            {'letter': 'C', 'text': 'Rope'}
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
                            {'letter': 'C', 'text': 'Bound together with leather strips only'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'What shape were most Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Square'},
                            {'letter': 'B', 'text': 'Round'},
                            {'letter': 'C', 'text': 'Oval'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'How big were Viking shields usually?',
                        'options': [
                            {'letter': 'A', 'text': 'About 2-3 feet (60-90 cm) across'},
                            {'letter': 'B', 'text': 'About 4-5 feet (120-150 cm) across'},
                            {'letter': 'C', 'text': 'About 1 foot (30 cm) across'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What was sometimes added to the edge of a shield?',
                        'options': [
                            {'letter': 'A', 'text': 'A leather rim to protect the edges'},
                            {'letter': 'B', 'text': 'Metal studs'},
                            {'letter': 'C', 'text': 'Decorative carvings'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'Why did Vikings make their shields from wood instead of metal?',
                        'options': [
                            {'letter': 'A', 'text': 'Wood was lighter and easier to carry'},
                            {'letter': 'B', 'text': 'Wood was stronger than metal'},
                            {'letter': 'C', 'text': 'Metal was too expensive'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'How long did it take to make a Viking shield?',
                        'options': [
                            {'letter': 'A', 'text': 'A skilled craftsman could make one in a few days'},
                            {'letter': 'B', 'text': 'A few hours'},
                            {'letter': 'C', 'text': 'Several weeks'}
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
                            {'letter': 'A', 'text': 'Oil-based paints'},
                            {'letter': 'B', 'text': 'Natural paints made from plants, minerals, and animal products'},
                            {'letter': 'C', 'text': 'Dyes made from berries'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'What colors were commonly used on Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Red, yellow, black, and white'},
                            {'letter': 'B', 'text': 'Only green'},
                            {'letter': 'C', 'text': 'Brown and gray'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What patterns were often painted on Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Spirals, circles, and geometric shapes'},
                            {'letter': 'B', 'text': 'Animals and birds'},
                            {'letter': 'C', 'text': 'Straight lines and stripes'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'Why did Vikings decorate their shields?',
                        'options': [
                            {'letter': 'A', 'text': 'To show which group they belonged to and to look impressive'},
                            {'letter': 'B', 'text': 'To make them stronger'},
                            {'letter': 'C', 'text': 'To honor the gods'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'What symbol was sometimes painted on shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Runes (Viking letters) or family symbols'},
                            {'letter': 'B', 'text': 'Crosses'},
                            {'letter': 'C', 'text': 'Stars and moons'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'Were all Viking shields decorated the same way?',
                        'options': [
                            {'letter': 'A', 'text': 'No, each shield was unique'},
                            {'letter': 'B', 'text': 'Yes, they all looked the same'},
                            {'letter': 'C', 'text': 'Only shields for leaders had decorations'}
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
                            {'letter': 'C', 'text': 'With a strap around the arm'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'What was a "Shield Wall"?',
                        'options': [
                            {'letter': 'A', 'text': 'A defensive wall around a village'},
                            {'letter': 'B', 'text': 'Warriors standing close together with shields overlapping'},
                            {'letter': 'C', 'text': 'Shields stacked in a pile'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'Could Viking shields be used to attack as well as defend?',
                        'options': [
                            {'letter': 'A', 'text': 'Yes, the metal boss could be used to punch'},
                            {'letter': 'B', 'text': 'No, they were only for blocking'},
                            {'letter': 'C', 'text': 'Only the edge could be used to strike'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What happened to shields during battle?',
                        'options': [
                            {'letter': 'A', 'text': 'They could get damaged, broken, or lost'},
                            {'letter': 'B', 'text': 'They never got damaged'},
                            {'letter': 'C', 'text': 'They were always repaired immediately'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'How did Vikings carry their shields when not fighting?',
                        'options': [
                            {'letter': 'A', 'text': 'On their back or slung over their shoulder'},
                            {'letter': 'B', 'text': 'In a special bag'},
                            {'letter': 'C', 'text': 'Carried by servants'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'Why were shields so important to Viking warriors?',
                        'options': [
                            {'letter': 'A', 'text': 'They were the main protection in battle'},
                            {'letter': 'B', 'text': 'They were required by law'},
                            {'letter': 'C', 'text': 'They showed social status'}
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
    },
    'ancient-egypt': {
        'name': 'Ancient Egypt',
        'title': 'Ancient Egypt Quiz',
        'description': 'Explore the amazing world of pharaohs, pyramids, and mummies!',
        'emoji': '🏺',
        'difficulty': 'easy',
        'total_questions': 28,
        'sections': {
            1: {
                'title': 'Part 1: Ancient Egypt Basics',
                'questions': [
                    {
                        'number': 1,
                        'text': 'Which river was most important to Ancient Egypt?',
                        'options': [
                            {'letter': 'A', 'text': 'The Nile River'},
                            {'letter': 'B', 'text': 'The Tigris River'},
                            {'letter': 'C', 'text': 'The Euphrates River'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'About how long ago did Ancient Egypt exist?',
                        'options': [
                            {'letter': 'A', 'text': '1,500 years ago'},
                            {'letter': 'B', 'text': 'Over 3,000 years ago'},
                            {'letter': 'C', 'text': '2,000 years ago'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'What was the ruler of Ancient Egypt called?',
                        'options': [
                            {'letter': 'A', 'text': 'King'},
                            {'letter': 'B', 'text': 'Pharaoh'},
                            {'letter': 'C', 'text': 'Sultan'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'What continent is Egypt located on?',
                        'options': [
                            {'letter': 'A', 'text': 'Africa'},
                            {'letter': 'B', 'text': 'Asia'},
                            {'letter': 'C', 'text': 'Middle East'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'What was the main food that Ancient Egyptians grew?',
                        'options': [
                            {'letter': 'A', 'text': 'Wheat and barley'},
                            {'letter': 'B', 'text': 'Millet'},
                            {'letter': 'C', 'text': 'Oats'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'Why was the Nile River so important to Ancient Egyptians?',
                        'options': [
                            {'letter': 'A', 'text': 'It flooded every year and made the soil good for farming'},
                            {'letter': 'B', 'text': 'It provided the only source of water'},
                            {'letter': 'C', 'text': 'It was used for transportation only'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: Pyramids and Tombs',
                'questions': [
                    {
                        'number': 7,
                        'text': 'What were pyramids built for?',
                        'options': [
                            {'letter': 'A', 'text': 'As tombs for pharaohs'},
                            {'letter': 'B', 'text': 'As temples for the gods'},
                            {'letter': 'C', 'text': 'As storage buildings'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'Where are the most famous pyramids located?',
                        'options': [
                            {'letter': 'A', 'text': 'Luxor'},
                            {'letter': 'B', 'text': 'Giza'},
                            {'letter': 'C', 'text': 'Thebes'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'What is the Great Sphinx?',
                        'options': [
                            {'letter': 'A', 'text': 'A type of temple'},
                            {'letter': 'B', 'text': 'A statue with a lion body and human head'},
                            {'letter': 'C', 'text': 'A type of tomb'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What were pyramids made out of?',
                        'options': [
                            {'letter': 'A', 'text': 'Sandstone'},
                            {'letter': 'B', 'text': 'Clay bricks'},
                            {'letter': 'C', 'text': 'Large stone blocks'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'Why did pharaohs want to be buried in pyramids?',
                        'options': [
                            {'letter': 'A', 'text': 'They believed it would help them in the afterlife'},
                            {'letter': 'B', 'text': 'They wanted to be closer to the gods'},
                            {'letter': 'C', 'text': 'It showed their power and wealth'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'What shape are the sides of a pyramid?',
                        'options': [
                            {'letter': 'A', 'text': 'Rectangles'},
                            {'letter': 'B', 'text': 'Circles'},
                            {'letter': 'C', 'text': 'Triangles'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Part 3: Daily Life in Ancient Egypt',
                'questions': [
                    {
                        'number': 13,
                        'text': 'What did Ancient Egyptians write on?',
                        'options': [
                            {'letter': 'A', 'text': 'Papyrus (made from a plant)'},
                            {'letter': 'B', 'text': 'Parchment'},
                            {'letter': 'C', 'text': 'Clay tablets'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'What was the Ancient Egyptian writing system called?',
                        'options': [
                            {'letter': 'A', 'text': 'Hieroglyphics'},
                            {'letter': 'B', 'text': 'Cuneiform'},
                            {'letter': 'C', 'text': 'Latin'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What did most Ancient Egyptian children do?',
                        'options': [
                            {'letter': 'A', 'text': 'Went to school all day'},
                            {'letter': 'B', 'text': 'Helped their parents with farming and crafts'},
                            {'letter': 'C', 'text': 'Learned to read and write'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'What did Ancient Egyptians eat a lot of?',
                        'options': [
                            {'letter': 'A', 'text': 'Bread, fish, and vegetables'},
                            {'letter': 'B', 'text': 'Meat and cheese'},
                            {'letter': 'C', 'text': 'Fruits and nuts'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'What did Ancient Egyptians use to make their clothes?',
                        'options': [
                            {'letter': 'A', 'text': 'Linen (made from flax plants)'},
                            {'letter': 'B', 'text': 'Wool'},
                            {'letter': 'C', 'text': 'Silk'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'What did Ancient Egyptians use to keep cool in the hot sun?',
                        'options': [
                            {'letter': 'A', 'text': 'They built houses with thick walls'},
                            {'letter': 'B', 'text': 'They swam all day'},
                            {'letter': 'C', 'text': 'They wore light clothing and stayed in the shade'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Part 4: Mummies and the Afterlife',
                'questions': [
                    {
                        'number': 19,
                        'text': 'What is a mummy?',
                        'options': [
                            {'letter': 'A', 'text': 'A preserved dead body wrapped in cloth'},
                            {'letter': 'B', 'text': 'A type of tomb'},
                            {'letter': 'C', 'text': 'A type of coffin'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'Why did Ancient Egyptians make mummies?',
                        'options': [
                            {'letter': 'A', 'text': 'To honor the dead'},
                            {'letter': 'B', 'text': 'They believed the body needed to be preserved for the afterlife'},
                            {'letter': 'C', 'text': 'To prevent disease'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'What did Ancient Egyptians put inside the mummy wrappings?',
                        'options': [
                            {'letter': 'A', 'text': 'Special items and amulets for protection'},
                            {'letter': 'B', 'text': 'Jewelry and gold'},
                            {'letter': 'C', 'text': 'Tools and weapons'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'Where were mummies usually placed?',
                        'options': [
                            {'letter': 'A', 'text': 'In temples'},
                            {'letter': 'B', 'text': 'In gardens'},
                            {'letter': 'C', 'text': 'In tombs or pyramids'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'What did Ancient Egyptians believe happened after death?',
                        'options': [
                            {'letter': 'A', 'text': 'They would go to an afterlife if they lived a good life'},
                            {'letter': 'B', 'text': 'They would become gods'},
                            {'letter': 'C', 'text': 'They would be reborn as humans'}
                        ]
                    }
                ]
            },
            5: {
                'title': 'Part 5: Gods and Goddesses',
                'questions': [
                    {
                        'number': 24,
                        'text': 'Who was the sun god in Ancient Egypt?',
                        'options': [
                            {'letter': 'A', 'text': 'Horus'},
                            {'letter': 'B', 'text': 'Anubis'},
                            {'letter': 'C', 'text': 'Ra'}
                        ]
                    },
                    {
                        'number': 25,
                        'text': 'Which god had the head of a jackal and was the god of mummification?',
                        'options': [
                            {'letter': 'A', 'text': 'Osiris'},
                            {'letter': 'B', 'text': 'Anubis'},
                            {'letter': 'C', 'text': 'Set'}
                        ]
                    },
                    {
                        'number': 26,
                        'text': 'Who was the goddess of love and beauty?',
                        'options': [
                            {'letter': 'A', 'text': 'Isis'},
                            {'letter': 'B', 'text': 'Hathor'},
                            {'letter': 'C', 'text': 'Sekhmet'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'What animal was often associated with the goddess Bastet?',
                        'options': [
                            {'letter': 'A', 'text': 'A lion'},
                            {'letter': 'B', 'text': 'A bird'},
                            {'letter': 'C', 'text': 'A cat'}
                        ]
                    },
                    {
                        'number': 28,
                        'text': 'What did Ancient Egyptians believe their gods controlled?',
                        'options': [
                            {'letter': 'A', 'text': 'Things like the sun, the Nile River, and the afterlife'},
                            {'letter': 'B', 'text': 'Only the harvest'},
                            {'letter': 'C', 'text': 'Only the afterlife'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {
            1: """
                <h2>Ancient Egypt Basics 🏺</h2>
                <p>Ancient Egypt was one of the most amazing civilizations in history! It existed for over 3,000 years, starting around 3,100 BC. That's a very, very long time ago - even before the Vikings!</p>
                
                <p>The most important thing about Ancient Egypt was the Nile River. This huge river flows through Egypt and was like a lifeline for the people. Every year, the Nile would flood, bringing rich, dark soil called silt to the land. This made the soil perfect for growing crops like wheat and barley. Without the Nile, there would have been no Ancient Egypt!</p>
                
                <p>The ruler of Ancient Egypt was called a pharaoh. The pharaoh was not just a king - Ancient Egyptians believed the pharaoh was actually a god on Earth! The pharaoh had complete power and was responsible for everything in the kingdom. People had to bow down and show great respect to the pharaoh.</p>
                
                <p>Ancient Egypt was located in Africa, in the northeastern part of the continent. Most of Egypt is desert, which is very hot and dry. But along the Nile River, there was a narrow strip of green, fertile land where people could live and farm. This is why almost all Ancient Egyptian cities were built near the Nile!</p>
                
                <p>The Ancient Egyptians were very smart and organized. They built amazing structures, created beautiful art, and developed a system of writing. They also believed strongly in the afterlife and spent a lot of time preparing for what they thought would happen after death.</p>
            """,
            2: """
                <h2>Pyramids and Tombs 🏗️</h2>
                <p>Pyramids are probably the most famous thing about Ancient Egypt! These huge triangular structures were built as tombs for pharaohs. The Ancient Egyptians believed that when a pharaoh died, they would need their body and treasures in the afterlife, so they built these massive pyramids to protect everything.</p>
                
                <p>The most famous pyramids are located at Giza, near the modern city of Cairo. The Great Pyramid of Giza is one of the Seven Wonders of the Ancient World and is still standing today! It was built for a pharaoh named Khufu around 4,500 years ago. The pyramid is made of over 2 million stone blocks, and each block weighs as much as a car!</p>
                
                <p>Building a pyramid was an enormous job that took thousands of workers many years to complete. Workers had to cut huge stones from quarries, drag them to the building site, and carefully place them one on top of another. There were no cranes or trucks - everything was done by hand or with simple tools!</p>
                
                <p>Near the pyramids at Giza stands the Great Sphinx, a huge statue with the body of a lion and the head of a human (probably a pharaoh). The Sphinx is about 240 feet long and 66 feet tall - that's as tall as a 6-story building! It was carved from one giant piece of limestone rock.</p>
                
                <p>Pyramids were designed to be very hard to get into. They had secret passages, false doors, and traps to keep robbers away from the pharaoh's treasures. However, most pyramids were still robbed over the centuries. The pharaohs' treasures and mummies were often stolen, which is why we don't find many mummies in pyramids today.</p>
            """,
            3: """
                <h2>Daily Life in Ancient Egypt 🏠</h2>
                <p>Most Ancient Egyptians were farmers. They worked very hard growing crops like wheat, barley, vegetables, and fruits. They also raised animals like cattle, sheep, goats, and pigs. Farming was done by hand with simple tools, and everyone in the family helped out, including children!</p>
                
                <p>Ancient Egyptians were one of the first people to invent writing. Their writing system was called hieroglyphics, which used pictures and symbols instead of letters. There were over 700 different hieroglyphic symbols! They wrote on a material called papyrus, which was made from a plant that grew along the Nile River. Papyrus was like paper, but it was made by flattening and drying strips of the papyrus plant.</p>
                
                <p>Children in Ancient Egypt didn't go to school like we do today. Most children learned skills from their parents - boys learned their father's job (like farming or crafting), and girls learned from their mothers (like cooking and weaving). Only children from wealthy families, especially boys, might learn to read and write hieroglyphics.</p>
                
                <p>Ancient Egyptians ate a lot of bread - it was their main food! They also ate fish from the Nile, vegetables like onions and garlic, fruits like dates and figs, and sometimes meat. They drank beer (even children drank a weak version) and water. They didn't have sugar, so they used honey to sweeten things.</p>
                
                <p>Clothing was made from linen, which came from flax plants. Linen is a light, cool fabric that was perfect for the hot Egyptian climate. Most people wore simple white clothes, while pharaohs and wealthy people wore more elaborate, colorful clothing with jewelry. Both men and women wore makeup, especially dark eye makeup called kohl, which they believed protected their eyes from the sun!</p>
            """,
            4: """
                <h2>Mummies and the Afterlife 💀</h2>
                <p>Ancient Egyptians had very strong beliefs about what happened after death. They believed that when a person died, their spirit would travel to the afterlife, but only if their body was preserved. This is why they created mummies - preserved dead bodies wrapped in cloth.</p>
                
                <p>The process of making a mummy was very complicated and took about 70 days! First, special priests would remove the person's internal organs (like the heart, liver, and lungs) and preserve them in special jars. Then they would dry out the body using a special salt called natron. After the body was completely dry, they would wrap it in hundreds of yards of linen cloth strips. Sometimes they would put a mask over the face that looked like the person when they were alive.</p>
                
                <p>Inside the mummy wrappings, priests would place special items like amulets (small charms) for protection, jewelry, and sometimes even small statues. They believed these items would help the person in the afterlife. The most important organ was the heart - Ancient Egyptians believed the heart would be weighed against a feather in the afterlife to see if the person had been good or bad!</p>
                
                <p>Mummies were placed in tombs (underground rooms) or pyramids along with everything the person might need in the afterlife - food, furniture, clothes, and treasures. The Ancient Egyptians believed the person's spirit could use these things in the afterlife. They also wrote spells and prayers on the tomb walls to help guide the spirit.</p>
                
                <p>Not everyone could afford to be mummified - it was very expensive! Usually only pharaohs, wealthy people, and sometimes important animals (like cats, which were considered sacred) were mummified. Regular people were simply buried in the sand, which naturally preserved some bodies because the dry desert sand acted like the mummification process.</p>
            """,
            5: """
                <h2>Gods and Goddesses ⚡</h2>
                <p>Ancient Egyptians believed in many gods and goddesses who controlled different parts of the world. They thought these gods looked like humans but with animal heads, or sometimes like animals. There were hundreds of different gods!</p>
                
                <p>The most important god was Ra (or Re), the sun god. Ancient Egyptians believed that Ra traveled across the sky in a boat during the day, bringing light to the world. At night, he would travel through the underworld. Ra was often shown with the head of a falcon and a sun disk on his head. Without Ra, there would be no sun, no crops, and no life!</p>
                
                <p>Anubis was the god of mummification and the dead. He had the head of a jackal (a wild dog) and was responsible for protecting the dead and helping with the mummification process. Ancient Egyptians believed Anubis would guide souls to the afterlife and weigh their hearts to see if they had been good.</p>
                
                <p>Isis was a very important goddess - she was the goddess of magic, healing, and protection. She was also the wife of Osiris (god of the afterlife) and the mother of Horus (god of the sky). Isis was known for being very powerful and protective, especially of children and the dead.</p>
                
                <p>Bastet was the goddess of cats, protection, and joy. She was often shown as a woman with a cat's head, or sometimes as a cat. Ancient Egyptians loved cats and believed they were sacred animals. They even mummified cats when they died! Bastet was thought to protect homes and bring happiness.</p>
                
                <p>Ancient Egyptians built huge temples for their gods and made offerings (gifts) to them every day. They believed that if they didn't honor the gods, bad things would happen - the Nile might not flood, crops might not grow, or the sun might not rise. The gods were a very important part of everyday life!</p>
            """
        },
        'correct_answers': {
            1: 'A', 2: 'B', 3: 'B', 4: 'A', 5: 'A', 6: 'A',
            7: 'A', 8: 'B', 9: 'B', 10: 'C', 11: 'A', 12: 'C',
            13: 'A', 14: 'A', 15: 'B', 16: 'A', 17: 'A', 18: 'C',
            19: 'A', 20: 'B', 21: 'A', 22: 'C', 23: 'A',
            24: 'C', 25: 'B', 26: 'B', 27: 'C', 28: 'A'
        }
    },
    'ancient-egypt-medium': {
        'name': 'Ancient Egypt Advanced',
        'title': 'Ancient Egypt Quiz - Medium',
        'description': 'Explore deeper into pharaohs, dynasties, and ancient Egyptian culture!',
        'emoji': '🏛️',
        'difficulty': 'medium',
        'total_questions': 28,
        'sections': {
            1: {
                'title': 'Part 1: Pharaohs and Dynasties',
                'questions': [
                    {
                        'number': 1,
                        'text': 'Who was the first pharaoh to unite Upper and Lower Egypt?',
                        'options': [
                            {'letter': 'A', 'text': 'Menes (also called Narmer)'},
                            {'letter': 'B', 'text': 'Ramses II'},
                            {'letter': 'C', 'text': 'Tutankhamun'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'Which female pharaoh ruled as a full pharaoh and built many monuments?',
                        'options': [
                            {'letter': 'A', 'text': 'Cleopatra'},
                            {'letter': 'B', 'text': 'Hatshepsut'},
                            {'letter': 'C', 'text': 'Nefertiti'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'What were the three main periods of Ancient Egyptian history called?',
                        'options': [
                            {'letter': 'A', 'text': 'Early Period, Golden Age, and Late Period'},
                            {'letter': 'B', 'text': 'First Dynasty, Second Dynasty, and Third Dynasty'},
                            {'letter': 'C', 'text': 'Old Kingdom, Middle Kingdom, and New Kingdom'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'Which pharaoh is famous for building the Great Pyramid of Giza?',
                        'options': [
                            {'letter': 'A', 'text': 'Ramses II'},
                            {'letter': 'B', 'text': 'Tutankhamun'},
                            {'letter': 'C', 'text': 'Khufu (also called Cheops)'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'What was the name of the boy pharaoh whose tomb was discovered almost completely intact?',
                        'options': [
                            {'letter': 'A', 'text': 'Amenhotep III'},
                            {'letter': 'B', 'text': 'Tutankhamun'},
                            {'letter': 'C', 'text': 'Thutmose III'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'Which pharaoh tried to change Egypt\'s religion to worship only one god?',
                        'options': [
                            {'letter': 'A', 'text': 'Ramses II'},
                            {'letter': 'B', 'text': 'Cleopatra'},
                            {'letter': 'C', 'text': 'Akhenaten'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: Architecture and Monuments',
                'questions': [
                    {
                        'number': 7,
                        'text': 'What is the name of the massive stone structure with a lion body and human head near the pyramids?',
                        'options': [
                            {'letter': 'A', 'text': 'The Colossus'},
                            {'letter': 'B', 'text': 'The Great Sphinx'},
                            {'letter': 'C', 'text': 'The Obelisk'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'What were the tall, pointed stone monuments called that were often placed in pairs at temple entrances?',
                        'options': [
                            {'letter': 'A', 'text': 'Stelae'},
                            {'letter': 'B', 'text': 'Pylons'},
                            {'letter': 'C', 'text': 'Obelisks'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'What was the purpose of the Valley of the Kings?',
                        'options': [
                            {'letter': 'A', 'text': 'A place where battles were fought'},
                            {'letter': 'B', 'text': 'A market where goods were traded'},
                            {'letter': 'C', 'text': 'A hidden valley where pharaohs were buried in tombs'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What architectural feature did Ancient Egyptians use to support heavy stone roofs?',
                        'options': [
                            {'letter': 'A', 'text': 'Wooden beams'},
                            {'letter': 'B', 'text': 'Metal supports'},
                            {'letter': 'C', 'text': 'Massive stone columns'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'What was the name of the ancient Egyptian capital city during the Old Kingdom?',
                        'options': [
                            {'letter': 'A', 'text': 'Thebes'},
                            {'letter': 'B', 'text': 'Alexandria'},
                            {'letter': 'C', 'text': 'Memphis'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'What were the large stone blocks used to build pyramids called?',
                        'options': [
                            {'letter': 'A', 'text': 'Megaliths'},
                            {'letter': 'B', 'text': 'Limestone blocks'},
                            {'letter': 'C', 'text': 'Granite slabs'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Part 3: Religion and Gods',
                'questions': [
                    {
                        'number': 13,
                        'text': 'What was the name of the ancient Egyptian book that contained spells and prayers for the afterlife?',
                        'options': [
                            {'letter': 'A', 'text': 'The Pyramid Texts'},
                            {'letter': 'B', 'text': 'The Coffin Texts'},
                            {'letter': 'C', 'text': 'The Book of the Dead'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'Which god was the ruler of the underworld and judge of the dead?',
                        'options': [
                            {'letter': 'A', 'text': 'Anubis'},
                            {'letter': 'B', 'text': 'Set'},
                            {'letter': 'C', 'text': 'Osiris'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What was the ceremony called where a pharaoh\'s heart was weighed against a feather?',
                        'options': [
                            {'letter': 'A', 'text': 'The Judgment of the Dead'},
                            {'letter': 'B', 'text': 'The Trial of Osiris'},
                            {'letter': 'C', 'text': 'The Weighing of the Heart'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'Which god was depicted with the head of a falcon and was the god of the sky?',
                        'options': [
                            {'letter': 'A', 'text': 'Thoth'},
                            {'letter': 'B', 'text': 'Ra'},
                            {'letter': 'C', 'text': 'Horus'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'What was the name of the god of wisdom and writing, often shown with the head of an ibis?',
                        'options': [
                            {'letter': 'A', 'text': 'Ptah'},
                            {'letter': 'B', 'text': 'Khnum'},
                            {'letter': 'C', 'text': 'Thoth'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'Which goddess was the wife of Osiris and mother of Horus?',
                        'options': [
                            {'letter': 'A', 'text': 'Hathor'},
                            {'letter': 'B', 'text': 'Bastet'},
                            {'letter': 'C', 'text': 'Isis'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Part 4: Writing and Knowledge',
                'questions': [
                    {
                        'number': 19,
                        'text': 'What was the simplified form of hieroglyphics used for everyday writing called?',
                        'options': [
                            {'letter': 'A', 'text': 'Demotic script'},
                            {'letter': 'B', 'text': 'Cursive hieroglyphics'},
                            {'letter': 'C', 'text': 'Hieratic script'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'What famous stone helped scholars finally understand hieroglyphics?',
                        'options': [
                            {'letter': 'A', 'text': 'The Black Stone'},
                            {'letter': 'B', 'text': 'The Sphinx Stone'},
                            {'letter': 'C', 'text': 'The Rosetta Stone'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'What were the ancient Egyptian priests who could read and write called?',
                        'options': [
                            {'letter': 'A', 'text': 'Scholars'},
                            {'letter': 'B', 'text': 'Writers'},
                            {'letter': 'C', 'text': 'Scribes'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What was the name of the plant used to make papyrus?',
                        'options': [
                            {'letter': 'A', 'text': 'Nile reed'},
                            {'letter': 'B', 'text': 'Egyptian grass'},
                            {'letter': 'C', 'text': 'Cyperus papyrus'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'What did Ancient Egyptians use to write with on papyrus?',
                        'options': [
                            {'letter': 'A', 'text': 'Quill pens'},
                            {'letter': 'B', 'text': 'Stylus'},
                            {'letter': 'C', 'text': 'Reed brushes and ink'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'What were the earliest religious texts carved on pyramid walls called?',
                        'options': [
                            {'letter': 'A', 'text': 'Temple Inscriptions'},
                            {'letter': 'B', 'text': 'Royal Decrees'},
                            {'letter': 'C', 'text': 'Pyramid Texts'}
                        ]
                    }
                ]
            },
            5: {
                'title': 'Part 5: Society and Daily Life',
                'questions': [
                    {
                        'number': 25,
                        'text': 'What was the social class of skilled workers like craftsmen and artists called?',
                        'options': [
                            {'letter': 'A', 'text': 'Merchants'},
                            {'letter': 'B', 'text': 'Farmers'},
                            {'letter': 'C', 'text': 'Artisans'}
                        ]
                    },
                    {
                        'number': 26,
                        'text': 'What was the name of the Ancient Egyptian unit of measurement based on the length from elbow to fingertips?',
                        'options': [
                            {'letter': 'A', 'text': 'Palm'},
                            {'letter': 'B', 'text': 'Span'},
                            {'letter': 'C', 'text': 'Cubit'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'What was the main crop that Ancient Egyptians used to make bread and beer?',
                        'options': [
                            {'letter': 'A', 'text': 'Rice'},
                            {'letter': 'B', 'text': 'Corn'},
                            {'letter': 'C', 'text': 'Emmer wheat and barley'}
                        ]
                    },
                    {
                        'number': 28,
                        'text': 'What was the name of the Ancient Egyptian calendar that had 365 days?',
                        'options': [
                            {'letter': 'A', 'text': 'The lunar calendar'},
                            {'letter': 'B', 'text': 'The solar calendar'},
                            {'letter': 'C', 'text': 'The civil calendar'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {
            1: """
                <h2>Pharaohs and Dynasties 👑</h2>
                <p>Ancient Egypt was ruled by pharaohs for over 3,000 years! The first pharaoh to unite Upper and Lower Egypt was Menes (also called Narmer), who ruled around 3100 BC. This unification marked the beginning of Ancient Egypt as a single kingdom. Menes established the first dynasty and built the capital city of Memphis.</p>
                
                <p>Ancient Egyptian history is divided into three main periods: the Old Kingdom (2686-2181 BC), the Middle Kingdom (2055-1650 BC), and the New Kingdom (1550-1069 BC). Each period had its own characteristics and achievements. The Old Kingdom is famous for building the great pyramids, the Middle Kingdom was a time of expansion and prosperity, and the New Kingdom was the age of empire and great pharaohs like Ramses II.</p>
                
                <p>One of the most famous pharaohs was Hatshepsut, who was one of the few female pharaohs. She ruled for about 20 years during the New Kingdom and was known for her successful trade expeditions and building projects. She even had herself depicted as a male pharaoh in many statues and carvings!</p>
                
                <p>Khufu (also called Cheops) was the pharaoh who built the Great Pyramid of Giza, one of the Seven Wonders of the Ancient World. This massive structure took about 20 years to build and used over 2 million stone blocks!</p>
                
                <p>Tutankhamun became famous not because of his achievements as pharaoh (he died very young), but because his tomb was discovered in 1922 almost completely intact, filled with amazing treasures. This discovery gave us incredible insights into how pharaohs were buried.</p>
                
                <p>One of the most unusual pharaohs was Akhenaten, who tried to change Egypt's religion from worshiping many gods to worshiping only one god, the Aten (the sun disk). This was very controversial, and after his death, Egypt returned to worshiping many gods again.</p>
            """,
            2: """
                <h2>Architecture and Monuments 🏗️</h2>
                <p>Ancient Egyptians were master builders! The Great Sphinx is a massive statue with the body of a lion and the head of a human (probably a pharaoh). It stands near the pyramids at Giza and is about 240 feet long and 66 feet tall. The Sphinx was carved from one giant piece of limestone rock and is one of the world's oldest and largest statues!</p>
                
                <p>Obelisks were tall, pointed stone monuments that Ancient Egyptians placed in pairs at temple entrances. They were made from a single piece of stone and could be over 100 feet tall! Obelisks were often covered in hieroglyphics and had a gold cap on top that would shine in the sunlight. Many obelisks were later taken to other countries and can still be seen in places like Rome, Paris, and New York!</p>
                
                <p>The Valley of the Kings was a hidden valley in the desert where pharaohs of the New Kingdom were buried. Instead of building pyramids (which were too easy for robbers to find), pharaohs had their tombs carved deep into the rock of this valley. The tombs were filled with treasures, but unfortunately, most were robbed over the centuries. The tomb of Tutankhamun was one of the few that remained mostly untouched!</p>
                
                <p>Ancient Egyptian temples used massive stone columns to support heavy stone roofs. These columns were often decorated with carvings and paintings. Some columns were shaped like plants, such as papyrus or lotus flowers. The columns were so large and heavy that they required incredible engineering skill to build!</p>
                
                <p>Memphis was the capital city during the Old Kingdom and was located near modern-day Cairo. It was a huge city with many temples, palaces, and workshops. The city was so important that its name became the word for Egypt in many ancient languages!</p>
                
                <p>Pyramids were built using limestone blocks that were cut from quarries and dragged to the building site. The largest blocks weighed as much as a car! Workers had to cut these blocks perfectly so they would fit together without gaps. The outer layer of the pyramids was made from fine white limestone that would have shone brightly in the sun!</p>
            """,
            3: """
                <h2>Religion and Gods ⚡</h2>
                <p>The Book of the Dead was a collection of spells, prayers, and instructions that Ancient Egyptians believed would help the dead person's spirit navigate the afterlife. It wasn't actually a single book, but rather a collection of texts that could be customized for each person. Copies were often written on papyrus and placed in tombs, or painted on tomb walls.</p>
                
                <p>Osiris was one of the most important gods - he was the god of the underworld and the judge of the dead. According to legend, Osiris was killed by his brother Set, but was brought back to life by his wife Isis. However, he could no longer rule the living world, so he became the ruler of the afterlife. Osiris was always shown as a mummy, wrapped in white cloth.</p>
                
                <p>The Weighing of the Heart ceremony was a crucial part of the Ancient Egyptian belief about the afterlife. When a person died, their heart was weighed against a feather (representing truth and justice) on a scale. If the heart was lighter than the feather, the person could enter the afterlife. If it was heavier (because of bad deeds), a monster would eat the heart and the person would cease to exist!</p>
                
                <p>Horus was the god of the sky, often shown with the head of a falcon. He was the son of Osiris and Isis, and was one of the most important gods. The pharaoh was believed to be the living embodiment of Horus on Earth. Horus was also associated with protection and was often shown with the "Eye of Horus," which was a symbol of protection and healing.</p>
                
                <p>Thoth was the god of wisdom, writing, and knowledge. He was usually shown with the head of an ibis (a type of bird) or sometimes as a baboon. Thoth was believed to have invented writing and was the scribe of the gods. He was also associated with the moon and was said to measure time.</p>
                
                <p>Isis was one of the most important goddesses. She was the wife of Osiris and the mother of Horus. Isis was known for her magic and was believed to be very powerful. She was often shown with a throne-shaped headdress or with wings spread protectively. Isis was associated with protection, healing, and motherhood, and was one of the most widely worshiped goddesses in Ancient Egypt.</p>
            """,
            4: """
                <h2>Writing and Knowledge 📜</h2>
                <p>Hieroglyphics were the formal writing system of Ancient Egypt, but they were very complex and time-consuming to write. For everyday use, scribes developed hieratic script, which was a simplified, cursive form of hieroglyphics. Hieratic was much faster to write and was used for business documents, letters, and other everyday writing. It was written from right to left, usually with a reed brush on papyrus.</p>
                
                <p>The Rosetta Stone was discovered in 1799 and was the key to understanding hieroglyphics! The stone had the same text written in three different scripts: hieroglyphics, demotic (another Egyptian script), and Greek. Because scholars could read Greek, they were finally able to figure out what the hieroglyphics meant. This discovery opened up the entire world of Ancient Egyptian writing!</p>
                
                <p>Scribes were highly respected members of Ancient Egyptian society. They were the only people (besides priests) who could read and write. Scribes went to special schools for many years to learn hieroglyphics and hieratic script. They worked for the government, temples, and wealthy people, keeping records, writing letters, and copying important texts. Being a scribe was one of the best jobs in Ancient Egypt!</p>
                
                <p>Papyrus was made from the Cyperus papyrus plant, which grew along the banks of the Nile River. To make papyrus, workers would cut the stems of the plant into thin strips, lay them out in two layers (one horizontal, one vertical), press them together, and let them dry. The natural sap in the plant would glue the strips together, creating a smooth writing surface. Papyrus was so important that the word "paper" comes from "papyrus"!</p>
                
                <p>Ancient Egyptians wrote with reed brushes made from reeds that grew along the Nile. They would cut one end of the reed at an angle to create a brush tip. For ink, they used a mixture of water, gum, and soot (for black) or other natural materials for colors. They would dip their brush in the ink and write on papyrus. Scribes often carried their writing tools in a special case.</p>
                
                <p>The Pyramid Texts are the oldest religious texts in the world! They were carved on the walls inside pyramids during the Old Kingdom. These texts contained spells and prayers to help the pharaoh's spirit in the afterlife. Later, similar texts were written on coffins (Coffin Texts) and on papyrus (Book of the Dead). These texts give us incredible insight into Ancient Egyptian beliefs about death and the afterlife.</p>
            """,
            5: """
                <h2>Society and Daily Life 🏠</h2>
                <p>Ancient Egyptian society was organized into different social classes. At the top were the pharaoh and royal family, followed by nobles and priests. Below them were artisans - skilled workers like craftsmen, artists, and builders. Artisans were respected because they created beautiful objects and built amazing structures. They included carpenters, potters, jewelers, painters, and sculptors. Many artisans worked on royal projects like building pyramids or decorating tombs.</p>
                
                <p>Ancient Egyptians used a system of measurement based on parts of the human body. The most important unit was the cubit, which was the length from a person's elbow to the tip of their middle finger (about 18-20 inches). The cubit was used to measure everything from building pyramids to measuring land. There were also smaller units like the palm (width of the hand) and the digit (width of a finger).</p>
                
                <p>The main crops in Ancient Egypt were emmer wheat and barley. These grains were used to make bread, which was the most important food in the Egyptian diet. Bread was eaten at every meal! Barley was also used to make beer, which was the most common drink (even children drank a weak version). Ancient Egyptians also grew vegetables like onions, garlic, leeks, and lettuce, and fruits like dates, figs, and grapes.</p>
                
                <p>Ancient Egyptians created one of the first accurate calendars in history! They had a civil calendar with 365 days, divided into 12 months of 30 days each, plus 5 extra days at the end of the year. This calendar was based on the flooding of the Nile River, which happened at the same time every year. The calendar was so accurate that it was only off by about 6 hours per year! The Ancient Egyptians also had a separate lunar calendar for religious festivals.</p>
                
                <p>Life in Ancient Egypt revolved around the Nile River. The river's annual flood brought rich soil that made farming possible. People lived in houses made of mud bricks, which kept them cool in the hot climate. Most people were farmers, but there were also craftsmen, traders, soldiers, and government workers. Children learned their parents' jobs, and only a few (usually boys from wealthy families) learned to read and write.</p>
            """
        },
        'correct_answers': {
            1: 'A', 2: 'B', 3: 'C', 4: 'C', 5: 'B', 6: 'C',
            7: 'B', 8: 'C', 9: 'C', 10: 'C', 11: 'C', 12: 'B',
            13: 'C', 14: 'C', 15: 'C', 16: 'C', 17: 'C', 18: 'C',
            19: 'C', 20: 'C', 21: 'C', 22: 'C', 23: 'C', 24: 'C',
            25: 'C', 26: 'C', 27: 'C', 28: 'C'
        }
    },
    'baghdad-abbasid': {
        'name': 'Baghdad & Abbasid Empire',
        'title': 'Baghdad and the Abbasid Empire Quiz',
        'description': 'Discover the amazing city of Baghdad and the golden age of the Abbasid Empire!',
        'emoji': '🏛️',
        'difficulty': 'medium',
        'total_questions': 30,
        'sections': {
            1: {
                'title': 'Part 1: The Founding of Baghdad',
                'questions': [
                    {
                        'number': 1,
                        'text': 'In what year was the city of Baghdad founded?',
                        'options': [
                            {'letter': 'A', 'text': '762 CE'},
                            {'letter': 'B', 'text': '800 CE'},
                            {'letter': 'C', 'text': '900 CE'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'Which Abbasid caliph founded the city of Baghdad?',
                        'options': [
                            {'letter': 'A', 'text': 'Harun al-Rashid'},
                            {'letter': 'B', 'text': 'Al-Mansur'},
                            {'letter': 'C', 'text': 'Al-Ma\'mun'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'What was the original shape of Baghdad\'s design?',
                        'options': [
                            {'letter': 'A', 'text': 'Square with four gates'},
                            {'letter': 'B', 'text': 'Circular with concentric walls'},
                            {'letter': 'C', 'text': 'Rectangular with parallel streets'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'Why did the Abbasids move their capital from Damascus to Baghdad?',
                        'options': [
                            {'letter': 'A', 'text': 'To escape the cold weather'},
                            {'letter': 'B', 'text': 'To establish a new political and cultural center'},
                            {'letter': 'C', 'text': 'Because Damascus was destroyed'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'Which river runs through Baghdad, making it an important trading center?',
                        'options': [
                            {'letter': 'A', 'text': 'The Nile River'},
                            {'letter': 'B', 'text': 'The Tigris River'},
                            {'letter': 'C', 'text': 'The Euphrates River'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: The Amazing City Architecture',
                'questions': [
                    {
                        'number': 6,
                        'text': 'What was the name of Baghdad\'s original circular design?',
                        'options': [
                            {'letter': 'A', 'text': 'The Round City'},
                            {'letter': 'B', 'text': 'The Square City'},
                            {'letter': 'C', 'text': 'The Triangle City'}
                        ]
                    },
                    {
                        'number': 7,
                        'text': 'What was located at the very center of the Round City?',
                        'options': [
                            {'letter': 'A', 'text': 'A marketplace'},
                            {'letter': 'B', 'text': 'The caliph\'s palace and the main mosque'},
                            {'letter': 'C', 'text': 'A garden'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'How many main gates did the original Round City have?',
                        'options': [
                            {'letter': 'A', 'text': 'Two gates'},
                            {'letter': 'B', 'text': 'Four gates'},
                            {'letter': 'C', 'text': 'Six gates'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'What architectural style became famous during the Abbasid period?',
                        'options': [
                            {'letter': 'A', 'text': 'Gothic style'},
                            {'letter': 'B', 'text': 'Arabesque style with geometric patterns'},
                            {'letter': 'C', 'text': 'Modern style'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What were the walls of Baghdad made from?',
                        'options': [
                            {'letter': 'A', 'text': 'Wood'},
                            {'letter': 'B', 'text': 'Mud bricks and baked bricks'},
                            {'letter': 'C', 'text': 'Stone only'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Part 3: The House of Wisdom',
                'questions': [
                    {
                        'number': 11,
                        'text': 'What was the House of Wisdom?',
                        'options': [
                            {'letter': 'A', 'text': 'The caliph\'s home'},
                            {'letter': 'B', 'text': 'A major library and center for learning and translation'},
                            {'letter': 'C', 'text': 'A marketplace'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'Which caliph is most associated with establishing the House of Wisdom?',
                        'options': [
                            {'letter': 'A', 'text': 'Al-Mansur'},
                            {'letter': 'B', 'text': 'Al-Ma\'mun'},
                            {'letter': 'C', 'text': 'Harun al-Rashid'}
                        ]
                    },
                    {
                        'number': 13,
                        'text': 'What did scholars at the House of Wisdom translate from?',
                        'options': [
                            {'letter': 'A', 'text': 'Only Arabic books'},
                            {'letter': 'B', 'text': 'Greek, Persian, Indian, and other ancient texts'},
                            {'letter': 'C', 'text': 'Only religious texts'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'Why was the House of Wisdom so important?',
                        'options': [
                            {'letter': 'A', 'text': 'It was the tallest building'},
                            {'letter': 'B', 'text': 'It preserved and spread knowledge from many cultures'},
                            {'letter': 'C', 'text': 'It was the biggest marketplace'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What subjects were studied at the House of Wisdom?',
                        'options': [
                            {'letter': 'A', 'text': 'Only religion'},
                            {'letter': 'B', 'text': 'Mathematics, astronomy, medicine, philosophy, and more'},
                            {'letter': 'C', 'text': 'Only art'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Part 4: Daily Life in Baghdad',
                'questions': [
                    {
                        'number': 16,
                        'text': 'What were the busy marketplaces in Baghdad called?',
                        'options': [
                            {'letter': 'A', 'text': 'Malls'},
                            {'letter': 'B', 'text': 'Bazaars or souks'},
                            {'letter': 'C', 'text': 'Stores'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'What could you find in Baghdad\'s bazaars?',
                        'options': [
                            {'letter': 'A', 'text': 'Only food'},
                            {'letter': 'B', 'text': 'Spices, silk, books, jewelry, and goods from all over the world'},
                            {'letter': 'C', 'text': 'Only clothes'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'What was a common material for making beautiful art and decorations?',
                        'options': [
                            {'letter': 'A', 'text': 'Plastic'},
                            {'letter': 'B', 'text': 'Ceramic tiles with colorful patterns'},
                            {'letter': 'C', 'text': 'Wood only'}
                        ]
                    },
                    {
                        'number': 19,
                        'text': 'What was the main language used in Baghdad during the Abbasid period?',
                        'options': [
                            {'letter': 'A', 'text': 'English'},
                            {'letter': 'B', 'text': 'Arabic'},
                            {'letter': 'C', 'text': 'Greek'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'What made Baghdad a great place for people from different cultures to meet?',
                        'options': [
                            {'letter': 'A', 'text': 'It had the best weather'},
                            {'letter': 'B', 'text': 'It was a center of trade and learning where people from many places came'},
                            {'letter': 'C', 'text': 'It was the smallest city'}
                        ]
                    }
                ]
            },
            5: {
                'title': 'Part 5: Trade and Commerce',
                'questions': [
                    {
                        'number': 21,
                        'text': 'Why was Baghdad\'s location on the Tigris River so important?',
                        'options': [
                            {'letter': 'A', 'text': 'It made the city look pretty'},
                            {'letter': 'B', 'text': 'It allowed ships to bring goods from faraway places'},
                            {'letter': 'C', 'text': 'It provided drinking water only'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What valuable goods came to Baghdad from far away?',
                        'options': [
                            {'letter': 'A', 'text': 'Only local products'},
                            {'letter': 'B', 'text': 'Silk from China, spices from India, and goods from many lands'},
                            {'letter': 'C', 'text': 'Only food'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'What did merchants use to buy and sell goods?',
                        'options': [
                            {'letter': 'A', 'text': 'Credit cards'},
                            {'letter': 'B', 'text': 'Coins made of gold and silver'},
                            {'letter': 'C', 'text': 'Paper money'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'What made Baghdad one of the richest cities in the world?',
                        'options': [
                            {'letter': 'A', 'text': 'It had the most people'},
                            {'letter': 'B', 'text': 'It was a major trading center connecting East and West'},
                            {'letter': 'C', 'text': 'It had the biggest buildings'}
                        ]
                    },
                    {
                        'number': 25,
                        'text': 'What was the name of the trade routes that connected Baghdad to other parts of the world?',
                        'options': [
                            {'letter': 'A', 'text': 'The Highway'},
                            {'letter': 'B', 'text': 'The Silk Road and other trade routes'},
                            {'letter': 'C', 'text': 'The River Road'}
                        ]
                    }
                ]
            },
            6: {
                'title': 'Part 6: Science and Achievements',
                'questions': [
                    {
                        'number': 26,
                        'text': 'What period is the Abbasid era often called?',
                        'options': [
                            {'letter': 'A', 'text': 'The Dark Ages'},
                            {'letter': 'B', 'text': 'The Islamic Golden Age'},
                            {'letter': 'C', 'text': 'The Modern Age'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'What important mathematical concept did scholars in Baghdad help develop?',
                        'options': [
                            {'letter': 'A', 'text': 'Only addition'},
                            {'letter': 'B', 'text': 'Algebra and the number zero'},
                            {'letter': 'C', 'text': 'Only counting'}
                        ]
                    },
                    {
                        'number': 28,
                        'text': 'What did astronomers in Baghdad study?',
                        'options': [
                            {'letter': 'A', 'text': 'Only the sun'},
                            {'letter': 'B', 'text': 'The stars, planets, and movements in the sky'},
                            {'letter': 'C', 'text': 'Only the moon'}
                        ]
                    },
                    {
                        'number': 29,
                        'text': 'What did doctors in Baghdad help improve?',
                        'options': [
                            {'letter': 'A', 'text': 'Only surgery'},
                            {'letter': 'B', 'text': 'Medical knowledge, hospitals, and treatments'},
                            {'letter': 'C', 'text': 'Only medicine for animals'}
                        ]
                    },
                    {
                        'number': 30,
                        'text': 'Why is the Abbasid period so important in history?',
                        'options': [
                            {'letter': 'A', 'text': 'It had the biggest armies'},
                            {'letter': 'B', 'text': 'It was a time of great learning, science, and cultural achievements'},
                            {'letter': 'C', 'text': 'It lasted the longest'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {
            1: """
                <h2>The Founding of Baghdad 🏗️</h2>
                <p>Baghdad was founded in <strong>762 CE</strong> by the Abbasid caliph <strong>Al-Mansur</strong>. The Abbasids had just taken control of the Islamic empire and wanted to build a new capital city that would be their own. They chose a perfect spot on the <strong>Tigris River</strong> in what is now Iraq.</p>
                
                <p>Al-Mansur wanted Baghdad to be a symbol of the new Abbasid dynasty's power and greatness. He carefully planned the city and chose the location because it was at a crossroads of important trade routes. The Tigris River made it easy for ships to bring goods from faraway places, and the land was fertile for farming.</p>
                
                <p>The original design of Baghdad was <strong>circular</strong> - a perfect circle! This was very unusual for cities at that time. The city had <strong>concentric walls</strong>, which means walls inside walls, like circles within circles. At the very center was the caliph's palace and the main mosque. This design showed that the caliph was the center of power and authority.</p>
                
                <p>Baghdad was built to replace <strong>Damascus</strong> as the capital. The Abbasids wanted to move away from the old Umayyad capital and create something completely new. They wanted Baghdad to be a center of learning, culture, and trade - not just a political capital, but a city that would become famous throughout the world!</p>
                
                <p>The city grew very quickly! Within just a few decades, Baghdad became one of the largest and most important cities in the world. People came from all over to trade, learn, and live in this amazing new city. It became a true center of the Islamic Golden Age!</p>
            """,
            2: """
                <h2>The Amazing City Architecture 🏛️</h2>
                <p>The original Baghdad was called <strong>"The Round City"</strong> or "Madinat al-Salam" (City of Peace) because of its unique circular design. This was one of the most carefully planned cities in history! The city had <strong>four main gates</strong> facing the four directions: north, south, east, and west. Each gate was named and had special meaning.</p>
                
                <p>At the very center of the Round City was the <strong>caliph's palace and the main mosque</strong>. These were the most important buildings, showing that religion and government were at the heart of the city. Around this center, the city was divided into different sections for different purposes - some for markets, some for homes, some for workshops.</p>
                
                <p>The walls of Baghdad were made from <strong>mud bricks and baked bricks</strong>. Mud bricks were made from clay and dried in the sun, while baked bricks were fired in kilns to make them stronger. The walls were thick and tall, designed to protect the city from enemies. The outer wall was especially impressive and could be seen from far away!</p>
                
                <p>Abbasid architecture became famous for its beautiful decorations. Artists created <strong>arabesque patterns</strong> - intricate designs with geometric shapes, flowers, and vines that repeated in beautiful patterns. These patterns decorated buildings, pottery, textiles, and even books. The style was so beautiful that it influenced art for centuries!</p>
                
                <p>As Baghdad grew, it expanded beyond the original Round City. New neighborhoods were built, and the city became a huge metropolis with many districts. But the original Round City remained the heart of Baghdad, showing the vision and planning of its founders. The architecture of Baghdad became a model for other cities throughout the Islamic world!</p>
            """,
            3: """
                <h2>The House of Wisdom 📚</h2>
                <p>The <strong>House of Wisdom</strong> (Bayt al-Hikmah) was one of the most important places in Baghdad! It was a huge library, translation center, and place of learning. Think of it as a combination of a library, university, and research center all in one amazing building!</p>
                
                <p>The House of Wisdom was most strongly supported by <strong>Caliph Al-Ma'mun</strong>, who ruled from 813 to 833 CE. He loved learning and wanted to gather all the knowledge in the world in one place. He sent scholars to faraway lands to find books and bring them back to Baghdad.</p>
                
                <p>One of the most important jobs at the House of Wisdom was <strong>translation</strong>. Scholars translated books from many languages into Arabic. They translated works from <strong>Greek, Persian, Indian, Syriac, and other languages</strong>. This was incredibly important because many ancient Greek texts about science, math, and philosophy might have been lost forever if they hadn't been translated and preserved!</p>
                
                <p>The House of Wisdom wasn't just about storing books - it was a place where scholars <strong>studied, researched, and created new knowledge</strong>. Mathematicians worked on algebra and geometry. Astronomers studied the stars and planets. Doctors learned about medicine and treatments. Philosophers discussed big questions about life and the world.</p>
                
                <p>The House of Wisdom helped make Baghdad the intellectual capital of the world! Scholars from many different places came to study there. They shared ideas, debated, and worked together. This exchange of knowledge led to amazing discoveries and advancements in science, mathematics, medicine, and many other fields. The House of Wisdom was truly a beacon of learning during the Islamic Golden Age!</p>
            """,
            4: """
                <h2>Daily Life in Baghdad 🏙️</h2>
                <p>Life in Baghdad during the Abbasid period was vibrant and exciting! The city was a bustling metropolis where people from many different cultures and backgrounds lived together. <strong>Arabic</strong> was the main language, but you could hear many other languages spoken in the streets as traders and scholars came from all over the world.</p>
                
                <p>The heart of daily life in Baghdad was the <strong>bazaars</strong> (also called souks). These were busy marketplaces where you could buy almost anything! The bazaars were like huge outdoor malls with narrow streets lined with shops. Each area of the bazaar specialized in different goods - one street for spices, another for textiles, another for books, and so on.</p>
                
                <p>In the bazaars, you could find amazing things from all over the world! <strong>Silk from China, spices from India, beautiful ceramics, jewelry, perfumes, books, and so much more</strong>. The bazaars were not just places to shop - they were also social centers where people met, talked, and shared news. Storytellers would entertain crowds, and you could hear music and see performances.</p>
                
                <p>Art and decoration were everywhere in Baghdad! Beautiful <strong>ceramic tiles</strong> with colorful patterns decorated buildings. Textiles with intricate designs were used for clothing and decoration. Calligraphy (beautiful writing) was considered an art form, and skilled calligraphers created stunning works. Even everyday objects were often beautifully decorated.</p>
                
                <p>Baghdad was a true <strong>cosmopolitan city</strong> - a place where people from different cultures, religions, and backgrounds could meet and exchange ideas. Muslims, Christians, Jews, and people of other faiths lived and worked together. Scholars, merchants, artisans, and ordinary people all contributed to making Baghdad a vibrant, exciting place to live. This diversity and exchange of ideas helped make the Islamic Golden Age so special!</p>
            """,
            5: """
                <h2>Trade and Commerce 💰</h2>
                <p>Baghdad's location on the <strong>Tigris River</strong> made it one of the most important trading centers in the world! The river allowed ships to travel and bring goods from faraway places. Baghdad became a hub where trade routes from East and West met, making it incredibly wealthy and important.</p>
                
                <p>Merchants in Baghdad traded in amazing goods from all over the known world! <strong>Silk came from China</strong> along the famous Silk Road. <strong>Spices like pepper, cinnamon, and cloves came from India and Southeast Asia</strong>. Precious metals, gems, textiles, perfumes, books, and exotic foods all flowed through Baghdad's markets. The city was like a giant trading post connecting different parts of the world!</p>
                
                <p>To buy and sell goods, people used <strong>coins made of gold and silver</strong>. The Abbasids minted their own coins, which were accepted throughout their empire and beyond. Having a standard currency made trade much easier - merchants from different places could all use the same coins to do business.</p>
                
                <p>Baghdad's position made it incredibly wealthy. The city sat at the crossroads of major trade routes: the <strong>Silk Road</strong> from the East, routes from Africa, routes from Europe, and sea routes through the Persian Gulf. Merchants from all over the world came to Baghdad to trade. This made the city one of the richest and most prosperous places on Earth!</p>
                
                <p>The wealth from trade helped support the arts, sciences, and learning in Baghdad. Rich merchants and the caliph used their money to build beautiful buildings, support scholars, and create works of art. Trade didn't just bring goods - it also brought ideas, knowledge, and cultural exchange. This made Baghdad not just a trading center, but a center of civilization itself!</p>
            """,
            6: """
                <h2>Science and Achievements 🔬</h2>
                <p>The Abbasid period is often called the <strong>"Islamic Golden Age"</strong> because it was a time of incredible achievements in science, mathematics, medicine, and many other fields. Scholars in Baghdad and throughout the Abbasid Empire made discoveries that changed the world and are still important today!</p>
                
                <p>Mathematics was one of the most important areas of study. Scholars in Baghdad helped develop <strong>algebra</strong> (the word "algebra" actually comes from Arabic!). They also introduced the <strong>number zero</strong> and the decimal system to the Western world. These mathematical concepts are so important that we still use them today in everything from basic math to computers!</p>
                
                <p>Astronomers in Baghdad studied the <strong>stars, planets, and movements in the sky</strong>. They built observatories and created detailed star maps. They improved calendars and could predict eclipses. Their work helped people understand the universe better and improved navigation for traders and travelers. Some of their observations and calculations were so accurate that they're still impressive today!</p>
                
                <p>Medicine was another area where scholars made huge advances. Doctors in Baghdad improved medical knowledge, built <strong>hospitals</strong>, and wrote important medical books. They learned about anatomy, surgery, and treatments for diseases. They also created pharmacies and developed new medicines. Their medical knowledge was the most advanced in the world at that time!</p>
                
                <p>The achievements of the Abbasid period are still important today! The work done by scholars in Baghdad helped preserve ancient knowledge (like Greek science and philosophy) and created new knowledge that spread throughout the world. This period showed how important learning, curiosity, and the exchange of ideas are for human progress. The Islamic Golden Age is a reminder of what people can achieve when they value education and knowledge!</p>
            """
        },
        'correct_answers': {
            1: 'A', 2: 'B', 3: 'B', 4: 'B', 5: 'B',
            6: 'A', 7: 'B', 8: 'B', 9: 'B', 10: 'B',
            11: 'B', 12: 'B', 13: 'B', 14: 'B', 15: 'B',
            16: 'B', 17: 'B', 18: 'B', 19: 'B', 20: 'B',
            21: 'B', 22: 'B', 23: 'B', 24: 'B', 25: 'B',
            26: 'B', 27: 'B', 28: 'B', 29: 'B', 30: 'B'
        }
    },
    'reward-vikings': {
        'name': 'Reward Quizzes',
        'title': 'Reward Quizzes - Vikings',
        'description': 'Test your knowledge! Answer all easy Viking questions without supporting text.',
        'emoji': '🏆',
        'difficulty': 'reward',
        'total_questions': 54,
        'sections': {
            1: {
                'title': 'Part 1: Vikings General Knowledge',
                'questions': [
                    {
                        'number': 1,
                        'text': 'Where did the Vikings come from?',
                        'options': [
                            {'letter': 'A', 'text': 'The Mediterranean region'},
                            {'letter': 'B', 'text': 'Scandinavia (countries like Norway and Sweden)'},
                            {'letter': 'C', 'text': 'Central Europe'}
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
                            {'letter': 'A', 'text': 'Merchants'},
                            {'letter': 'B', 'text': 'Farmers'},
                            {'letter': 'C', 'text': 'Craftsmen'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'What were Viking letters and writing called?',
                        'options': [
                            {'letter': 'A', 'text': 'Latin'},
                            {'letter': 'B', 'text': 'Runes'},
                            {'letter': 'C', 'text': 'Greek'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'Where did Vikings usually carve their writing?',
                        'options': [
                            {'letter': 'A', 'text': 'On parchment'},
                            {'letter': 'B', 'text': 'On stones and wood'},
                            {'letter': 'C', 'text': 'On clay tablets'}
                        ]
                    },
                    {
                        'number': 6,
                        'text': 'What did Vikings use to buy things before they had coins?',
                        'options': [
                            {'letter': 'A', 'text': 'Gold coins'},
                            {'letter': 'B', 'text': 'Silver jewelry (often cut into pieces)'},
                            {'letter': 'C', 'text': 'Bartering (trading goods for goods)'}
                        ]
                    },
                    {
                        'number': 7,
                        'text': 'What were Viking houses called?',
                        'options': [
                            {'letter': 'A', 'text': 'Castles'},
                            {'letter': 'B', 'text': 'Longhouses'},
                            {'letter': 'C', 'text': 'Cottages'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'What were most Viking houses made out of?',
                        'options': [
                            {'letter': 'A', 'text': 'Wood, stone, or turf (grass and dirt)'},
                            {'letter': 'B', 'text': 'Bricks and cement'},
                            {'letter': 'C', 'text': 'Clay and mud'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'Where was the fire usually placed in a Viking house?',
                        'options': [
                            {'letter': 'A', 'text': 'In the fireplace by the wall'},
                            {'letter': 'B', 'text': 'In the middle of the room on the floor'},
                            {'letter': 'C', 'text': 'In a separate kitchen room'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What material were Viking clothes mostly made from?',
                        'options': [
                            {'letter': 'A', 'text': 'Cotton'},
                            {'letter': 'B', 'text': 'Wool and linen'},
                            {'letter': 'C', 'text': 'Leather'}
                        ]
                    },
                    {
                        'number': 11,
                        'text': 'What did Viking children do for fun?',
                        'options': [
                            {'letter': 'A', 'text': 'Played with toys and dolls'},
                            {'letter': 'B', 'text': 'Played board games and wrestled'},
                            {'letter': 'C', 'text': 'Read books'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'Which of these animals did Vikings keep on their farms?',
                        'options': [
                            {'letter': 'A', 'text': 'Horses'},
                            {'letter': 'B', 'text': 'Pigs, sheep, and chickens'},
                            {'letter': 'C', 'text': 'Goats'}
                        ]
                    },
                    {
                        'number': 13,
                        'text': 'What did Vikings eat a lot of?',
                        'options': [
                            {'letter': 'A', 'text': 'Bread and cheese'},
                            {'letter': 'B', 'text': 'Fish and meat stew'},
                            {'letter': 'C', 'text': 'Fruits and vegetables'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'What were the famous Viking boats called?',
                        'options': [
                            {'letter': 'A', 'text': 'Galleys'},
                            {'letter': 'B', 'text': 'Longships'},
                            {'letter': 'C', 'text': 'Skiffs'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What scary animal head was often carved on the front of a Viking ship?',
                        'options': [
                            {'letter': 'A', 'text': 'A dragon or snake'},
                            {'letter': 'B', 'text': 'A wolf'},
                            {'letter': 'C', 'text': 'A bear'}
                        ]
                    },
                    {
                        'number': 16,
                        'text': 'Why did they put dragon heads on their ships?',
                        'options': [
                            {'letter': 'A', 'text': 'To show which family owned the ship'},
                            {'letter': 'B', 'text': 'To scare away enemies and sea monsters'},
                            {'letter': 'C', 'text': 'To honor the gods'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'How did Viking ships move across the water?',
                        'options': [
                            {'letter': 'A', 'text': 'With paddles only'},
                            {'letter': 'B', 'text': 'Using sails and oars (rowing)'},
                            {'letter': 'C', 'text': 'With a sail only'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'Vikings were great explorers. Which faraway place did they reach before Christopher Columbus?',
                        'options': [
                            {'letter': 'A', 'text': 'North America'},
                            {'letter': 'B', 'text': 'South America'},
                            {'letter': 'C', 'text': 'Asia'}
                        ]
                    },
                    {
                        'number': 19,
                        'text': 'How did Vikings find their way at sea?',
                        'options': [
                            {'letter': 'A', 'text': 'They used compasses'},
                            {'letter': 'B', 'text': 'They looked at the sun, stars, and birds'},
                            {'letter': 'C', 'text': 'They followed other ships'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'Did real Viking helmets have horns on them?',
                        'options': [
                            {'letter': 'A', 'text': 'Yes, always'},
                            {'letter': 'B', 'text': 'No, never (that is just a myth!)'},
                            {'letter': 'C', 'text': 'Only for special ceremonies'}
                        ]
                    },
                    {
                        'number': 21,
                        'text': 'What was the Viking\'s most common weapon?',
                        'options': [
                            {'letter': 'A', 'text': 'A sword'},
                            {'letter': 'B', 'text': 'An axe or a spear'},
                            {'letter': 'C', 'text': 'A bow and arrow'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'What did Vikings use to protect themselves in a fight?',
                        'options': [
                            {'letter': 'A', 'text': 'A round wooden shield'},
                            {'letter': 'B', 'text': 'A metal shield'},
                            {'letter': 'C', 'text': 'Armor made of chainmail'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'What was a "Shield Wall"?',
                        'options': [
                            {'letter': 'A', 'text': 'A defensive wall around a village'},
                            {'letter': 'B', 'text': 'When warriors stood close together with shields overlapping'},
                            {'letter': 'C', 'text': 'A formation where shields were stacked'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'What were the very fierce Viking warriors called?',
                        'options': [
                            {'letter': 'A', 'text': 'Berserkers'},
                            {'letter': 'B', 'text': 'Jarls'},
                            {'letter': 'C', 'text': 'Huscarls'}
                        ]
                    },
                    {
                        'number': 25,
                        'text': 'Who was the Viking god of thunder?',
                        'options': [
                            {'letter': 'A', 'text': 'Loki'},
                            {'letter': 'B', 'text': 'Thor'},
                            {'letter': 'C', 'text': 'Odin'}
                        ]
                    },
                    {
                        'number': 26,
                        'text': 'What weapon did Thor carry?',
                        'options': [
                            {'letter': 'A', 'text': 'A magic hammer'},
                            {'letter': 'B', 'text': 'A sword'},
                            {'letter': 'C', 'text': 'An axe'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'Who was the king of all the Viking gods?',
                        'options': [
                            {'letter': 'A', 'text': 'Odin'},
                            {'letter': 'B', 'text': 'Thor'},
                            {'letter': 'C', 'text': 'Tyr'}
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
                            {'letter': 'B', 'text': 'Asgard'},
                            {'letter': 'C', 'text': 'Helheim'}
                        ]
                    },
                    {
                        'number': 30,
                        'text': 'Which day of the week is named after the god Thor?',
                        'options': [
                            {'letter': 'A', 'text': 'Tuesday'},
                            {'letter': 'B', 'text': 'Wednesday'},
                            {'letter': 'C', 'text': 'Thursday (Thor\'s Day)'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Part 2: Viking Shields',
                'questions': [
                    {
                        'number': 31,
                        'text': 'What was the main material used to make Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Metal'},
                            {'letter': 'B', 'text': 'Wood'},
                            {'letter': 'C', 'text': 'Leather'}
                        ]
                    },
                    {
                        'number': 32,
                        'text': 'What type of wood was most commonly used for Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Oak, pine, or linden (lime wood)'},
                            {'letter': 'B', 'text': 'Birch'},
                            {'letter': 'C', 'text': 'Ash'}
                        ]
                    },
                    {
                        'number': 33,
                        'text': 'How thick were most Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'About 1 inch (2-3 cm) thick'},
                            {'letter': 'B', 'text': 'About half an inch (1 cm) thick'},
                            {'letter': 'C', 'text': 'About 2-3 inches (5-7 cm) thick'}
                        ]
                    },
                    {
                        'number': 34,
                        'text': 'What was placed on the front of the shield to make it stronger?',
                        'options': [
                            {'letter': 'A', 'text': 'A layer of leather'},
                            {'letter': 'B', 'text': 'A metal boss (round center piece)'},
                            {'letter': 'C', 'text': 'Metal strips around the edge'}
                        ]
                    },
                    {
                        'number': 35,
                        'text': 'What was the metal boss on a Viking shield used for?',
                        'options': [
                            {'letter': 'A', 'text': 'Just decoration'},
                            {'letter': 'B', 'text': 'Protection and to hold the shield together'},
                            {'letter': 'C', 'text': 'To identify the owner'}
                        ]
                    },
                    {
                        'number': 36,
                        'text': 'What was the handle on a Viking shield usually made from?',
                        'options': [
                            {'letter': 'A', 'text': 'Metal'},
                            {'letter': 'B', 'text': 'Leather or wood'},
                            {'letter': 'C', 'text': 'Rope'}
                        ]
                    },
                    {
                        'number': 37,
                        'text': 'How were the wooden planks for a shield usually arranged?',
                        'options': [
                            {'letter': 'A', 'text': 'Glued together side by side'},
                            {'letter': 'B', 'text': 'Planks placed together and held with glue or nails'},
                            {'letter': 'C', 'text': 'Bound together with leather strips only'}
                        ]
                    },
                    {
                        'number': 38,
                        'text': 'What shape were most Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Square'},
                            {'letter': 'B', 'text': 'Round'},
                            {'letter': 'C', 'text': 'Oval'}
                        ]
                    },
                    {
                        'number': 39,
                        'text': 'How big were Viking shields usually?',
                        'options': [
                            {'letter': 'A', 'text': 'About 2-3 feet (60-90 cm) across'},
                            {'letter': 'B', 'text': 'About 4-5 feet (120-150 cm) across'},
                            {'letter': 'C', 'text': 'About 1 foot (30 cm) across'}
                        ]
                    },
                    {
                        'number': 40,
                        'text': 'What was sometimes added to the edge of a shield?',
                        'options': [
                            {'letter': 'A', 'text': 'A leather rim to protect the edges'},
                            {'letter': 'B', 'text': 'Metal studs'},
                            {'letter': 'C', 'text': 'Decorative carvings'}
                        ]
                    },
                    {
                        'number': 41,
                        'text': 'Why did Vikings make their shields from wood instead of metal?',
                        'options': [
                            {'letter': 'A', 'text': 'Wood was lighter and easier to carry'},
                            {'letter': 'B', 'text': 'Wood was stronger than metal'},
                            {'letter': 'C', 'text': 'Metal was too expensive'}
                        ]
                    },
                    {
                        'number': 42,
                        'text': 'How long did it take to make a Viking shield?',
                        'options': [
                            {'letter': 'A', 'text': 'A skilled craftsman could make one in a few days'},
                            {'letter': 'B', 'text': 'A few hours'},
                            {'letter': 'C', 'text': 'Several weeks'}
                        ]
                    },
                    {
                        'number': 43,
                        'text': 'What did Vikings use to paint their shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Oil-based paints'},
                            {'letter': 'B', 'text': 'Natural paints made from plants, minerals, and animal products'},
                            {'letter': 'C', 'text': 'Dyes made from berries'}
                        ]
                    },
                    {
                        'number': 44,
                        'text': 'What colors were commonly used on Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Red, yellow, black, and white'},
                            {'letter': 'B', 'text': 'Only green'},
                            {'letter': 'C', 'text': 'Brown and gray'}
                        ]
                    },
                    {
                        'number': 45,
                        'text': 'What patterns were often painted on Viking shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Spirals, circles, and geometric shapes'},
                            {'letter': 'B', 'text': 'Animals and birds'},
                            {'letter': 'C', 'text': 'Straight lines and stripes'}
                        ]
                    },
                    {
                        'number': 46,
                        'text': 'Why did Vikings decorate their shields?',
                        'options': [
                            {'letter': 'A', 'text': 'To show which group they belonged to and to look impressive'},
                            {'letter': 'B', 'text': 'To make them stronger'},
                            {'letter': 'C', 'text': 'To honor the gods'}
                        ]
                    },
                    {
                        'number': 47,
                        'text': 'What symbol was sometimes painted on shields?',
                        'options': [
                            {'letter': 'A', 'text': 'Runes (Viking letters) or family symbols'},
                            {'letter': 'B', 'text': 'Crosses'},
                            {'letter': 'C', 'text': 'Stars and moons'}
                        ]
                    },
                    {
                        'number': 48,
                        'text': 'Were all Viking shields decorated the same way?',
                        'options': [
                            {'letter': 'A', 'text': 'No, each shield was unique'},
                            {'letter': 'B', 'text': 'Yes, they all looked the same'},
                            {'letter': 'C', 'text': 'Only shields for leaders had decorations'}
                        ]
                    },
                    {
                        'number': 49,
                        'text': 'How did Vikings hold their shields?',
                        'options': [
                            {'letter': 'A', 'text': 'With one hand using a handle on the back'},
                            {'letter': 'B', 'text': 'With both hands'},
                            {'letter': 'C', 'text': 'With a strap around the arm'}
                        ]
                    },
                    {
                        'number': 50,
                        'text': 'What was a "Shield Wall"?',
                        'options': [
                            {'letter': 'A', 'text': 'A defensive wall around a village'},
                            {'letter': 'B', 'text': 'Warriors standing close together with shields overlapping'},
                            {'letter': 'C', 'text': 'Shields stacked in a pile'}
                        ]
                    },
                    {
                        'number': 51,
                        'text': 'Could Viking shields be used to attack as well as defend?',
                        'options': [
                            {'letter': 'A', 'text': 'Yes, the metal boss could be used to punch'},
                            {'letter': 'B', 'text': 'No, they were only for blocking'},
                            {'letter': 'C', 'text': 'Only the edge could be used to strike'}
                        ]
                    },
                    {
                        'number': 52,
                        'text': 'What happened to shields during battle?',
                        'options': [
                            {'letter': 'A', 'text': 'They could get damaged, broken, or lost'},
                            {'letter': 'B', 'text': 'They never got damaged'},
                            {'letter': 'C', 'text': 'They were always repaired immediately'}
                        ]
                    },
                    {
                        'number': 53,
                        'text': 'How did Vikings carry their shields when not fighting?',
                        'options': [
                            {'letter': 'A', 'text': 'On their back or slung over their shoulder'},
                            {'letter': 'B', 'text': 'In a special bag'},
                            {'letter': 'C', 'text': 'Carried by servants'}
                        ]
                    },
                    {
                        'number': 54,
                        'text': 'Why were shields so important to Viking warriors?',
                        'options': [
                            {'letter': 'A', 'text': 'They were the main protection in battle'},
                            {'letter': 'B', 'text': 'They were required by law'},
                            {'letter': 'C', 'text': 'They showed social status'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {},
        'correct_answers': {
            1: 'B', 2: 'A', 3: 'B', 4: 'B', 5: 'B', 6: 'B',
            7: 'B', 8: 'A', 9: 'B', 10: 'B', 11: 'B', 12: 'B', 13: 'B',
            14: 'B', 15: 'A', 16: 'B', 17: 'B', 18: 'A', 19: 'B',
            20: 'B', 21: 'B', 22: 'A', 23: 'B', 24: 'A',
            25: 'B', 26: 'A', 27: 'A', 28: 'B', 29: 'A', 30: 'C',
            31: 'B', 32: 'A', 33: 'A', 34: 'B', 35: 'B', 36: 'B',
            37: 'B', 38: 'B', 39: 'A', 40: 'A', 41: 'A', 42: 'A',
            43: 'B', 44: 'A', 45: 'A', 46: 'A', 47: 'A', 48: 'A',
            49: 'A', 50: 'B', 51: 'A', 52: 'A', 53: 'A', 54: 'A'
        }
    },
    'assassins-creed-mirage': {
        'name': 'Real People of Assassin\'s Creed Mirage',
        'title': 'Real People of Assassin\'s Creed Mirage',
        'description': 'Learn about the real historical figures featured in Assassin\'s Creed Mirage!',
        'emoji': '🗡️',
        'difficulty': 'medium',
        'total_questions': 35,
        'sections': {
            1: {
                'title': 'Ali ibn Muhammad',
                'questions': [
                    {
                        'number': 1,
                        'text': 'What was Ali ibn Muhammad known for leading?',
                        'options': [
                            {'letter': 'A', 'text': 'A rebellion of enslaved people called the Zanj'},
                            {'letter': 'B', 'text': 'A trade expedition'},
                            {'letter': 'C', 'text': 'A religious pilgrimage'}
                        ]
                    },
                    {
                        'number': 2,
                        'text': 'Which group of people followed him?',
                        'options': [
                            {'letter': 'A', 'text': 'The Zanj (enslaved people from East Africa)'},
                            {'letter': 'B', 'text': 'Merchants and traders'},
                            {'letter': 'C', 'text': 'Religious scholars'}
                        ]
                    },
                    {
                        'number': 3,
                        'text': 'Was he part of the Abbasid government or against it?',
                        'options': [
                            {'letter': 'A', 'text': 'Against it - he led a rebellion'},
                            {'letter': 'B', 'text': 'Part of it - he was a government official'},
                            {'letter': 'C', 'text': 'He worked with the government'}
                        ]
                    },
                    {
                        'number': 4,
                        'text': 'Where did his rebellion mainly take place?',
                        'options': [
                            {'letter': 'A', 'text': 'In southern Iraq, near Basra'},
                            {'letter': 'B', 'text': 'In Baghdad'},
                            {'letter': 'C', 'text': 'In Syria'}
                        ]
                    },
                    {
                        'number': 5,
                        'text': 'Why do people still remember him today?',
                        'options': [
                            {'letter': 'A', 'text': 'He led one of the largest slave revolts in history'},
                            {'letter': 'B', 'text': 'He was a famous poet'},
                            {'letter': 'C', 'text': 'He built great monuments'}
                        ]
                    }
                ]
            },
            2: {
                'title': 'Banu Musa Brothers',
                'questions': [
                    {
                        'number': 6,
                        'text': 'How many brothers were in the Banu Musa group?',
                        'options': [
                            {'letter': 'A', 'text': 'Three brothers'},
                            {'letter': 'B', 'text': 'Two brothers'},
                            {'letter': 'C', 'text': 'Four brothers'}
                        ]
                    },
                    {
                        'number': 7,
                        'text': 'What type of work were they famous for?',
                        'options': [
                            {'letter': 'A', 'text': 'Engineering and inventing machines'},
                            {'letter': 'B', 'text': 'Writing poetry'},
                            {'letter': 'C', 'text': 'Leading armies'}
                        ]
                    },
                    {
                        'number': 8,
                        'text': 'Did they invent machines or write stories?',
                        'options': [
                            {'letter': 'A', 'text': 'They invented machines and mechanical devices'},
                            {'letter': 'B', 'text': 'They wrote stories'},
                            {'letter': 'C', 'text': 'They did both equally'}
                        ]
                    },
                    {
                        'number': 9,
                        'text': 'Where did they work and study?',
                        'options': [
                            {'letter': 'A', 'text': 'In Baghdad during the Abbasid period'},
                            {'letter': 'B', 'text': 'In Egypt'},
                            {'letter': 'C', 'text': 'In Spain'}
                        ]
                    },
                    {
                        'number': 10,
                        'text': 'What is one thing they helped improve in science?',
                        'options': [
                            {'letter': 'A', 'text': 'Mechanical engineering and automation'},
                            {'letter': 'B', 'text': 'Medicine'},
                            {'letter': 'C', 'text': 'Astronomy'}
                        ]
                    }
                ]
            },
            3: {
                'title': 'Al-Mutawakkil',
                'questions': [
                    {
                        'number': 11,
                        'text': 'What was Al-Mutawakkil\'s job in the Abbasid Empire?',
                        'options': [
                            {'letter': 'A', 'text': 'He was the Caliph (ruler)'},
                            {'letter': 'B', 'text': 'He was a general'},
                            {'letter': 'C', 'text': 'He was a scholar'}
                        ]
                    },
                    {
                        'number': 12,
                        'text': 'Was he a ruler or a soldier?',
                        'options': [
                            {'letter': 'A', 'text': 'A ruler - he was the Caliph'},
                            {'letter': 'B', 'text': 'A soldier'},
                            {'letter': 'C', 'text': 'A merchant'}
                        ]
                    },
                    {
                        'number': 13,
                        'text': 'Where did he rule from?',
                        'options': [
                            {'letter': 'A', 'text': 'From Samarra, the capital city'},
                            {'letter': 'B', 'text': 'From Baghdad'},
                            {'letter': 'C', 'text': 'From Damascus'}
                        ]
                    },
                    {
                        'number': 14,
                        'text': 'What big empire did he lead?',
                        'options': [
                            {'letter': 'A', 'text': 'The Abbasid Empire'},
                            {'letter': 'B', 'text': 'The Byzantine Empire'},
                            {'letter': 'C', 'text': 'The Persian Empire'}
                        ]
                    },
                    {
                        'number': 15,
                        'text': 'What happened to him at the end of his rule?',
                        'options': [
                            {'letter': 'A', 'text': 'He was assassinated by his own guards'},
                            {'letter': 'B', 'text': 'He retired peacefully'},
                            {'letter': 'C', 'text': 'He was defeated in battle'}
                        ]
                    }
                ]
            },
            4: {
                'title': 'Qabiha',
                'questions': [
                    {
                        'number': 16,
                        'text': 'Who was Qabiha the mother of?',
                        'options': [
                            {'letter': 'A', 'text': 'Al-Mutawakkil, the Caliph'},
                            {'letter': 'B', 'text': 'A famous general'},
                            {'letter': 'C', 'text': 'A scholar'}
                        ]
                    },
                    {
                        'number': 17,
                        'text': 'Did she have influence in the royal court?',
                        'options': [
                            {'letter': 'A', 'text': 'Yes, she had significant influence'},
                            {'letter': 'B', 'text': 'No, she had no influence'},
                            {'letter': 'C', 'text': 'She had little influence'}
                        ]
                    },
                    {
                        'number': 18,
                        'text': 'Was she famous for ruling directly or advising others?',
                        'options': [
                            {'letter': 'A', 'text': 'Advising others - she was a powerful advisor'},
                            {'letter': 'B', 'text': 'Ruling directly'},
                            {'letter': 'C', 'text': 'Neither'}
                        ]
                    },
                    {
                        'number': 19,
                        'text': 'Why was her position important at the time?',
                        'options': [
                            {'letter': 'A', 'text': 'Mothers of caliphs often had great political power'},
                            {'letter': 'B', 'text': 'She was a military leader'},
                            {'letter': 'C', 'text': 'She was a religious leader'}
                        ]
                    },
                    {
                        'number': 20,
                        'text': 'What does her story tell us about palace life?',
                        'options': [
                            {'letter': 'A', 'text': 'Women could have significant political influence'},
                            {'letter': 'B', 'text': 'Women had no power'},
                            {'letter': 'C', 'text': 'Only men had power'}
                        ]
                    }
                ]
            },
            5: {
                'title': 'Arib al-Ma\'muniyya',
                'questions': [
                    {
                        'number': 21,
                        'text': 'What was Arib famous for performing?',
                        'options': [
                            {'letter': 'A', 'text': 'Music, singing, and poetry'},
                            {'letter': 'B', 'text': 'Fighting in battles'},
                            {'letter': 'C', 'text': 'Scientific experiments'}
                        ]
                    },
                    {
                        'number': 22,
                        'text': 'Was she known for music, fighting, or science?',
                        'options': [
                            {'letter': 'A', 'text': 'Music - she was a famous singer and musician'},
                            {'letter': 'B', 'text': 'Fighting'},
                            {'letter': 'C', 'text': 'Science'}
                        ]
                    },
                    {
                        'number': 23,
                        'text': 'Where did she perform her work?',
                        'options': [
                            {'letter': 'A', 'text': 'In the royal court of Baghdad'},
                            {'letter': 'B', 'text': 'In public markets'},
                            {'letter': 'C', 'text': 'In religious temples'}
                        ]
                    },
                    {
                        'number': 24,
                        'text': 'Why was she unusual for her time?',
                        'options': [
                            {'letter': 'A', 'text': 'She was a highly educated and independent woman artist'},
                            {'letter': 'B', 'text': 'She was a warrior'},
                            {'letter': 'C', 'text': 'She was a ruler'}
                        ]
                    },
                    {
                        'number': 25,
                        'text': 'How do people remember her today?',
                        'options': [
                            {'letter': 'A', 'text': 'As one of the most famous female musicians and poets of the Abbasid period'},
                            {'letter': 'B', 'text': 'As a military leader'},
                            {'letter': 'C', 'text': 'As a religious scholar'}
                        ]
                    }
                ]
            },
            6: {
                'title': 'Al-Jahiz',
                'questions': [
                    {
                        'number': 26,
                        'text': 'What type of books did Al-Jahiz write?',
                        'options': [
                            {'letter': 'A', 'text': 'Books about animals, literature, and many topics'},
                            {'letter': 'B', 'text': 'Only religious books'},
                            {'letter': 'C', 'text': 'Only history books'}
                        ]
                    },
                    {
                        'number': 27,
                        'text': 'Was he a soldier or a scholar?',
                        'options': [
                            {'letter': 'A', 'text': 'A scholar and writer'},
                            {'letter': 'B', 'text': 'A soldier'},
                            {'letter': 'C', 'text': 'A merchant'}
                        ]
                    },
                    {
                        'number': 28,
                        'text': 'What topics did he enjoy studying?',
                        'options': [
                            {'letter': 'A', 'text': 'Animals, literature, philosophy, and many subjects'},
                            {'letter': 'B', 'text': 'Only mathematics'},
                            {'letter': 'C', 'text': 'Only religion'}
                        ]
                    },
                    {
                        'number': 29,
                        'text': 'Why were his writings important?',
                        'options': [
                            {'letter': 'A', 'text': 'He wrote about many subjects and helped preserve knowledge'},
                            {'letter': 'B', 'text': 'He wrote military strategies'},
                            {'letter': 'C', 'text': 'He wrote only poetry'}
                        ]
                    },
                    {
                        'number': 30,
                        'text': 'What made his ideas different from others?',
                        'options': [
                            {'letter': 'A', 'text': 'He wrote in a humorous and engaging style about serious topics'},
                            {'letter': 'B', 'text': 'He only wrote serious books'},
                            {'letter': 'C', 'text': 'He only wrote poetry'}
                        ]
                    }
                ]
            },
            7: {
                'title': 'Muhammad ibn Tahir',
                'questions': [
                    {
                        'number': 31,
                        'text': 'What role did Muhammad ibn Tahir have in the empire?',
                        'options': [
                            {'letter': 'A', 'text': 'He was a governor'},
                            {'letter': 'B', 'text': 'He was a soldier'},
                            {'letter': 'C', 'text': 'He was a scholar'}
                        ]
                    },
                    {
                        'number': 32,
                        'text': 'What city or region did he govern?',
                        'options': [
                            {'letter': 'A', 'text': 'Khurasan (a large region in the east)'},
                            {'letter': 'B', 'text': 'Baghdad'},
                            {'letter': 'C', 'text': 'Egypt'}
                        ]
                    },
                    {
                        'number': 33,
                        'text': 'Did he work for the caliph?',
                        'options': [
                            {'letter': 'A', 'text': 'Yes, he was appointed by the caliph'},
                            {'letter': 'B', 'text': 'No, he was independent'},
                            {'letter': 'C', 'text': 'He worked against the caliph'}
                        ]
                    },
                    {
                        'number': 34,
                        'text': 'What was his main responsibility?',
                        'options': [
                            {'letter': 'A', 'text': 'To govern and maintain order in his region'},
                            {'letter': 'B', 'text': 'To lead armies'},
                            {'letter': 'C', 'text': 'To write books'}
                        ]
                    },
                    {
                        'number': 35,
                        'text': 'Why is he remembered in history?',
                        'options': [
                            {'letter': 'A', 'text': 'He was an important governor during a time of change in the Abbasid Empire'},
                            {'letter': 'B', 'text': 'He was a famous poet'},
                            {'letter': 'C', 'text': 'He was a great warrior'}
                        ]
                    }
                ]
            }
        },
        'reading_material': {},
        'correct_answers': {
            # Ali ibn Muhammad (Questions 1-5)
            1: 'A',  # Led Zanj rebellion
            2: 'A',  # Zanj (enslaved people) followed him
            3: 'A',  # Against the Abbasid government
            4: 'A',  # Rebellion in southern Iraq near Basra
            5: 'A',  # Led one of the largest slave revolts
            # Banu Musa Brothers (Questions 6-10)
            6: 'A',  # Three brothers
            7: 'A',  # Engineering and inventing machines
            8: 'A',  # Invented machines and mechanical devices
            9: 'A',  # Worked in Baghdad during Abbasid period
            10: 'A',  # Mechanical engineering and automation
            # Al-Mutawakkil (Questions 11-15)
            11: 'A',  # He was the Caliph (ruler)
            12: 'A',  # A ruler - he was the Caliph
            13: 'A',  # Ruled from Samarra
            14: 'A',  # Led the Abbasid Empire
            15: 'A',  # Assassinated by his own guards
            # Qabiha (Questions 16-20)
            16: 'A',  # Mother of Al-Mutawakkil
            17: 'A',  # Yes, had significant influence
            18: 'A',  # Advising others - powerful advisor
            19: 'A',  # Mothers of caliphs had great political power
            20: 'A',  # Women could have significant political influence
            # Arib al-Ma'muniyya (Questions 21-25)
            21: 'A',  # Music, singing, and poetry
            22: 'A',  # Music - famous singer and musician
            23: 'A',  # Performed in royal court of Baghdad
            24: 'A',  # Highly educated and independent woman artist
            25: 'A',  # Most famous female musician/poet of Abbasid period
            # Al-Jahiz (Questions 26-30)
            26: 'A',  # Books about animals, literature, many topics
            27: 'A',  # Scholar and writer
            28: 'A',  # Animals, literature, philosophy, many subjects
            29: 'A',  # Wrote about many subjects, preserved knowledge
            30: 'A',  # Humorous and engaging style about serious topics
            # Muhammad ibn Tahir (Questions 31-35)
            31: 'A',  # He was a governor
            32: 'A',  # Governed Khurasan
            33: 'A',  # Yes, appointed by the caliph
            34: 'A',  # To govern and maintain order
            35: 'A'   # Important governor during time of change
        }
    }
}

@app.route('/')
def home():
    # Organize quizzes by difficulty
    quizzes_by_difficulty = {
        'easy': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'easy'},
        'medium': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'medium'},
        'hard': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'hard'},
        'reward': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'reward'}
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
    # Organize quizzes by difficulty for display
    quizzes_by_difficulty = {
        'easy': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'easy'},
        'medium': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'medium'},
        'hard': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'hard'},
        'reward': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'reward'}
    }
    # Pass all quizzes so we can show results for all of them
    return render_template('results.html', quiz=quiz, quiz_id=quiz_id, all_quizzes=quizzes, quizzes_by_difficulty=quizzes_by_difficulty)

@app.route('/progress')
def progress():
    # Organize quizzes by difficulty for display
    quizzes_by_difficulty = {
        'easy': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'easy'},
        'medium': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'medium'},
        'hard': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'hard'},
        'reward': {k: v for k, v in quizzes.items() if v.get('difficulty') == 'reward'}
    }
    return render_template('progress.html', quizzes=quizzes, quizzes_by_difficulty=quizzes_by_difficulty)

if __name__ == '__main__':
    import threading
    import webview
    
    # Run Flask in a separate thread
    def run_flask():
        app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)
    
    # Start Flask server in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    import time
    time.sleep(1)
    
    # Create embedded browser window
    webview.create_window(
        'Kids Q&A Quiz App',
        'http://127.0.0.1:8080',
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True
    )
    
    # Start the webview (this blocks until window is closed)
    webview.start(debug=False)
