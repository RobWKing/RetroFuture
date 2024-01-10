spawn_data = {1:
                  [{0: [{'seeker': 1, 'twirler': 1, 'bouncer': 1, 'wedge': 1}],
                    2: [{'seeker': 1, 'twirler': 1, 'bouncer': 1}],
                    5: [{'wedge': 1}]}],

              2: [{0: [{'seeker': 1, 'twirler': 1, 'bouncer': 12, 'wedge': 1}],
                    2: [{'seeker': 1, 'twirler': 1, 'bouncer': 12}],
                    5: [{'wedge': 25}]}],

              3: [{0: [{'seeker': 1, 'twirler': 1, 'bouncer': 12, 'wedge': 1}],
                    2: [{'seeker': 1, 'twirler': 1, 'bouncer': 12}],
                    5: [{'wedge': 25}]}],
              }

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
