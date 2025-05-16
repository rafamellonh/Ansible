### 

* Criar ou iniciar uma role 

```
ansible-galaxy init teste

```

```
roles/
└── minha-role/
    ├── tasks/             # Passos principais que a role executa (obrigatório: main.yml)
    ├── handlers/          # Ações disparadas por "notify" (ex: restart de serviços)
    ├── templates/         # Arquivos Jinja2 (.j2) que geram arquivos de configuração dinâmicos
    ├── files/             # Arquivos estáticos copiados como estão (ex: binários, .zip)
    ├── vars/              # Variáveis específicas da role
    ├── defaults/          # Variáveis com valores padrão (menor precedência)
    ├── meta/              # Dependências de outras roles e metadados
    └── tests/             # Testes simples para verificar a role (como playbooks de teste)
```

### Testar a role
```
$ ansible-playbook -i system-update/tests/inventory system-update/tests/test.yml --syntax-check

playbook: system-update/tests/test.yml
```