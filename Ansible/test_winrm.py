import winrm

session = winrm.Session('http://192.168.1.240:5985/wsman',
                        auth=('rafael', 'Brasil2014'))

try:
    r = session.run_cmd('ipconfig')
    print(r.status_code)
    print(r.std_out.decode())
except Exception as e:
    print("Erro:", e)

