import numpy as np
import pandas as pd
import scipy


# def convert_mat_to_df(datapath):
#     data = scipy.io.loadmat(datapath)
#     column_names = data['pyaldata'].dtype.names
#     print(column_names)
#     columns_to_preserve_structure = ['all_spikes']
#     unwrap_column_names = ['animal', 'session', 'trial_id', 'trial_name', 'trial_length', 'bin_size','trial_length']
#     # Extracting all trials from the array
#     data_trials = data['pyaldata'][0, :]  # Shape (n_trials,)

#     # Convert each trial to a flat list by unwrapping list/array contents safely, but preserve 2D arrays
#     data_list = []
#     for trial in data_trials:
#         trial_flat = []
#         for i, item in enumerate(trial):
#             col_name = column_names[i]
#             # If the column is one where we want to preserve the 2D array, don't unwrap it
#             if col_name in columns_to_preserve_structure:
#                 trial_flat.append(item)  # Keep the entire 2D array intact
                
#             elif isinstance(item, (list, np.ndarray)):
#                 # If it's a list/array and its length is 1, unwrap it
#                 if len(item) == 1:
#                     # check if the item is a list and if the lenght of the list is 1
#                     if isinstance(item[0], (list, np.ndarray)) and len(item[0]) == 1:
#                         trial_flat.append(item[0][0])
#                     else:
#                         trial_flat.append(item[0])
#                 else:
#                     trial_flat.append(item)  # Otherwise, leave it as is
#             else:
#                 trial_flat.append(item)  # Otherwise, use the item as is
#         data_list.append(trial_flat)

#     # Create a pandas DataFrame
#     df = pd.DataFrame(data_list, columns=column_names)
#     return df





def load_BCI_log(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    if not lines:
        return pd.DataFrame(columns=["timestamp", "loglevel", "message"])

    # Get the prefix from the first line by splitting based on ":"
    prefix = lines[0].split(":")[0] + ":"

    # Parse the content into a DataFrame
    data = []
    combined_line = ""
    for line in lines:
        if line.startswith(prefix):
            if combined_line:
                # Process the previously combined line
                try:
                    # Extract timestamp: text between the first ":" and "-"
                    timestamp = combined_line.split()[1].strip()
                    timestamp = timestamp.rsplit("_", 1)[-1]
                    
                    # Extract log level: text after the first "-" and before the next ":"
                    log_level = combined_line.split()[3].strip()
                    
                    # Extract message: text after the second ":"
                    message = combined_line.split(' ',4)[4].strip()
                    
                    # Append parsed data
                    data.append([timestamp, log_level, message])
                except (IndexError, ValueError) as e:
                    print(f"Skipping line due to error: {e}")
                    print(f"Line: {combined_line}")
                combined_line = ""
            combined_line = line.strip()
        else:
            combined_line += " " + line.strip()

    # Process the last combined line if any
    if combined_line:
        try:
            # Extract timestamp: text between the first ":" and "-"
            timestamp = combined_line.split()[1].strip()
            timestamp = timestamp.rsplit("_", 1)[-1]
            
            # Extract log level: text after the first "-" and before the next ":"
            log_level = combined_line.split()[3].strip()
            
            # Extract message: text after the second ":"
            message = combined_line.split(' ',4)[4].strip()
            
            # Append parsed data
            data.append([timestamp, log_level, message])
        except (IndexError, ValueError) as e:
            print(f"Skipping line due to error: {e}")
            print(f"Line: {combined_line}")

    # Create the DataFrame
    df = pd.DataFrame(data, columns=["timestamp", "loglevel", "message"])
    
    # Convert the timestamp column to numeric
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    
    return df