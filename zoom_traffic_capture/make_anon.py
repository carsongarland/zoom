from yacryptopan import CryptoPAn
from secrets import token_bytes
from csv import reader, writer
from sys import argv
from ipaddress import ip_address, ip_network

non_columbia_ips = []
columbia_ips = []

cp = CryptoPAn(token_bytes(32))

def handle_ip(ip):
  if ip in columbia_ips:
    return cp.anonymize(ip)
  elif ip in non_columbia_ips:
    return ip
  else:
    for net in columbia_nets:
      if ip_address(ip) in ip_network(net):
        columbia_ips.append(ip)
        return cp.anonymize(ip)
  non_columbia_ips.append(ip)
  return ip

def handle_anon(file_name):
  read_name = file_name
  write_name = file_name.split('.')[0] + '_anon.csv'
  with open(read_name, 'r') as stats:
      with open(write_name, 'w') as stats_anon:
        stats = reader(stats)
        stats_anon = writer(stats_anon)
        header_flag = 1
        for row in stats:
            if header_flag == 1:
              ip_src_index = row.index('ip_src')
              ip_dst_index = row.index('ip_dst')
              header_flag = 0
            else:
              row[ip_src_index] = handle_ip(row[ip_src_index])
              row[ip_dst_index] = handle_ip(row[ip_dst_index])   
            stats_anon.writerow(row)

if __name__ == "__main__":
   for file in argv:
      if 'csv' in file:
        handle_anon(file)
