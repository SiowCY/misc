# coding: utf-8

import xml.etree.ElementTree as et
import sys, argparse, csv, sqlite3, os, re, time

''' PENDING
### Import data to MySQL ###
#import MySQLdb

#mydb = MySQLdb.connect(host='10.0.0.1',user='root',passwd='password',db='dbname',charset='utf8')
#cursor = mydb.cursor()

'''


#getroot
#findall
#tag
#attrib

report_name = ""
report_host = ""
host_properties = ""
host_end = ""
last_unauth = ""
cred_scan = ""
policy_used = ""
target_os = ""
host_ip = ""
host_fqdn = ""
host_start = ""
report_port = ""

	
#0=Information 1=Low 2=Medium 3=High 4=Critical
issue_severity = ""
plugin_id = ""
plugin_name = ""
plugin_family = ""
plugin_description = ""
plugin_fname = ""
risk_factor = ""
plugin_solution = ""
plugin_synopsis = ""
plugin_outputs = ""

# Compliance variable
compliance_check_id = ""
compliance_check_name = ""
compliance_info = ""
compliance_policy_value = ""
compliance_actual_value = ""
compliance_result = ""
compliance_audit_file = ""
compliance_error = ""


remove_html_tag = re.compile('<.*?>')

parser = argparse.ArgumentParser(description='Nessus XML to sqlite3 db to csv')
parser.add_argument('-i', '--input', help='Insert Nessus XML .nessus XML', action='store')
args = parser.parse_args()

### Stand alone sqlite format, create new database ### 

xmlfile = args.input
filename = xmlfile.split('.')
fn = filename[0]
outxml = fn+"-edited.xml"

# Append the XML format
with open(xmlfile,"rt") as input1:
	with open(outxml,"wt") as output1:
		for line in input1:
			output1.write(line.replace('<cm:','<').replace('</cm:','</'))
fn1 = fn+'.db'
va_csv = fn+'-VA.csv'
comp_csv = fn+'-comp.csv'

table1 = "report"
table2 = "issue"
table3 = "compliance"
conn = sqlite3.connect(fn1)
cur = conn.cursor()
#cur.executescript("DROP TABLE IF EXISTS "+table+";")

try:
	cur.execute("CREATE TABLE "+table1+" (report_name TEXT, report_host TEXT, cred_scan TEXT, host_end TEXT, host_start TEXT, host_ip TEXT, policy_used TEXT, target_os TEXT);")
	
	cur.execute("CREATE TABLE "+table2+" (report_name TEXT, report_host TEXT, report_port TEXT, plugin_id TEXT, plugin_name TEXT, plugin_family TEXT, plugin_description TEXT, plugin_fname TEXT, risk_factor TEXT, plugin_solution TEXT, plugin_synopsis TEXT, plugin_outputs TEXT, report_host_port TEXT);")
	
	cur.execute("CREATE TABLE "+table3+" (report_name TEXT, report_host TEXT, compliance_check_id TEXT, compliance_check_name TEXT, compliance_info TEXT, compliance_policy_value TEXT, compliance_actual_value TEXT, compliance_error TEXT, compliance_result TEXT, compliance_audit_file TEXT, plugin_id TEXT, plugin_name TEXT, plugin_synopsis TEXT, plugin_family TEXT, plugin_fname TEXT);")

except:
	print "Existing table was found."

