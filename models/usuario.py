class Usuario:
    def __init__(self, vem_hash: str):
        self.vem_hash = vem_hash

    def to_dict(self):
        return {"vem_hash": self.vem_hash}
