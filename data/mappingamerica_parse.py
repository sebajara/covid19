import xlrd
import pandas as pd
import numpy as np
import pickle

# Data downloaded from: http://measureofamerica.org/maps/
# into excel files.

# Local files location:
files_folder = 'mappingamerica/'
# Names of the excel sheets
files_name = ['MappingAmerica_Demographics.xlsx',
              'MappingAmerica_Education.xlsx',
              'MappingAmerica_Environment.xlsx',
              'MappingAmerica_HDI.xlsx',
              'MappingAmerica_Health.xlsx',
              'MappingAmerica_Housing.xlsx',
              'MappingAmerica_Inclusion-Engagement.xlsx',
              'MappingAmerica_Safety-Security.xlsx',
              'MappingAmerica_Work-Wealth-Poverty.xlsx']
files_dataset = ['Demographics',
                 'Education',
                 'Environment',
                 'HDI',
                 'Health',
                 'Housing',
                 'Inclusion-Engagement',
                 'Safety-Security',
                 'Work-Wealth-Poverty']
files_path = [files_folder+file_name for file_name in files_name]

## TODO:
# Fix parsing issue w county data 'HDI', 'Inclusion-Engagement', 'Safety-Security'

def parse_mappingamerica_excel(excel_file, target_sheets=['State', 'County']):
    '''Function for parsing MappingAmerica excel sheets. Takes two input
    arguments: excel_file, which is the actual file path, and
    target_sheets, which is a list with the name of all sheets that
    wished to be parsed. Returns two lists, one with a dataframe
    containing the data for each sheet, and a second with the
    information regarding the corresponding sheet columns.'''
    book = xlrd.open_workbook(excel_file)
    # Find the index of those sheets
    target_sheet_indexes = [n for (n, sheet_name) in enumerate(book.sheet_names())
                            if sheet_name in target_sheets]
    # Make a list
    sheets = [book.sheet_by_index(n) for n in target_sheet_indexes]
    df_list = []
    info_list = []
    for sheet in sheets:
        (df, info) = parse_mappingamerica_sheet(sheet)
        df_list.append(df)
        info_list.append(info)
    return(df_list, info_list)


def parse_mappingamerica_sheet(sheet):
    '''Main function for parsing a sheet of the MappingAmerica excel
    files. It retuns two dataframes, one with the actual data and a
    second with the information regarding columns.'''
    # Find the type of observation we have and the row where values
    # begin
    obs_type = ''
    for r in range(sheet.nrows):
        if(sheet.cell(r, 0).value.isupper()):
            obs_type = sheet.cell(r, 0).value
            data_row_start = r+1
    # Find the kind of headers and their row and column locations
    header_rows = {}
    header_info_col = 0
    while(not header_rows.keys()):
        header_info_col = header_info_col + 1
        for r in range(data_row_start):
            if sheet.cell(r, header_info_col).value:
                header_rows[sheet.cell(r, header_info_col).value] = r
    # Collect all row data into a list
    data = []
    for r in range(data_row_start, sheet.nrows):
        data.append(sheet.row_values(r))
    # convert to data frame
    df = pd.DataFrame(data)
    # drop mid columns
    drop_cols = list(range(1, header_info_col+1))
    df = df.drop(drop_cols, axis=1)
    # replace all n/a by NaN
    df = df.replace('n/a', np.nan)
    # get column names and info regarding each
    col_names = [obs_type]
    variable_list = []
    gender_list = []
    race_list = []
    source_list = []
    year_list = []
    notes_list = []
    for c in range(header_info_col+1, sheet.ncols):
        if('GENDER' in header_rows.keys()):
            gender = sheet.cell(header_rows['GENDER'], c).value
        else:
            gender = 'Everyone'
        if('RACE' in header_rows.keys()):
            race = sheet.cell(header_rows['RACE'], c).value
        else:
            race = 'Everyone'
        if('SOURCE' in header_rows.keys()):
            source = sheet.cell(header_rows['SOURCE'], c).value
        elif('SOURCE_NAME' in header_rows.keys()):
            source = sheet.cell(header_rows['SOURCE_NAME'], c).value
        else:
            source = np.nan
        if('YEAR' in header_rows.keys()):
            year = sheet.cell(header_rows['YEAR'], c).value
        else:
            year = np.nan
        if('NOTES' in header_rows.keys()):
            notes = sheet.cell(header_rows['NOTES'], c).value
        else:
            notes = np.nan
        if('VARIABLE' in header_rows.keys()):
            variable = sheet.cell(header_rows['VARIABLE'], c).value
        elif('DISPLAY_NAME' in header_rows.keys()):
            variable = sheet.cell(header_rows['DISPLAY_NAME'], c).value
        else:
            print('Available headers:')
            print(header_rows.keys())
            raise RuntimeError("Missing the variables names to create table")
        variable_list.append(variable)
        gender_list.append(gender)
        race_list.append(race)
        source_list.append(source)
        year_list.append(year)
        notes_list.append(notes)
        col_names.append('{}_{}_{}'.format(variable, gender, race))
    # rename columns
    df.columns = col_names
    # set the index
    df = df.set_index(obs_type)
    # make a dataframe mapping column names to each
    columns_info = pd.DataFrame([])
    columns_info['VARIABLE'] = variable_list
    columns_info['GENDER'] = gender_list
    columns_info['RACE'] = race_list
    columns_info['SOURCE'] = source_list
    columns_info['YEAR'] = year_list
    columns_info['NOTES'] = notes_list
    columns_info.index = col_names[1:]
    return(df, columns_info)


data_by_state = {}
data_by_county = {}
sheets = ['State', 'County']
for (path, dataset) in zip(files_path, files_dataset):
    (dfs, infos) = parse_mappingamerica_excel(path, target_sheets=sheets)
    data_by_state[dataset] = [dfs[0], infos[0]]
    data_by_county[dataset] = [dfs[1], infos[1]]

with open("mappingamerica/mappingamerica_by_state.pickle", "wb") as file:
    pickle.dump(data_by_state, file)
with open("mappingamerica/mappingamerica_by_county.pickle", "wb") as file:
    pickle.dump(data_by_county, file)