tree = et.parse(outxml)
root = tree.getroot()
for main in root.findall('Report'):

	# Report Name
	reportname = main.attrib

	#report_name.append(reportname.get('name'))
	report_name = reportname.get('name')

	# Report Host
	reporthost = main.findall('ReportHost')
	#print reporthost

	for report_host1 in reporthost:
		report_host = report_host1.get('name')
		#report_host.append(report_host1.get('name'))
		#print report_host

		host_property = report_host1.find('HostProperties')	

		for host_properties in host_property.findall('tag'):
			host_name = host_properties.get('name')
			#print host_name
			
			if host_name == "HOST_END":
				#host_end.append(host_properties.text)
				host_end = host_properties.text
			if host_name == "Credentialed_Scan":
				#cred_scan.append(host_properties.text)
				cred_scan = host_properties.text
			if host_name == "policy-used":
				#policy_used.append(host_properties.text)
				policy_used = host_properties.text
			if host_name == "operating-system":
				#target_os.append(host_properties.text)
				target_os = host_properties.text
			if host_name == "host-ip":
				#host_ip.append(host_properties.text)
				host_ip = host_properties.text
			if host_name == "HOST_START":
				#host_start.append(host_properties.text)				
				host_start = host_properties.text			
		
		#print report_detail
		cur.execute('INSERT INTO report (report_name, report_host, host_ip, target_os, cred_scan, host_start, host_end, policy_used) VALUES (?,?,?,?,?,?,?,?)',(report_name, report_host, host_ip, target_os, cred_scan, host_start, host_end, policy_used))
				
		conn.commit()

		for report_items in report_host1.findall('ReportItem'):
			report_items_pluginName = report_items.get('pluginName')
			if 'Compliance Checks' in report_items_pluginName:
				
			#report_items = report_host1.find('ReportItem')
		
			#report_port.append(report_items.get('port'))
				#report_port = report_items.get('port')
				
				#issue_severity.append(report_items.get('severity'))
				issue_severity = report_items.get('severity')
				
				
				for issue_severity_details in issue_severity:
					#print issue_severity_details
					if issue_severity_details == '0':		
						issue_severity = "INFO"
						
					elif issue_severity_details == '1':				
						issue_severity = "LOW"
						
					elif issue_severity_details == '2':				
						issue_severity = "MEDIUM"
						
					elif issue_severity_details == '3':
						issue_severity = "HIGH"
						
					elif issue_severity_details == '4':
						issue_severity = "CRITICAL"
						
				#plugin_id.append(report_items.get('pluginID'))
				plugin_id = report_items.get('pluginID')
				
				#plugin_name.append(report_items.get('pluginName'))
				plugin_name = report_items.get('pluginName')
				
				#plugin_family.append(report_items.get('pluginFamily'))
				plugin_family = report_items.get('pluginFamily')
				
				#plugin_fname.append(report_items.find('fname').text)
				plugin_fname = report_items.find('fname').text
				
				#risk_factor.append(report_items.find('risk_factor').text)
				risk_factor = report_items.find('risk_factor').text	
				
				#compliance_check_name 
				try:
					compliance_check_name = report_items.find('compliance-check-name').text
					if compliance_check_name is None:
						compliance_check_name = ""
					else:
						compliance_check_name = compliance_check_name.replace('&apos;',"'")
				except:
					pass
				
				#compliance-actual-value 
				try: 
					compliance_actual_value = report_items.find('compliance-actual-value').text
					if compliance_actual_value is None:
						compliance_actual_value = ""
					else:
						compliance_error = ""
				except:
					pass
						
				
				#compliance-audit-file
				try:
					compliance_audit_file = report_items.find('compliance-audit-file').text
					if compliance_audit_file is None:
						compliance_audit_file = ""
					else:
						compliance_error = ""
				except:
					pass
				
				#compliance-check-id
				try:
					compliance_check_id = report_items.find('compliance-check-id').text
					if compliance_check_id is None:
						compliance_check_id = ""
					else:
						compliance_error = ""
				except:
					pass
				
				#compliance-policy-value
				try:
					compliance_policy_value = report_items.find('compliance-policy-value').text.strip('\n')
					if compliance_policy_value is None:
						compliance_policy_value = ""
					else:
						compliance_error = ""
				except: 
					pass
				#compliance-info
				try:
					compliance_info = report_items.find('compliance-info').text.strip('\n')
					if compliance_info is None:
						compliance_info = ""
					else:
						compliance_error = ""
				except:
					pass
				#compliance-error
				try:
					compliance_error = report_items.find('compliance-error').text
					if compliance_error is None:
						compliance_error = ""
					else:
						compliance_info = ""
						compliance_policy_value = ""
						compliance_actual_value = ""
						compliance_audit_file = ""
				except:
					pass			
				#compliance-result
				try:
					compliance_result = report_items.find('compliance-result').text
					if compliance_result is None:
						compliance_result = ""
				except:
					pass
					
				#compliance-solution
				try:
					compliance_solution = report_items.find('compliance-solution').text
					if compliance_solution is None:
						compliance_solution = ""
					else:
						compliance_solution = compliance_solution.replace('&apos;',"'")
				except:
					pass
	
				cur.execute('INSERT INTO compliance (report_name, report_host, compliance_check_id, compliance_check_name, compliance_info, compliance_policy_value, compliance_actual_value, compliance_error, compliance_result, compliance_audit_file, plugin_id, plugin_name, plugin_family, plugin_fname) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(report_name, report_host, compliance_check_id, compliance_check_name, compliance_info, compliance_policy_value, compliance_actual_value, compliance_error, compliance_result, compliance_audit_file, plugin_id, plugin_name, plugin_family, plugin_fname))
				conn.commit()
				
			else:
				report_port = report_items.get('port')
			
			#issue_severity.append(report_items.get('severity'))
				issue_severity = report_items.get('severity')
			
				for issue_severity_details in issue_severity:
					#print issue_severity_details
					if issue_severity_details == '0':		
						issue_severity = "INFO"
						
					elif issue_severity_details == '1':				
						issue_severity = "LOW"
						
					elif issue_severity_details == '2':				
						issue_severity = "MEDIUM"
						
					elif issue_severity_details == '3':
						issue_severity = "HIGH"
						
					elif issue_severity_details == '4':
						issue_severity = "CRITICAL"
						
				#plugin_id.append(report_items.get('pluginID'))
				plugin_id = report_items.get('pluginID')
				
				#plugin_name.append(report_items.get('pluginName'))
				plugin_name = report_items.get('pluginName')
				
				#plugin_family.append(report_items.get('pluginFamily'))
				plugin_family = report_items.get('pluginFamily')
				
				#plugin_description.append(report_items.find('description').text)
				plugin_description = report_items.find('description').text
				
				#plugin_fname.append(report_items.find('fname').text)
				plugin_fname = report_items.find('fname').text
				
				#risk_factor.append(report_items.find('risk_factor').text)
				risk_factor = report_items.find('risk_factor').text
				
				#plugin_solution.append(report_items.find('solution').text)
				try:
					plugin_solution = report_items.find('solution').text
					if plugin_solution is None:
						plugin_solution = ""
				except:
					plugin_solution = ""
					pass
				
				#plugin_synopsis.append(report_items.find('synopsis').text)
				try:
					plugin_synopsis = report_items.find('synopsis').text
					if plugin_synopsis is None:
						plugin_synopsis = ""
				except:
					plugin_synopsis = ""
					pass
					
				try:
					plugin_outputs = report_items.find('plugin_output').text.strip('\n')
					if plugin_outputs is None:
						plugin_outputs = ""
				except:
					plugin_outputs = ""
					pass
				
				
				if risk_factor == "None":
					pass
				else:
				# Insert into DB base on IP
					#cur.execute('INSERT INTO issue (report_host, report_port, plugin_id, plugin_name, plugin_family, plugin_description, plugin_fname, risk_factor, plugin_solution, plugin_synopsis, plugin_outputs) VALUES (?,?,?,?,?,?,?,?,?,?,?)',(report_host, report_port, plugin_id, plugin_name, plugin_family, plugin_description, plugin_fname, risk_factor, plugin_solution, plugin_synopsis, plugin_outputs))
					#conn.commit()
					
				# Insert into DB base on vuln
					cur.execute('INSERT INTO issue (report_name, report_host, report_port, plugin_id, plugin_name, plugin_family, plugin_description, plugin_fname, risk_factor, plugin_solution, plugin_synopsis, plugin_outputs, report_host_port) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',(report_name, report_host, report_port, plugin_id, plugin_name, plugin_family, plugin_description, plugin_fname, risk_factor, plugin_solution, plugin_synopsis, plugin_outputs, report_host))
					conn.commit()
					
	# Compliance Report Generating
		cur.execute('select report_name, report_host, compliance_check_id, compliance_check_name, compliance_info, compliance_policy_value, compliance_actual_value, compliance_error, compliance_result, compliance_audit_file from compliance')
	
	# Compliance Report Generating to CSV
	with open(comp_csv,"wb") as new_csv:
		csv_writer = csv.writer(new_csv)
		csv_writer.writerow([i[0] for i in cur.description]) # write headers
		csv_writer.writerows(cur)
	

	# VA Report Generating 
		cur.execute("update issue SET report_host_port = (report_host || ':' || report_port)")
		cur.execute("update issue SET report_host_port = replace(report_host_port, ':0' , '')")

		cur.execute('select report_name, replace(group_concat(DISTINCT (report_host_port)), "," , "\n") report_host, plugin_id, plugin_name, plugin_family, plugin_description, plugin_fname, risk_factor, replace(group_concat(distinct plugin_solution), "," , "\n") plugin_solution, replace(group_concat(distinct plugin_synopsis), "," , "\n")plugin_synopsis, plugin_outputs from issue group by plugin_id, plugin_name order by risk_factor asc')
	
	# VA Report Generating to CSV
	with open(va_csv,"wb") as newva_csv:
		csv_writer = csv.writer(newva_csv)
		csv_writer.writerow([i[0] for i in cur.description]) # write headers
		csv_writer.writerows(cur)
	
	conn.commit()
	conn.close()
