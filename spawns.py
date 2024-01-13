spawn_data = {1:
                  [{0: [{'seeker': 1, 'twirler': 1, 'bouncer': 1, 'wedge': 1}],
                    1.2: [{'seeker': 5, 'twirler': 1, 'bouncer': 1}],
                    1.5: [{'seeker': 3, 'twirler': 2, 'bouncer': 1}],
                    1.9: [{'seeker': 2, 'twirler': 1, 'bouncer': 2}],
                    5: [{'wedge': 1}]}],

              2: [{0: [{'seeker': 1, 'twirler': 1, 'bouncer': 12, 'wedge': 1}],
                    2: [{'seeker': 1, 'twirler': 1, 'bouncer': 12}],
                    5: [{'wedge': 25}]}],

              3: [{0: [{'seeker': 1, 'twirler': 1, 'bouncer': 12, 'wedge': 1}],
                    2: [{'seeker': 1, 'twirler': 1, 'bouncer': 12}],
                    5: [{'wedge': 25}]}],

              4: [{0: [{'twirler': 2}],
                    1: [{'seeker': 3}],
                    2: [{'bouncer': 2}],
                    5: [{'twirler': 3}],
                    6: [{'seeker': 3}],
                    7: [{'bouncer': 3}]}],

              # do this manually in the custom level function to create lots of wedges and bouncers
              5: [{0: [{'bouncer': 6}],
                    2: [{'bouncer': 4}],
                    4: [{'bouncer': 5}],
                    6: [{'bouncer': 7}],
                    8: [{'wedge': 15}],
                    12: [{'wedge': 15}],
                    13: [{'wedge': 15}],
                    14: [{'wedge': 15}],
                    17: [{'wedge': 15}],
                    22: [{'wedge': 15}],
                    26: [{'wedge': 20}]}],

                11: [{0: [{'twirler': 2}],
                    1: [{'seeker': 3}],
                    2: [{'bouncer': 2}],
                    5: [{'twirler': 3}],
                    6: [{'seeker': 3}],
                    7: [{'bouncer': 3}]},]
              }

# Level 11 - Survival Mode

# Level 12 - Endless Mode

def calculate_total_enemies(spawn_data):
    total_enemies_per_level = {}
    for level, level_data_list in spawn_data.items():
        total_enemies = 0
        for per_second_enemy_list in level_data_list:
            for enemy_list in per_second_enemy_list.values():
                for individual_enemies in enemy_list:
                    for enemy_count in individual_enemies.values():
                        total_enemies += enemy_count
        total_enemies_per_level[level] = total_enemies

    return total_enemies_per_level

# print((calculate_total_enemies(spawn_data)).get(<your_level_here>))


for i in range(2):
    print(calculate_total_enemies(spawn_data))