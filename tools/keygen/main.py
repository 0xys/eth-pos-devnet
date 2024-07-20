import os
import sys
import json

from py_ecc.bls import G2ProofOfPossession as bls

from staking_deposit.key_handling.key_derivation.path import mnemonic_and_path_to_key

from staking_deposit.key_handling.key_derivation.path import mnemonic_and_path_to_key
from staking_deposit.utils.constants import (
    ETH1_ADDRESS_WITHDRAWAL_PREFIX,
    WORD_LISTS_PATH,
    ETH2GWEI,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)
from staking_deposit.utils.ssz import (
    compute_deposit_domain,
    compute_signing_root,
    BLSToExecutionChange,
    DepositData,
    DepositMessage,
    SignedBLSToExecutionChange,
)

from staking_deposit.settings import (
    ALL_CHAINS,
    MAINNET,
    PRATER,
    BaseChainSetting,
    DEPOSIT_CLI_VERSION,
    get_chain_setting,
)

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
    
    withdrawal_addr =  os.getenv('WITHDRAWAL_ADDRESS')
    if num is None:
        raise ValueError("Please set the NUM_VALIDATORS environment variable")
    
    genesis_for_version = os.getenv('GENESIS_FORK_VERSION')
    if genesis_for_version is None:
        raise ValueError("Please set the NUM_VALIDATORS environment variable")
    
    network_name = os.getenv('NETWORK_NAME')
    if network_name is None:
        raise ValueError("Please set the NETWORK_NAME environment variable")
    
    
    withdrawal_credentials = ETH1_ADDRESS_WITHDRAWAL_PREFIX
    withdrawal_credentials += b'\x00' * 11
    withdrawal_credentials += bytes.fromhex(withdrawal_addr[2:])
    
    deposits = []

    for index in range(0, int(num)):
        key_path = f"m/12381/3600/0/{index}"
        # Derive the key from the mnemonic and path
        sk = mnemonic_and_path_to_key(mnemonic=mnemonic, path=key_path, password=password)
        pub = bls.SkToPk(sk).hex()
        priv = sk.to_bytes(32, 'big').hex()
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

        deposit_msg = DepositMessage(
            pubkey=bytes.fromhex(pub),
            withdrawal_credentials=withdrawal_credentials,
            amount=32*ETH2GWEI,
        )

        domain = compute_deposit_domain(fork_version=bytes.fromhex(genesis_for_version[2:]))
        signing_root = compute_signing_root(deposit_msg, domain)

        signed_deposit = DepositData(
            **deposit_msg.as_dict(),
            signature=bls.Sign(sk, signing_root),
        )
    
        datum_dict = signed_deposit.as_dict()
        datum_dict.update({'deposit_message_root': deposit_msg.hash_tree_root})
        datum_dict.update({'deposit_data_root': signed_deposit.hash_tree_root})
        datum_dict.update({'fork_version': genesis_for_version})
        datum_dict.update({'network_name': network_name})
        datum_dict.update({'deposit_cli_version': DEPOSIT_CLI_VERSION})
        deposits.append(datum_dict)
    
    with open(f"{location}/deposits.json", 'w+') as f:
        f.write(json.dumps(deposits, default=lambda x: x.hex()))


