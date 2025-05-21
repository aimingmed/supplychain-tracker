#run the setup script to create the DB and the schema in the DB
#do this in a loop because the timing for when the SQL instance is ready is indeterminate
sleep 10


for i in {1..50};
do
    # specify socket path to avoid "Can't connect to local MySQL server through socket" error
    mysql -u root -pexample  < /usr/src/setup/setup.sql

    if [ $? -eq 0 ]
    then
        echo "setup.sql completed"
        break
    else
        echo "not ready yet..."
        sleep 1
    fi
done

