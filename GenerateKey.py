from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("encryption_key.txt", "wb")
file.write(key)
file.close()
#key generated : MWLoT3U7bS-m_g0VrpuueoLQHx1GF3DBVKTFUmb9JVg=
