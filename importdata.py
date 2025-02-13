import gspread
from google.oauth2 import service_account

# Replace 'path/to/your/credentials.json' with the actual path to your credentials file
CREDENTIALS_FILE = './credentials.json'

# Replace 'your_sheet_id' with the actual ID of your Google Sheet
SPREADSHEET_ID = '1LcjoJKVlrrZ7vRD_Usk15xhTctnftnDoCusH6QHTqK0'

def write_data_to_sheet(data, spreadsheet_id, credentials_file, worksheet_name='Sheet1'):
    try:
        gc = gspread.service_account(filename=credentials_file)
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet(worksheet_name)
        worksheet.clear()
        worksheet.update('A1', data)
        print(f"Data successfully written to spreadsheet: {spreadsheet_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
def read_data_from_sheet(spreadsheet_id, credentials_file, worksheet_name='Sheet1'):
    try:
        gc = gspread.service_account(filename=credentials_file)
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet(worksheet_name)
        data = worksheet.get_all_values()
        print(f"Data successfully read from spreadsheet: {spreadsheet_id}")
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def read_filtered_column(spreadsheet_id, credentials_file, worksheet_name='Sheet1'):
    gc = gspread.service_account(filename=credentials_file)
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(worksheet_name)
    
    # Get all values
    all_data = worksheet.get_all_values()
    
    # Filter rows where column 2 has value but columns 3 and 4 are empty
    filtered_values = []
    for row in all_data:
        if len(row) >= 4:  # Ensure row has at least 4 columns
            if row[1] and not row[2] and not row[3]:  # Check column 2 has value, 3 and 4 are empty
                filtered_values.append(row[1])
    
    return filtered_values
def update_selective_rows(spreadsheet_id, credentials_file, new_data_array, worksheet_name='Sheet1'):
    gc = gspread.service_account(filename=credentials_file)
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(worksheet_name)
    
    # Get all values from sheet
    all_data = worksheet.get_all_values()
    new_data_index = 0
    
    # Process each row in the sheet
    for row_index, row in enumerate(all_data, start=1):
        # Check if row has at least 4 columns and columns 3,4 are empty
        if len(row) >= 4 and not row[2] and not row[3]:
            # Make sure we haven't exceeded our new data array
            if new_data_index < len(new_data_array):
                # Update columns B, C, and D with new data
                worksheet.update(f'B{row_index}:D{row_index}', [new_data_array[new_data_index]])
                new_data_index += 1
    
    print(f"Successfully updated {new_data_index} rows with new data")

if __name__ == '__main__':
    filtered_data = read_filtered_column(SPREADSHEET_ID, CREDENTIALS_FILE)
    for value in filtered_data:
        print(value)
        
    my_2d_array = [
        ['FqewTbduLVSuNXqra32jf7h9eFSVC2Vm26xK6ebUpump', 'value3', 'value4'],
        ['31R1k6rCzkvWdmbzD9h9DSafQWrLTsNXxgoDwdACpump', 'value7', 'value8'],
        ['4udbpWxmvxYvvQgtUA9ZKER7jaN4UTE2nbgAjLvdpump', 'value11', 'value12']
    ]
    
    update_selective_rows(SPREADSHEET_ID, CREDENTIALS_FILE, my_2d_array)
