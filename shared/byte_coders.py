def enc(string: str) -> bytes:
  """"ASCII-encodes a string."""
  return bytes(string, "ascii")

def dec(bytes: bytes) -> str:
  """Decodes bytes to a string using ASCII."""
  return bytes.decode("ascii")