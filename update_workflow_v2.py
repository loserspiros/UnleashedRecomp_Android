import sys

with open('new_block.sh', 'r') as f:
    new_block_lines = f.readlines()

with open('.github/workflows/release.yml', 'r') as f:
    lines = f.readlines()

# Range to replace (inclusive, 1-based: 179 to 258)
start = 179
end = 258

new_lines = lines[:start-1] + new_block_lines + lines[end:]

with open('.github/workflows/release.yml', 'w') as f:
    f.writelines(new_lines)

print(f"Replaced lines {start} to {end} in .github/workflows/release.yml")
