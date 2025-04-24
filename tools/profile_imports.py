import subprocess

subprocess.run([
    "python", "-X", "importtime", "-c", "import xgi"
])

output = subprocess.check_output([
    "python", "-X", "importtime", "-c", "import your_module"
], stderr=subprocess.STDOUT)

print(output.decode())