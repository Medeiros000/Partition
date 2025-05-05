from database.Database import Database
from utils.Printer import Printer
from utils.Notes import Notes
from dotenv import load_dotenv
import os


def get_env_vars():
  load_dotenv()
  limit = int(os.getenv('REG_LIMIT'))
  column = os.getenv('COLUMN_NAME')
  table_origin = os.getenv('TABLE_ORIGIN')
  table_destination = os.getenv('TABLE_DESTINATION')
  notes_folder = os.getenv('NOTES_FOLDER') if os.getenv(
      'NOTES_FOLDER') != '' else 'files'
  info = os.getenv('INFO')
  logs = os.getenv('LOGS')
  return limit, column, table_origin, table_destination, notes_folder, info, logs


def execute_batch(db, p, n, table_name, temp_exec, sum_temp, count, reg_exec):
  reg_exec[count] = (temp_exec.copy(), sum_temp)
  query = db.show_create_table_partition(
      table_name, [temp_exec[0], temp_exec[-1]])
  p.print_green(query)
  n.write_note('sql_create_partition', query, type='sql', date=False)


def register_logs(n, reg_exec, columns_reg, logs):
  if logs:
    for reg in reg_exec.items():
      list_column = ';'.join(map(str, reg[1][0]))
      n.write_note('complete_reg_exec',
                   (reg[0], list_column, reg[1][1]), type='csv', date=True)
    for reg in reg_exec.items():
      content = f'{reg[0]},{reg[1][0][0]};{reg[1][0][-1]},{reg[1][1]}'
      n.write_note('simple_reg_exec', content, type='csv', date=False)
    for reg in columns_reg:
      n.write_note('columns', reg, date=False)


def main():
  limit, column, table_origin, table_destination, notes_folder, info, logs = get_env_vars()
  db = Database()
  p = Printer()
  n = Notes(notes_folder)

  sum_temp = 0
  count = 0
  reg_exec = {}
  temp_exec = []
  columns_reg = []
  data = db.auxiliar_data(table_origin, column)

  create_table = db.show_create_table_by_range(table_origin, column)
  create_table = create_table.replace(table_origin, table_destination)
  n.write_note('sql_create_table', create_table, type='sql', date=False)

  insert_into = db.show_insert_into(table_origin, table_destination)
  n.write_note('sql_insert_into', insert_into, type='sql', date=False)

  for i in range(0, len(data)):
    id = data[i][0]
    current_column = data[i][1]
    n_reg = data[i][2]
    if info:
      p.print_yellow(f'\ni: {i + 1}')
      p.print_yellow(f'current_column: {data[i]}\n')
      print('Package sum:', sum_temp)

    temp_exec.append(current_column)
    columns_reg.append(current_column)

    if n_reg > limit and len(temp_exec) == 1:
      if info:
        print(
            f'Atual current_column has {n_reg} and pass limit of transation: {limit}')
      sum_temp += n_reg
      execute_batch(db, p, n, table_destination,
                    temp_exec, sum_temp, count, reg_exec)
      temp_exec = []
      sum_temp = 0

    elif sum_temp + n_reg > limit:
      if info:
        print(f'{sum_temp} + {n_reg} pass limit of transation: {limit}')
      temp_exec.remove(current_column)
      columns_reg.remove(current_column)
      execute_batch(db, p, n, table_destination,
                    temp_exec, sum_temp, count, reg_exec)
      sum_temp = 0
      temp_exec = []
      count += 1

      if n_reg >= limit:
        if info:
          print(f'Data of the current batch has more than {limit}, execute')
        sum_temp += n_reg
        temp_exec.append(current_column)
        columns_reg.append(current_column)
        execute_batch(db, p, n, table_destination,
                      temp_exec, sum_temp, count, reg_exec)
        sum_temp = 0
        temp_exec = []
        count += 1
      else:
        if info:
          print(
              f'Data of the current batch has less than {limit}, add to the next batch')
        sum_temp += n_reg
        temp_exec.append(current_column)
        columns_reg.append(current_column)
    else:
      if info:
        print(f'{sum_temp} + {n_reg} not pass limit of transation: {limit}')
      sum_temp += n_reg

  # Check if there are remaining values
  if sum_temp > 0:
    if info:
      p.print_red('Remaining values')
      p.print_yellow(f'\nLast line: {temp_exec[-1]}')
    execute_batch(db, p, n, table_destination,
                  temp_exec, sum_temp, count, reg_exec)
    sum_temp = 0
    temp_exec = []
    count += 1

  register_logs(n, reg_exec, columns_reg, logs)
  p.print_yellow(f'Total batches: {count}')
  p.print_yellow('END')


if __name__ == "__main__":
  main()
