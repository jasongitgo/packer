import traceback

y=2
z=1

v={}
while y+z < 300:
    if 4*y+9*z == 400:
        print 'value:%d,%d' % (y,z)
        continue
    else:
        z=1
        while y+z < 300:
            if 4*y+9*z == 400:
                print 'value:%d,%d' % (y,z)
                v[y]=z
                break
            else:
                z+=1
    y+=1

print v
