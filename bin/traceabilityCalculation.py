import os, sys
import configure
import subprocess
import dendropy
import time

### Module where actual REvolver / BLAST cycles run takes place
### After every REvolver run, detection probability is checked with reciprocal Blast search and stored in a hash table
### Using the final hash table, decay rate is calculated using decay script

def main(prot_id, config_file):

	rootDir = os.getcwd()
 
	prot_config = configure.setParams(config_file)
	cache = prot_config.reuse_cache

	work_dir = prot_config.path_work_dir + '/' + prot_id
	os.chdir(work_dir)

	if os.path.exists(work_dir + '/omaId.txt'):
		blastHitId = open(work_dir + '/omaId.txt').read().split('\n')[0]
	else:
		sys.exit('### ERROR: No reciprocal BLAST hit id found!!!! ###')

	xml_file = 'revolver_config_' + prot_id + '.xml'
	#print xml_file
	proteome_file = 'proteome_' + prot_id

	trees = dendropy.TreeList.get_from_path(prot_config.simulation_tree, "newick")
	taxonset = []
	for element in trees.taxon_namespace:
		taxonset.append(str(element).replace("'", ""))
	taxonset = taxonset[::-1]
	detection_probability = {}
	for taxas in taxonset:
		detection_probability[taxas] = []
	
	print '##### Running REvolver / BLAST cycles: #####'
	start_time = time.time()

	command = 'java -Xmx2G -Xms2G -cp "%s" revolver %s' %(prot_config.REvolver, xml_file)
	print 'REvolver calculations command: ', command

	if cache and os.path.exists('decay_summary_%s.txt_parameter' %prot_id):
		pass
	else:
		for i in range(int(prot_config.simulation_runs)):
			print 'Run: ', i + 1

			success = False
			trials = 0
			while(not success and trials < 10):
				trials += 1
				try:
					run_revolver(prot_config.REvolver, xml_file)
					blastOutput = run_blast(prot_config.blastp, prot_id, proteome_file)
					for taxa in taxonset:
						detection = 0
						for line in blastOutput.split('\n'):
							#print line
							if taxa == line.split('\t')[0]:
								if line.split('\t')[1] == blastHitId:
									detection = 1
									break
						detection_probability[taxa].append(detection)
					success = True
				except KeyboardInterrupt:
					sys.exit('Keyboard interruption by user!!!')
				except:
					pass

		if trials >= 10:
			sys.exit('TOO MANY TRIALS FOR REVOLVER!!! Check REvolver configuration file.')
	
		print '#####\tTIME TAKEN: %s mins REvolver/BLAST#####' %((time.time() - start_time) / 60)

		ffull = open('full_decay_results_%s.txt' %prot_id, 'w')
		fsum = open('decay_summary_%s.txt' %prot_id, 'w')

		for taxa in taxonset:
			ffull.write(taxa + ' ')
			count = 0
			for element in detection_probability[taxa]:
				ffull.write(str(element))
				count += int(element)
			ffull.write('\n')
			fsum.write(str(float(count) / float(prot_config.simulation_runs)) + '\n')
		ffull.close()
		fsum.close()

		print '##### Calculating decay parameters #####'
		decayParams(prot_config.R, prot_id, prot_config.decay_script)

	os.chdir(rootDir)

def decayParams(r, prot_id, decay_script):
	command = '%s --vanilla --file=%s --args decay_summary_%s.txt' %(r, decay_script, prot_id)
	print '##### Decay parameter calculation command: ', command	
	os.system(command)
		
def run_revolver(REvolver, xml_file):
	#print 'java -Xmx2G -Xms2G -cp "%s" revolver %s' %(REvolver, xml_file)
	command = 'java -Xmx2G -Xms2G -cp "%s" revolver %s' %(REvolver, xml_file)
	#print '##### REvolver calculations command: ', command
	os.system(command)

def run_blast(blastp, prot_id, proteome):
	command = '%s -query REvolver_output/out.fa -db %s -outfmt 6 -max_target_seqs 5' %(blastp, proteome)
	result = subprocess.check_output(command, shell=True)
	return result
	
