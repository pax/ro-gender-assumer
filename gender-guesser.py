
file_path = 'data/candidati-8sept-prev.csv'  
country_code = 'romania'  
name_columns = ['last', 'last first', 'last last']  


import pandas as pd
import gender_guesser.detector as gender

def add_gender_columns(file_path, name_columns, country_code=None):
    data = pd.read_csv(file_path) 
    detector = gender.Detector(case_sensitive=False)

    gender_columns = []
    for column in name_columns:
        gender_column = f'gender_{column}'
        gender_columns.append(gender_column)
        if country_code:
            data[gender_column] = data[column].apply(
                lambda name: detector.get_gender(name.strip(), country_code) if pd.notna(name) else 'unknown')
        else:
            data[gender_column] = data[column].apply(
                lambda name: detector.get_gender(name.strip()) if pd.notna(name) else 'unknown')

    data['aggregate_gender'] = data[gender_columns].apply(lambda row: ','.join(row.values), axis=1)

    new_file_path = file_path.replace('.csv', f'_genders-{country_code if country_code else "default"}.csv')
    data.to_csv(new_file_path, index=False)
    
    print(f"New file saved as: {new_file_path}")

add_gender_columns(file_path, name_columns, country_code)
