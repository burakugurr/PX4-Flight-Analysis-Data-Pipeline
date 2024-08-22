from pyulog import *
import os

class ParseUlog:
    def convert_ulog2csv(self,ulog_file_name):
        ulog = ULog(ulog_file_name)
        data = ulog.data_list
        delimiter = ','
        
        time_s = None
        time_e = None
        
        output_file_prefix = ulog_file_name
        # strip '.ulg'
        if output_file_prefix.lower().endswith('.ulg'):
            output_file_prefix = output_file_prefix[:-4]

        base_name = os.path.basename(output_file_prefix)
        output_file_prefix = os.path.join("../outputs", base_name)

        for d in data:
            fmt = '{0}_{1}_{2}.csv'
            output_file_name = fmt.format(output_file_prefix, d.name.replace('/', '_'), d.multi_id)
            fmt = 'Writing {0} ({1} data points)'
    
            with open(output_file_name, 'w', encoding='utf-8') as csvfile:

                # use same field order as in the log, except for the timestamp
                data_keys = [f.field_name for f in d.field_data]
                data_keys.remove('timestamp')
                data_keys.insert(0, 'timestamp')  # we want timestamp at first position

                csvfile.write(delimiter.join(data_keys) + '\n')

                #get the index for row where timestamp exceeds or equals the required value
                time_s_i = np.where(d.data['timestamp'] >= time_s * 1e6)[0][0] \
                        if time_s else 0
                #get the index for row upto the timestamp of the required value
                time_e_i = np.where(d.data['timestamp'] >= time_e * 1e6)[0][0] \
                        if time_e else len(d.data['timestamp'])

                # write the data
                last_elem = len(data_keys)-1
                for i in range(time_s_i, time_e_i):
                    for k in range(len(data_keys)):
                        csvfile.write(str(d.data[data_keys[k]][i]))
                        if k != last_elem:
                            csvfile.write(delimiter)
                    csvfile.write('\n')

# test
# ParseUlog().convert_ulog2csv('/home/rocky/Flight-Analysis/src/minIO/Downloads/main.ulog')