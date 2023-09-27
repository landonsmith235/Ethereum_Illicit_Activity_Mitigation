from etherscan import Etherscan
eth = Etherscan('API Key')

#Function to convert Wei into ETH
def wei_converter(amount):
    new_amount = amount / 1000000000000000000
    return new_amount
    
#Function to Find the Total # of Transactions in Block Range
def transaction_count(trans_list):
    total = len(trans_list)
    return total

#Function to get transactions sent from the address within block range
#Returns a list with sent transactions
def transactions_sent(trans_list, address):
    new_list=[]
    for i in trans_list:
        if i['from'] == address:
            new_list.append(i)
    return new_list

#Function to get transactions received by the address within Block Range
#Returns a lsit with recieved transactions and the received transaction count
def transactions_recieved(trans_list, address):
    new_list=[]
    for i in trans_list:
        if i['to'] == address:
            new_list.append(i)
    return new_list

#Function to get max value sent or recieved from a list of transactions
def eth_max_val(trans_list):
    val_counter = []
    for i in trans_list:
        val_counter.append(int(i['value']))
    if len(val_counter) == 0:
        val_counter = 0
    else:
        val_counter = max(val_counter)
    return int(val_counter) / 1000000000000000000

#Function to get min value sent or recieved from a list of transactions
def eth_min_val(trans_list):
    val_counter = []
    for i in trans_list:
        val_counter.append(int(i['value']))
    if len(val_counter) == 0:
        val_counter = 0
    else:
        val_counter = min(val_counter)
    return int(val_counter) / 1000000000000000000

#Function to get total value sent or recieved from a list of transactions
def eth_total_val(trans_list):
    val_counter = 0
    for i in trans_list:
        val_counter += int(i['value'])
    return int(val_counter) / 1000000000000000000

#Function to get the average value sent or received from a list of transactions
def eth_avg_val(trans_list):
    from statistics import mean
    val_counter = []
    for i in trans_list:
        val_counter.append(int(i['value']))
    if len(val_counter) == 0:
        val_counter = 0
    else:
        val_counter = mean(val_counter)
    return int(val_counter) / 1000000000000000000

#Function to get time delta of the first and last transaction (time block with transaction in it was confirmed)
def first_last_trans_time_delta(trans_list):
    trans_times = []
    if len(trans_list) == 0:
        time_delta = 0
    if len(trans_list) == 1:
        time_delta = 0
    else:
        first_timestamp = int(trans_list[0]['timeStamp'])
        last_timestamp = int(trans_list[-1]['timeStamp'])
        time_delta = last_timestamp - first_timestamp
        time_delta = time_delta / 60
    return time_delta

#Function to get the average time between transactions
def avg_time_between(trans_list):
    from statistics import mean
    trans_times = []
    delta_list = []
    counter0 = 0
    counter1 = 1
    if len(trans_list) == 0:
        avg_time = 0
    if len(trans_list) == 1:
        avg_time = 0
    else:
        for i in trans_list:
            timestamp = i['timeStamp']
            timestamp = int(timestamp)
            trans_times.append(timestamp)
        for i in trans_times:
            try:
                delta = abs(trans_times[counter0] - trans_times[counter1])
                delta_list.append(delta)
                counter0 += 1
                counter1 += 1
            except:
                avg_time = mean(delta_list) / 60
                break
    return avg_time

#Function to return the number of unique addresses from which receieved transactions or to which the accoutn sent transactions
def find_num_unique(trans_list, direction):
    addresses=[]
    if direction == 'from':
        for i in trans_list:
            addresses.append(i['from'])
    if direction == 'to':
        for i in trans_list:
            addresses.append(i['to'])
    unique_addresses = list(set(addresses))
    return len(unique_addresses)

#Function to Create Batches for Processing
def batch_creator(df, batch_size):
    num_batches = len(df) // batch_size + 1
    dataframes = []
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size
        batch_df = df[start_idx:end_idx]
        dataframes.append(batch_df)
    return dataframes

