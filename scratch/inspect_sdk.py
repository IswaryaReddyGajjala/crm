with open("scratch/vobiz-sdk.cjs") as f:
    content = f.read()

start = max(0, 33648 - 150)
end = min(len(content), 33648 + 150)
print(content[start:end])
