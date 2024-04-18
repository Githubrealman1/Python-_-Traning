import paramiko
import os
import base64

def generate_ssh_key_pair():
    # Generate a new RSA key pair
    key = paramiko.RSAKey.generate(2048)
    
    # Save the private key to a file
    private_key_path = '/github/workspace/id_rsa'
    key.write_private_key_file(private_key_path)
    print("Private key saved to:", private_key_path)
    
    # Save the public key to a file
    public_key_path = '/github/workspace/id_rsa.pub'
    with open(public_key_path, 'w') as f:
        f.write(f"ssh-rsa {base64.b64encode(key.get_base())}")
    print("Public key saved to:", public_key_path)
    
    return private_key_path

def connect_with_ssh_key(private_key_path):
    try:
        # Create SSH client instance
        ssh_client = paramiko.SSHClient()
        
        # Automatically add host keys
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # Connect to localhost (your own machine)
        ssh_client.connect(hostname='localhost', pkey=private_key)
        
        print("Connected to localhost")
        
        # Perform operations here
        
        # Close the SSH connection
        ssh_client.close()
        print("Connection closed")
        
    except Exception as e:
        print("Failed to connect:", str(e))

# Generate SSH key pair
private_key_path = generate_ssh_key_pair()

# Connect to localhost using the generated key pair
connect_with_ssh_key(private_key_path)

# Clean up generated key files
os.remove(private_key_path)
os.remove('/github/workspace/id_rsa.pub')