#Function to Automate Features for a Single Account
def automate_feature_generation_single(blockchain_address, feature_list, start_block, end_block):
    from etherscan import Etherscan
    eth = Etherscan('API Key')
    import pandas as pd
    
    #Create a list for each feature
    feature_dict = {}
    for i in feature_list:
        feature_dict['list_' + i] = []
    #Create Features for Address
    balance = wei_converter(int(eth.get_eth_balance(blockchain_address)))
    try:
        txs = eth.get_normal_txs_by_address(blockchain_address, start_block, end_block, 'asc')
        txs = [n for n in txs if n['isError'] == '0']
    except:
        txs = []
    tx_rec = transactions_recieved(txs, blockchain_address)
    tx_sent = transactions_sent(txs, blockchain_address)
    try: 
        erc20_txs = eth.get_erc20_token_transfer_events_by_address(blockchain_address, start_block, end_block, 'asc')
    except:
        erc20_txs = []
    erc20_tx_rec = transactions_recieved(erc20_txs, blockchain_address)
    erc20_tx_sent = transactions_sent(erc20_txs, blockchain_address)
        
    feature_dict['list_Sent_tnx'].append(transaction_count(tx_sent))
    feature_dict['list_Received_tnx'].append(transaction_count(tx_rec))
    feature_dict['list_Total_Ether_Balance'].append(balance)
    feature_dict['list_Max_Val_Received'].append(eth_max_val(tx_rec))
    feature_dict['list_Min_Val_Received'].append(eth_min_val(tx_rec))
    feature_dict['list_Total_Ether_Received'].append(eth_total_val(tx_rec))
    feature_dict['list_Avg_Val_Received'].append(eth_avg_val(tx_rec))
    feature_dict['list_Max_Val_Sent'].append(eth_max_val(tx_sent))
    feature_dict['list_Min_Val_Sent'].append(eth_min_val(tx_sent))
    feature_dict['list_Total_Ether_Sent'].append(eth_total_val(tx_sent))
    feature_dict['list_Avg_Val_Sent'].append(eth_avg_val(tx_sent))
    feature_dict['list_Time_Diff_between_first_and_last_(Mins)'].append(first_last_trans_time_delta(txs))
    feature_dict['list_Avg_min_between_sent_tnx'].append(avg_time_between(tx_sent))
    feature_dict['list_Avg_min_between_received_tnx'].append(avg_time_between(tx_rec))
    feature_dict['list_Total_Transactions_(Including_Tnx_to_Create_Contract)'].append(transaction_count(txs))
    feature_dict['list_Total_ERC20_Tnxs'].append(transaction_count(erc20_txs))
    feature_dict['list_ERC20_Avg_Time_Between_Sent_Tnx'].append(avg_time_between(erc20_tx_sent))
    feature_dict['list_ERC20_Avg_Time_Between_Rec_Tnx'].append(avg_time_between(erc20_tx_rec))
    feature_dict['list_Unique_Received_From_Addresses'].append(find_num_unique(tx_rec, 'from'))
    feature_dict['list_Unique_Sent_To_Addresses'].append(find_num_unique(tx_sent, 'to'))
    feature_dict['list_ERC20_Uniq_Sent_Addr'].append(find_num_unique(erc20_tx_sent, 'to'))
    feature_dict['list_ERC20_Uniq_Rec_Addr'].append(find_num_unique(erc20_tx_rec, 'from'))
        
        
    data = {'Address':blockchain_address,
            'Sent_tnx':feature_dict['list_Sent_tnx'],
            'Recieved_tnx':feature_dict['list_Received_tnx'],
            'Total_Ether_Balance':feature_dict['list_Total_Ether_Balance'],
            'Max_Value_Received': feature_dict['list_Max_Val_Received'],
            'Min_Value_Received': feature_dict['list_Min_Val_Received'],
            'Total_Ether_Received': feature_dict['list_Total_Ether_Received'],
            'Time_Diff_between_first_and_last_(Mins)': feature_dict['list_Time_Diff_between_first_and_last_(Mins)'],
            'Total_Transactions(Including_Tnx_to_Create_Contract)': feature_dict['list_Total_Transactions_(Including_Tnx_to_Create_Contract)'],
            'Avg_Value_Received': feature_dict['list_Avg_Val_Received'],
            'Max_Value_Sent': feature_dict['list_Max_Val_Sent'],
            'Min_Value_Sent': feature_dict['list_Min_Val_Sent'],
            'Total_Ether_Sent': feature_dict['list_Total_Ether_Sent'],
            'Avg_Value_Sent': feature_dict['list_Avg_Val_Sent'],
            'Avg_min_between_sent_tnx': feature_dict['list_Avg_min_between_sent_tnx'],
            'Avg_min_between_received_tnx': feature_dict['list_Avg_min_between_received_tnx'],
            'Total_ERC20_Tnxs': feature_dict['list_Total_ERC20_Tnxs'],
            'ERC20_Avg_Time_Between_Sent_Tnx': feature_dict['list_ERC20_Avg_Time_Between_Sent_Tnx'],
            'ERC20_Avg_Time_Between_Rec_Tnx': feature_dict['list_ERC20_Avg_Time_Between_Rec_Tnx'],
            'Unique_Received_From_Addresses':feature_dict['list_Unique_Received_From_Addresses'],
            'Unique_Sent_To_Addresses':feature_dict['list_Unique_Sent_To_Addresses'],
            'ERC20_Uniq_Sent_Addr':feature_dict['list_ERC20_Uniq_Sent_Addr'],
            'ERC20_Uniq_Rec_Addr':feature_dict['list_ERC20_Uniq_Rec_Addr']}
    
    df = pd.DataFrame(data)
    return df

