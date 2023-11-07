import uvicorn
import argparse
import os

# command line argument for blocking logins that defaults to False
parser = argparse.ArgumentParser()
parser.add_argument("--block_logins", default=False, action="store_true")
args = parser.parse_args()

# set the environment variable
os.environ["BLOCK_FORTI_LOGINS"] = str(args.block_logins)

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=443,
        host="0.0.0.0",
        ssl_keyfile="./certs/privkey.pem",
        ssl_certfile="./certs/fullchain.pem",
    )
