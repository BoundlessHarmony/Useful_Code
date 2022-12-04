writeThis=[]
with open("C:\\Users\\Boundless\\Documents\\army\\work\\iPERMS\\remove_newline_and_add_4_spaces.txt") as f:
    lines = f.readlines()
    for line in lines:
        if line=='\n':
            next
        else:
            writeThis.append(line)
f.close()


#write output
with open("C:\\Users\\Boundless\\Documents\\army\\work\\iPERMS\\formatted_auditd.txt", 'w') as x:
    for line in writeThis:
        x.write("    " + line)
    x.close()