#Function to Automate the Generation of Features for Multiple Accounts
def automate_feature_generation_multiple(blockchain_addresses, feature_list, start_block, end_block):
    from etherscan import Etherscan
    eth = Etherscan('API Key')
    import pandas as pd
    
    #Create a list for each feature
    feature_dict = {}
    for i in feature_list:
        feature_dict['list_' + i] = []
    #Iterate through each address & append results to dictionary
    for i in blockchain_addresses:
        balance = wei_converter(int(eth.get_eth_balance(i)))
        try:
            txs = eth.get_normal_txs_by_address(i, start_block, end_block, 'asc')
            txs = [n for n in txs if n['isError'] == '0']
        except:
            txs = []
        tx_rec = transactions_recieved(txs, i)
        tx_sent = transactions_sent(txs, i)
        try: 
            erc20_txs = eth.get_erc20_token_transfer_events_by_address(i, start_block, end_block, 'asc')
        except:
            erc20_txs = []
        erc20_tx_rec = transactions_recieved(erc20_txs, i)
        erc20_tx_sent = transactions_sent(erc20_txs, i)
        
        feature_dict['list_Sent_tnx'].append(transaction_count(tx_sent))
        feature_dict['list_Received_tnx'].append(transaction_count(tx_rec))
        feature_dict['list_Total_Ether_Balance'].append(balance)
        feature_dict['list_Max_Val_Received'].append(eth_max_val(tx_rec))
        feature_dict['list_Min_Val_Received'].append(eth_min_val(tx_rec))
        feature_dict['list_Total_Ether_Received'].append(eth_total_val(tx_rec))
        feature_dict['list_Avg_Val_Received'].append(eth_avg_val(tx_rec))
        feature_dict['list_Max_Val_Sent'].append(eth_max_val(tx_sent))
        feature_dict['list_Min_Val_Sent'].append(eth_min_val(tx_sent))
        feature_dict['list_Total_Ether_Sent'].append(eth_total_val(tx_sent))
        feature_dict['list_Avg_Val_Sent'].append(eth_avg_val(tx_sent))
        feature_dict['list_Time_Diff_between_first_and_last_(Mins)'].append(first_last_trans_time_delta(txs))
        feature_dict['list_Avg_min_between_sent_tnx'].append(avg_time_between(tx_sent))
        feature_dict['list_Avg_min_between_received_tnx'].append(avg_time_between(tx_rec))
        feature_dict['list_Total_Transactions_(Including_Tnx_to_Create_Contract)'].append(transaction_count(txs))
        feature_dict['list_Total_ERC20_Tnxs'].append(transaction_count(erc20_txs))
        feature_dict['list_ERC20_Avg_Time_Between_Sent_Tnx'].append(avg_time_between(erc20_tx_sent))
        feature_dict['list_ERC20_Avg_Time_Between_Rec_Tnx'].append(avg_time_between(erc20_tx_rec))
        feature_dict['list_Unique_Received_From_Addresses'].append(find_num_unique(tx_rec, 'from'))
        feature_dict['list_Unique_Sent_To_Addresses'].append(find_num_unique(tx_sent, 'to'))
        feature_dict['list_ERC20_Uniq_Sent_Addr'].append(find_num_unique(erc20_tx_sent, 'to'))
        feature_dict['list_ERC20_Uniq_Rec_Addr'].append(find_num_unique(erc20_tx_rec, 'from'))
        
        
    data = {'Address':blockchain_addresses,
            'Sent_tnx':feature_dict['list_Sent_tnx'],
            'Recieved_tnx':feature_dict['list_Received_tnx'],
            'Total_Ether_Balance':feature_dict['list_Total_Ether_Balance'],
            'Max_Value_Received': feature_dict['list_Max_Val_Received'],
            'Min_Value_Received': feature_dict['list_Min_Val_Received'],
            'Total_Ether_Received': feature_dict['list_Total_Ether_Received'],
            'Time_Diff_between_first_and_last_(Mins)': feature_dict['list_Time_Diff_between_first_and_last_(Mins)'],
            'Total_Transactions(Including_Tnx_to_Create_Contract)': feature_dict['list_Total_Transactions_(Including_Tnx_to_Create_Contract)'],
            'Avg_Value_Received': feature_dict['list_Avg_Val_Received'],
            'Max_Value_Sent': feature_dict['list_Max_Val_Sent'],
            'Min_Value_Sent': feature_dict['list_Min_Val_Sent'],
            'Total_Ether_Sent': feature_dict['list_Total_Ether_Sent'],
            'Avg_Value_Sent': feature_dict['list_Avg_Val_Sent'],
            'Avg_min_between_sent_tnx': feature_dict['list_Avg_min_between_sent_tnx'],
            'Avg_min_between_received_tnx': feature_dict['list_Avg_min_between_received_tnx'],
            'Total_ERC20_Tnxs': feature_dict['list_Total_ERC20_Tnxs'],
            'ERC20_Avg_Time_Between_Sent_Tnx': feature_dict['list_ERC20_Avg_Time_Between_Sent_Tnx'],
            'ERC20_Avg_Time_Between_Rec_Tnx': feature_dict['list_ERC20_Avg_Time_Between_Rec_Tnx'],
            'Unique_Received_From_Addresses':feature_dict['list_Unique_Received_From_Addresses'],
            'Unique_Sent_To_Addresses':feature_dict['list_Unique_Sent_To_Addresses'],
            'ERC20_Uniq_Sent_Addr':feature_dict['list_ERC20_Uniq_Sent_Addr'],
            'ERC20_Uniq_Rec_Addr':feature_dict['list_ERC20_Uniq_Rec_Addr']}
    df = pd.DataFrame(data)
    return df

