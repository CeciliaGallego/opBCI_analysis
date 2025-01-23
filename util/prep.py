import numpy as np
import pandas as pd
import scipy


def convert_mat_to_df(datapath):
    data = scipy.io.loadmat(datapath)
    column_names = data['pyaldata'].dtype.names
    print(column_names)
    columns_to_preserve_structure = ['all_spikes']
    unwrap_column_names = ['animal', 'session', 'trial_id', 'trial_name', 'trial_length', 'bin_size','trial_length']
    # Extracting all trials from the array
    data_trials = data['pyaldata'][0, :]  # Shape (n_trials,)

    # Convert each trial to a flat list by unwrapping list/array contents safely, but preserve 2D arrays
    data_list = []
    for trial in data_trials:
        trial_flat = []
        for i, item in enumerate(trial):
            col_name = column_names[i]
            # If the column is one where we want to preserve the 2D array, don't unwrap it
            if col_name in columns_to_preserve_structure:
                trial_flat.append(item)  # Keep the entire 2D array intact
                
            elif isinstance(item, (list, np.ndarray)):
                # If it's a list/array and its length is 1, unwrap it
                if len(item) == 1:
                    # check if the item is a list and if the lenght of the list is 1
                    if isinstance(item[0], (list, np.ndarray)) and len(item[0]) == 1:
                        trial_flat.append(item[0][0])
                    else:
                        trial_flat.append(item[0])
                else:
                    trial_flat.append(item)  # Otherwise, leave it as is
            else:
                trial_flat.append(item)  # Otherwise, use the item as is
        data_list.append(trial_flat)

    # Create a pandas DataFrame
    df = pd.DataFrame(data_list, columns=column_names)
    return df