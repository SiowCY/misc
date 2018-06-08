
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
#WITH
#   vulnerability_metadata AS (
#	  SELECT *
#		 
#	  FROM dim_vulnerability dv
#   ),
#   assets_grouped_by_site_and_vulnerability AS (
#	  SELECT site_id, vulnerability_id, array_to_string(array_agg(ip_address || (CASE WHEN host_name IS NULL THEN '' ELSE ' (' || host_name || ')' END)), ', ') AS affected_assets
#	  FROM fact_asset_vulnerability_finding
#		 JOIN dim_asset USING (asset_id)
#		 JOIN dim_site_asset USING (asset_id)
#	  GROUP BY site_id, vulnerability_id
#   ),
#   best_solutions_for_vulnerabilities AS (
#	  SELECT vulnerability_id, array_to_string(array_agg(ds.summary || ': ' || proofAsText(ds.fix)), E'\n\n') AS solutions
#	  FROM dim_vulnerability_solution
#		 JOIN dim_solution_highest_supercedence dshs USING (solution_id)
#		 JOIN dim_solution ds ON ds.solution_id = dshs.superceding_solution_id
#	  WHERE vulnerability_id IN (SELECT DISTINCT vulnerability_id FROM assets_grouped_by_site_and_vulnerability)
#	  GROUP BY vulnerability_id
#   ),
#   vuln_cves_ids AS (
#		SELECT vulnerability_id, array_to_string(array_agg(reference), ',') AS cves
#		FROM dim_vulnerability_reference
#		WHERE source = 'CVE'
#		GROUP BY vulnerability_id
#   )
#SELECT 
#   da.ip_address AS "ip_address",
#   da.host_name as "Host Name",
#   dos.name AS "OS", 
#   dos.version AS "OS Version",  
#   vm.title AS "Title",
#   proofAsText(vm.description) AS "description",
#	solutions AS "fix",
#	proofAsText(favi.proof) as "summary",	
#   round(vm.cvss_score::numeric, 1) AS "Original CVSS Score",
#   vcves.cves AS "Vulnerability CVE IDs",
#	CASE
#		WHEN vm.cvss_score = 10 THEN
#		'Critical'
#		WHEN vm.cvss_score BETWEEN 7
#		AND 9.9 THEN
#		'High'
#		WHEN vm.cvss_score BETWEEN 4
#		AND 6.9 THEN
#		'Medium'
#		WHEN vm.cvss_score BETWEEN 0
#		AND 3.9 THEN
#		'Low'
#	END AS "Original Severity",
#	   CASE
#		WHEN favi.port = -1 THEN
#		'0'
#		WHEN favi.port = favi.port THEN
#		favi.port
#	END AS "Port"
#FROM fact_asset_vulnerability_instance favi
#   JOIN dim_asset da USING (asset_id)
#   JOIN dim_operating_system dos USING (operating_system_id)
#   JOIN vulnerability_metadata vm USING (vulnerability_id)
#   JOIN best_solutions_for_vulnerabilities USING (vulnerability_id)
#   LEFT OUTER JOIN vuln_cves_ids vcves USING (vulnerability_id)
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
