from tuf.repository_tool import *

import datetime

repository = create_new_repository("repository")

repository.root.threshold = 2

# The root keys loaded to satisfy root's threshold.
user1_root_key = import_ed25519_privatekey_from_file("keystore/user1_root", password='passwd')
user2_root_key = import_ed25519_privatekey_from_file("keystore/user2_root", password='passwd')

# Any of these four root keys may be used to satisfy root's threshold.
repository.root.add_verification_key(import_ed25519_publickey_from_file("keystore/user1_root.pub"))
repository.root.add_verification_key(import_ed25519_publickey_from_file("keystore/user2_root.pub"))
repository.root.add_verification_key(import_ed25519_publickey_from_file("keystore/user3_root.pub"))
repository.root.add_verification_key(import_ed25519_publickey_from_file("keystore/user4_root.pub"))

repository.root.load_signing_key(user1_root_key)
repository.root.load_signing_key(user2_root_key)

# Add the public keys for the remaining top-level roles.
repository.targets.add_verification_key(import_ed25519_publickey_from_file("keystore/targets.pub"))
repository.snapshot.add_verification_key(import_ed25519_publickey_from_file("keystore/snapshot.pub"))
repository.timestamp.add_verification_key(import_ed25519_publickey_from_file("keystore/timestamp.pub"))

repository.targets.load_signing_key(import_ed25519_privatekey_from_file("keystore/targets", password='passwd'))
repository.snapshot.load_signing_key(import_ed25519_privatekey_from_file("keystore/snapshot", password='passwd'))
repository.timestamp.load_signing_key(import_ed25519_privatekey_from_file("keystore/timestamp", password='passwd'))

repository.timestamp.expiration = datetime.datetime(2044, 10, 28, 12, 8)

repository.targets.compressions = ["gz"]
repository.snapshot.compressions = ["gz"]
# Write all the metadata to disk, signing metadata according to the private
# keys loaded for each role.
repository.write()
