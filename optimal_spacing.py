import collections
import math
import random

from absl import app
from absl import flags

OUTPUT_FILE = flags.DEFINE_string('output_file', 'learning_schedule.csv', 'Output file for the schedule.')
NUM_DAYS = flags.DEFINE_integer('num_days', 500, 'Number of days to generate a schedule for.')
INIT_GAP = flags.DEFINE_integer('init_gap', 2, 'Initial gap between introduction and first repeat.')
GAP_GROWTH = flags.DEFINE_float('gap_growth', 1.5, 'Rate that gap grows at per introduction.')
LESSONS_PER_UNIT = flags.DEFINE_integer('lessons_per_unit', 10, 'Number of lessons per unit.')

def generate_schedule():
    schedule = []
    unit_progress = []
    last_unit = 0
    lessons_used = collections.defaultdict(int)
    while len(schedule) < NUM_DAYS.value:
        if not len(unit_progress) or unit_progress[0][0] >= 2:
            last_unit += 1
            schedule.extend([(last_unit, 1), (last_unit, 2)])
            days_spent = 2
            curr_unit = (INIT_GAP.value,INIT_GAP.value,last_unit)
        else:
            min_gap = unit_progress[0][0]
            index = 1
            while index < len(unit_progress) and unit_progress[index][0] <= min_gap + 1 and unit_progress[index][2] != schedule[-1][0]:
                index += 1
            unit_index = random.randrange(0,index)
            while unit_progress[unit_index][2] == schedule[-1]:
                unit_index = random.randrange(0,index)
            days_spent = 1
            schedule.append((unit_progress[unit_index][2], lessons_used[unit_progress[unit_index][2]] + days_spent))
            new_gap = math.ceil(unit_progress[unit_index][1] * GAP_GROWTH.value)
            curr_unit = (new_gap, new_gap, unit_progress[unit_index][2])
            del unit_progress[unit_index]
        unit_progress = [(u[0] - days_spent, u[1], u[2]) for u in unit_progress]
        lessons_used[curr_unit[2]] += days_spent
        if lessons_used[curr_unit[2]] <= LESSONS_PER_UNIT.value:
            unit_progress.append(curr_unit)
        unit_progress.sort()
    return schedule
      

def main(argv):
    schedule = generate_schedule()
    units_completed = [u[0] for u in schedule if u[1] == 10]
    print(f'Max unit completed: {max(units_completed)}')
    max_unit = max([u[0] for u in schedule])
    print(f'Max unit needed: {max_unit}')
    pretty_schedule = [f'{u[0]}, {u[1]}\n' for u in schedule]
    with open(OUTPUT_FILE.value, 'w') as f:
        f.write('unit,lesson\n')
        f.writelines(pretty_schedule)

if __name__ == '__main__':
  app.run(main)