from flask import Flask, request, jsonify
from consistent_hash import ConsistentHashing
import docker
import requests
import time
import threading

app = Flask(__name__)
client = docker.from_env()
ch = ConsistentHashing()
servers = {}  # server_id → container
next_id = 1  # auto-incrementing server ID.


@app.route("/rep", methods=["GET"])
def get_servers():
    return jsonify(list(servers.keys())), 200


@app.route("/add", methods=["POST"])
def add_server():
    global next_id
    try:
        server_id = next_id
        container = client.containers.run(
            "ds-server",
            detach=True,
            environment={"SERVER_ID": str(server_id)},
            ports={"5000/tcp": None},
            network="ds_net",
            name=f"server-{server_id}",
            labels={"group": "ds"},
            restart_policy={"Name": "always"}
        )
        ch.add_server(server_id)
        servers[server_id] = container
        next_id += 1
        print(f"[+] Server {server_id} added")
        return jsonify({"message": f"Server {server_id} added"}), 201

    except Exception as e:
        print("ERROR while adding server:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/rm", methods=["DELETE"])
def remove_server():
    try:
        server_id = int(request.args.get("id"))
        if server_id in servers:
            servers[server_id].remove(force=True)
            del servers[server_id]
            ch.remove_server(server_id)
            print(f"[-] Server {server_id} removed")
            return jsonify({"message": f"Server {server_id} removed"}), 200
        return jsonify({"error": "Server not found"}), 404
    except:
        return jsonify({"error": "Invalid request"}), 400


@app.route("/<path:subpath>", methods=["GET"])
def route_request(subpath):
    try:
        request_id = int(request.args.get("id", 0))
        server_id = ch.get_server(request_id)

        if server_id is None or server_id not in servers:
            return jsonify({"error": "No available servers"}), 503

        # Use container DNS name inside Docker network
        target_url = f"http://server-{server_id}:5000/{subpath}"
        resp = requests.get(target_url, params=request.args)

        return (resp.text, resp.status_code, resp.headers.items())

    except Exception as e:
        print("ERROR forwarding request:", str(e))
        return jsonify({"error": str(e)}), 500


def heartbeat_loop():
    while True:
        print("[HB] Checking servers...")
        time.sleep(5)
        for server_id in list(servers.keys()):
            try:
                url = f"http://server-{server_id}:5000/heartbeat"
                r = requests.get(url, timeout=2)
                if r.status_code != 200:
                    raise Exception("Not healthy")
            except:
                print(f"[!] Server {server_id} failed heartbeat. Restarting...")

                # Remove dead container
                try:
                    servers[server_id].remove(force=True)
                except:
                    pass

                del servers[server_id]
                ch.remove_server(server_id)

                # Re-create the same server
                try:
                    container = client.containers.run(
                        "ds-server",
                        detach=True,
                        environment={"SERVER_ID": str(server_id)},
                        ports={"5000/tcp": None},
                        network="ds_net",
                        name=f"server-{server_id}",
                        labels={"group": "ds"},
                        restart_policy={"Name": "always"}
                    )
                    servers[server_id] = container
                    ch.add_server(server_id)
                    print(f"[+] Server {server_id} restarted")
                except Exception as e:
                    print(f"[!] Failed to restart server {server_id}: {e}")


# Start heartbeat thread
heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
heartbeat_thread.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
