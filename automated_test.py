import subprocess

def test_message_sending_and_receiving():
    subprocess.run(["python", "send_message.py"])
    subprocess.run(["python", "send_message_json.py"])
    subprocess.run(["python", "send_message_file_reference.py"])
    subprocess.run(["python", "send_message_with_attributes.py"])
    subprocess.run(["python", "send_message_large_payload.py"])
    subprocess.run(["python", "receive_message.py"])

if __name__ == "__main__":
    test_message_sending_and_receiving()
