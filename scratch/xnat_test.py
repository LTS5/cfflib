import cfflib as cf

a=cf.load('/path/to/meta.cml')

cf.set_xnat_connection({'server': 'http://localhost:8080/xnat', 'user':'myuser', 'password': 'mypassword'})

# push connectome object
#cf.xnat_push(a,  projectid = 'DEB02', subjectid= 'L01', experimentid = 'EXP4', overwrite = True)

# pull connectom object
cf.xnat_pull( projectid = 'DEB02', subjectid= 'L01', experimentid = 'EXP4', storagepath='/tmp')