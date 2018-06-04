#
# Example Python client for University Registration DB
#

import psycopg2


class SchemaCreator:
# connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
	userid   = "y18s1c9120_zyan3302"
	passwd   = "430005932"
	myHost = "soit-db-pro-2.ucc.usyd.edu.au"

# instance variable for the database connection   
	conn = None 
	


    # Establishes a connection to the database.
    # The connection parameters are read from the instance variables above
    # (userid, passwd, and database).
    # @returns  true   on success and then the instance variable 'conn' 
    #                  holds an open connection to the database.
    #           false  otherwise
#
	def connectToDatabase(self):
		try:
			#connect to the database
			self.conn = psycopg2.connect(database=self.userid,user=self.userid,password=self.passwd,host=self.myHost)
			return True

		except psycopg2.Error as sqle:       
			#TODO: add error handling #/
			print("psycopg2.Error : " + sqle.pgerror)
			return False


	# open ONE single database connection
	def openConnection (self):
		retval = True
		if self.conn is not None :
			print("You are already connected to the database no second connection is needed!")
		else:
			if self.connectToDatabase():
				print("You successfully connected to the database.")
			else:
				print("Oops - something went wrong.")
				retval = False
		return retval
		

# close the database connection again
	def closeConnection (self): 
		if self.conn is None :
			print("You are not connected to the database!")
		else:
			try:      
				self.conn.close() # close the connection again after usage! 
				self.conn = None      
			except psycopg2.Error as sqle:       
				#TODO: add error handling #/
				print("psycopg2.Error : " + sqle.pgerror)

	def createSchema(self):
		try:

			curs = self.conn.cursor()

			# execute the query
			curs.execute("""
CREATE TABLE IF NOT EXISTS A3_USER
(FIRSTNAME VARCHAR(100) not null, 
LASTNAME VARCHAR(100) not null, 
ID SERIAL primary key);

Insert into A3_USER (FIRSTNAME,LASTNAME) values ('Dean','Smith');

CREATE TABLE IF NOT EXISTS A3_ISSUE 
(ID SERIAL primary key, 
DESCRIPTION VARCHAR(1000), 
PROJECTID INT, 
TITLE VARCHAR(100),  
CREATOR INT not null REFERENCES A3_USER, 
RESOLVER INT REFERENCES A3_USER, 
VERIFIER INT REFERENCES A3_USER);

Insert into A3_ISSUE (TITLE,DESCRIPTION,CREATOR,RESOLVER,VERIFIER) values ('Division by zero','Division by 0 doesn''t yield error or infinity as would be expected. Instead it results in -1.',1,1,1);

Insert into A3_ISSUE (TITLE,DESCRIPTION,CREATOR,RESOLVER,VERIFIER) values ('Factorial with addition anomaly','Performing a factorial and then addition produces an off by 1 error',1,1,1);

Insert into A3_ISSUE (TITLE,DESCRIPTION,CREATOR,RESOLVER,VERIFIER) values ('Incorrect BODMAS order','Addition occurring before multiplication',1,1,1);
""")
			self.conn.commit()
			# clean up! (NOTE this really belongs in a finally block) 
			curs.close()

		except psycopg2.Error as sqle:       
			#TODO: add error handling #/
			print("psycopg2.Error : " + sqle.pgerror)
##
# Main program.
#/

# create our actual client and test the database connection
creator = SchemaCreator()

if ( creator.openConnection() ):
        # create schema
        creator.createSchema()