#Function to Feature Engineer Batches Automatically
def batch_feature_engineering(batch_list, feature_list, start_block, end_block):
    import pandas as pd
    import time
    results_list = []
    missed_list = []
    counter = 1
    for i in batch_list:
        try:
            print('Batch #' + str(counter) + ' has begun processing...')
            result = automate_feature_generation_multiple(i['Address'].tolist(), feature_list, start_block, end_block)
            results_list.append(result)
            counter += 1
        except:
            print('Error Thrown on Batch #' + str(counter))
            missed_list.append(i)
            counter +=1
            time.sleep(10)
            continue
    
    final_dataset = pd.concat(results_list)
    return final_dataset, missed_list

#Function to Return Descriptive Statistics on Transaction-Based Datasets
def descriptive_statistics_transactions(df1, df1_name, df2, df2_name, stat):
    import pandas as pd
    df1 = df1.drop(columns = ['hash'])
    df2 = df2.drop(columns = ['hash'])
    feature_list = df1.columns
    calculation_df1 = []
    calculation_df2 = []
    if stat == 'mean':
        for i in range(df1.shape[1]):
            calculation_df1.append(df1.iloc[:,i].mean())
        for i in range(df2.shape[1]):
            calculation_df2.append(df2.iloc[:,i].mean())
    if stat == 'median':
        for i in range(df1.shape[1]):
            calculation_df1.append(df1.iloc[:,i].median())
        for i in range(df2.shape[1]):
            calculation_df2.append(df2.iloc[:,i].median())
    if stat == 'max':
        for i in range(df1.shape[1]):
            calculation_df1.append(df1.iloc[:,i].max())
        for i in range(df2.shape[1]):
            calculation_df2.append(df2.iloc[:,i].max())
    if stat == 'percentile_90':
        for i in range(df1.shape[1]):
            calculation_df1.append(np.percentile(df1.iloc[:,i],90))
        for i in range(df2.shape[1]):
            calculation_df2.append(np.percentile(df2.iloc[:,i],90))
    if stat == 'percentile_50':
        for i in range(df1.shape[1]):
            calculation_df1.append(np.percentile(df1.iloc[:,i],50))
        for i in range(df2.shape[1]):
            calculation_df2.append(np.percentile(df2.iloc[:,i],50))
    data = {'Features':feature_list,
           df1_name:calculation_df1,
           df2_name:calculation_df2}
    df = pd.DataFrame(data)
    return df

#Function to Help Convert ERC-20 Values Based on Decimal Value
def decimal_divisor(num):
    string = '1' + '0' * num
    return int(string)