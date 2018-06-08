
"""
#################################################################
# Example: python report-gen.py -i <Nexpose.csv>		#
# The output for the csv file name will be Nexpose-edited.csv	#
#								#
# Created by Yik - Feels free to edit				#
#								#
# Please use the following SQL Query to export the CSV from	#
# Nexpose, else this script will not able to generate the CSV	#
#								#
#################################################################
# ============================================================= #
# WITH															
#    asset_ips AS (
#       SELECT asset_id, ip_address, type
#       FROM dim_asset_ip_address dips
#    ),
#    asset_addresses AS (
#       SELECT da.asset_id,
#          (SELECT array_to_string(array_agg(ip_address), ',') FROM asset_ips WHERE asset_id = da.asset_id AND type = 'IPv4') AS ipv4s,
#          (SELECT array_to_string(array_agg(ip_address), ',') FROM asset_ips WHERE asset_id = da.asset_id AND type = 'IPv6') AS ipv6s,
#          (SELECT array_to_string(array_agg(mac_address), ',') FROM dim_asset_mac_address WHERE asset_id = da.asset_id) AS macs
#       FROM dim_asset da
#          JOIN asset_ips USING (asset_id)
#    ),
#    asset_names AS (
#       SELECT asset_id, array_to_string(array_agg(host_name), ',') AS names
#       FROM dim_asset_host_name
#       GROUP BY asset_id
#    ),
#    asset_facts AS (
#       SELECT asset_id, riskscore, exploits, malware_kits
#       FROM fact_asset
#    ),
#    vulnerability_metadata AS (
#       SELECT *
#          
#       FROM dim_vulnerability dv
#    )
# SELECT 
#    ds.name AS "site",
#    da.ip_address AS "ip", 
#    --dos.name AS "Asset OS Name", dos.version AS "Asset OS Version",  
#    --dsvc.name AS "Service Name",
#    favi.port AS "port",
#    vm.title AS "title",
#    proofAsText(vm.description) AS "descrip",
#    vm.severity AS "seve",
#    proofAsText(dsol.fix) AS "sol"  
#    
# FROM fact_asset_vulnerability_instance favi
#    JOIN dim_asset da USING (asset_id)
#    LEFT OUTER JOIN asset_addresses aa USING (asset_id)
#    LEFT OUTER JOIN asset_names an USING (asset_id)
#    JOIN dim_operating_system dos USING (operating_system_id)
#    JOIN asset_facts af USING (asset_id)
#    JOIN dim_service dsvc USING (service_id)
#    JOIN dim_protocol dp USING (protocol_id)
#    JOIN dim_site_asset dsa USING (asset_id)
#    JOIN dim_site ds USING (site_id)
#    JOIN vulnerability_metadata vm USING (vulnerability_id)
#    JOIN dim_vulnerability_solution dvss USING (vulnerability_id)
#    JOIN dim_solution dsol USING(solution_id)
#    JOIN dim_vulnerability_status dvs USING (status_id)
# 
# ============================================================= #
#################################################################
"""
import sys, argparse, csv, sqlite3, os

parser = argparse.ArgumentParser(description='Nexpose csv to sqlite3 db to csv')
parser.add_argument('-i', help='Insert Nexpose CSV File', action='store')


args = parser.parse_args()
filename = sys.argv[2].split('.')
fn = filename[0]
fn1 = fn+'.db'
wn1 = fn+'-edited.csv'
print "Table name: " + fn
fn = "internal"
if os.path.isfile(fn1):
	print "Similar databasae found, it will not create a new database."

else: 
	conn = sqlite3.connect(fn1)
	cur = conn.cursor()
	
	# Drop the table if exist
	cur.executescript("DROP TABLE IF EXISTS "+fn+";")
	try:
		cur.execute("CREATE TABLE "+fn+" (ip_address TEXT, 'Host Name' TEXT, OS TEXT, 'OS Version' TEXT, Title TEXT, description TEXT, fix TEXT, summary TEXT, 'Original CVSS Score' TEXT, 'Vulnerability CVE IDs' TEXT, 'Original Severity' TEXT, Port TEXT, ipport TEXT);")
	except:
		print "Existing table was found."
		
	# Insert the Nexpose CSV
	with open(sys.argv[2],'r') as f:
		dr = csv.DictReader(f)
		to_db = [(i['ip_address'],i['Host Name'],i['OS'],i['OS Version'],i['Title'],i['description'],i['fix'],i['summary'],i['Original CVSS Score'],i['Vulnerability CVE IDs'],i['Original Severity'],i['Port']) for i in dr]
		print type(to_db)
	cur.executemany("INSERT INTO "+fn+" (ip_address, 'Host Name', OS, 'OS Version', Title, description, fix, summary, 'Original CVSS Score', 'Vulnerability CVE IDs', 'Original Severity', Port) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);", to_db)
	
	# Concat IP and Port to single column 
	cur.execute("update "+fn+" SET ipport = (ip_address || ':' || Port)")
	cur.execute("update "+fn+" SET ipport = replace(ipport, ':0' , '')")
	
	# Concat IP:PORT and Solutions with unique Vuln Title
	cur.execute('select replace(group_concat(DISTINCT (ipport)), "," , "\n") ip_address, "Host Name", OS, "OS Version", Title, description, replace(group_concat(distinct fix), "," , "\n") fix, replace(group_concat(distinct summary), "," , "\n")summary, "Original CVSS Score", "Vulnerability CVE IDs", "Original Severity" from '+ fn +' group by Title, description order by "Original Severity" asc')

	print cur
	with open(wn1,"wb") as new_csv:
		csv_writer = csv.writer(new_csv)
		csv_writer.writerow([i[0] for i in cur.description]) # write headers
		csv_writer.writerows(cur)
	conn.commit()
	conn.close()
