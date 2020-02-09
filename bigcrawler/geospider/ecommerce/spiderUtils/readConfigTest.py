import ConfigParser

cf = ConfigParser.SafeConfigParser()
# read config
cf.read("test.txt")
# return all section
secs = cf.sections()
print 'sections:', secs

opts = cf.options("sec_a")
print 'options:', opts

kvs = cf.items("sec_a")
print 'sec_a:', kvs



# read by type
str_val = cf.get("sec_a", "a_key1")
int_val = cf.getint("sec_a", "a_key2")


print "value for sec_a's a_key1:", str_val
print "value for sec_a's a_key2:", int_val


# write config
# update value
# cf.set("sec_b", "b_key3", "new-$r")
# # set a new value
# cf.set("sec_b", "b_newkey", "new-value")
# # create a new section
cf.add_section('taobao.com')
cf.set('taobao.com', 'new_key', "{'filter': ['0-11-2', {2: 1}]}")

# write back to configure file
cf.write(open("test.txt", "w"))
