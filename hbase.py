import happybase as db
conn=db.Connection(host='192.168.19.10',port=9090)
conn.open()
families={
    'info':dict(),
    'adress':dict()
}
# conn.create_table('pls_hbase:pls1',families=families)
data=conn.table('pls')
# data.put('001',data={'info:name':'pls'})
# data.put('002',data={'address:street':'sd'})
# data.put('003',data={'info:sex':'男'})
# data.put('004',data={'address:city':'北京'})
# print(list(data.scan())[0][1])

