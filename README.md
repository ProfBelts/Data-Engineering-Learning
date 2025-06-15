# Data Engineering Week 1 Dockerizing the Ingestion Script

YT Link: https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=9


1. Convert the jupyter notebook to a script.
    - jupyter nbconvert --to=script upload-data.ipynb

2. Make sure to add argparse to pass params in the engine.  (3:00 min section of the video)

3.  Build the docker image
    - docker build -t taxi_ingest:v001 . 

4. Run the docker image
    - Create the docker network
        Ex. docker network create pg-network

    - Use the ipv4 address to make the download of the csv file faster.
    - Run the ff:
            URL='http://192.168.0.105:8000/yellow_tripdata_2021-01.csv'

            docker network create pg-network  # Only if not yet created

            docker run -it \
            --network=pg-network \
            taxi_ingest:v001 \
            --user=root \
            --password=root \
            --host=pg-database \
            --port=5432 \
            --db=ny_taxi \
            --table_name=yellow_taxi_trips \
            --url=${URL}

