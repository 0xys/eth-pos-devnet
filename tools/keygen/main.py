import os
import sys

from py_ecc.bls import G2ProofOfPossession as bls

from staking_deposit.key_handling.key_derivation.path import mnemonic_and_path_to_key

if __name__ == '__main__':
    mnemonic = os.getenv('MNEMONIC')
    if mnemonic is None:
        raise ValueError("Please set the MNEMONIC environment variable")

    password = os.getenv('PASSWORD')
    if password is None:
        password = ""
    
    location = os.getenv('KEYSTORE_PATH')
    if location is None:
        raise ValueError("Please set the KEYSTORE_PATH environment variable")
    
    num = os.getenv('NUM_VALIDATORS')
    if num is None:
        raise ValueError("Please set the NUM_VALIDATORS environment variable")

    for index in range(0, int(num)):
        key_path = f"m/12381/3600/0/{index}"
        # Derive the key from the mnemonic and path
        key = mnemonic_and_path_to_key(mnemonic=mnemonic, path=key_path, password=password)
        pub = bls.SkToPk(key).hex()
        priv = key.to_bytes(32, 'big').hex()
        print(f"{index}:")
        print(f"  Public key: {pub}")
        print(f"  Private key: {priv}")

        data = {
            'type': 'file-raw',
            'keyType': 'BLS',
            'privateKey': f'0x{priv}'
        }

        # save to yaml
        with open(f"{location}/key_{pub}.yaml", 'w+') as f:
            for key, value in data.items():
                f.write(f"{key}: \"{value}\"\n")

