OP = []
res = []
sssssssssssssssssssssssssssssssssssssssssssss
with open("C:\\Users\\Boundless\\Documents\\army\\work\\iPERMS\\auditd_knox.txt") as f:
    lines = f.readlines()[5:]
    for line in lines:
        spaced = line.split('-')

        # grab simple commands
        if spaced[3][0] == 'S':
            #print(spaced[3][2:])
            OP.append(spaced[3][2:])

        # grab the directory explicit commands
        if spaced[2][2:6] == "path":
            #print(spaced[2][7:])
            OP.append(spaced[2][7:])

f.close()


[res.append(x) for x in OP if x not in res]

#write output
with open("C:\\Users\\Boundless\\Documents\\army\\work\\iPERMS\\binaries.txt", 'w') as x:
    for line in res:
        x.write(line + "\n")
    x.close()
