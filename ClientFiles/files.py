import paramiko as pm
import pandas as pd

# --- GET DATAFRAME --- #
# Uses SFTP to receive a CSV file, then converts it to a pandas DataFrame
def get_df(ssh, filepath):
    sftp = ssh.open_sftp()
    csv_file = sftp.open(filepath)
    df = pd.read_csv(csv_file)
    sftp.close()
    return df