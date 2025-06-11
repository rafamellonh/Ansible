# 📦 Role Ansible: nginx

Esta role instala e configura o **NGINX** em sistemas baseados no **Ubuntu/Debian**, com foco em automação de ambientes de estudo com **Ansible** e **VMware**.

## ✅ Funcionalidades

- Instala o NGINX utilizando o gerenciador de pacotes `apt`
- Cria diretórios personalizados para organização de configurações
- Copia um `index.html` customizado para `/var/www/html`
- Aplica configurações de site com arquivos disponíveis em `files/`
- Não utiliza certificados SSL (configuração simples e direta)

## 📁 Estrutura

```bash
roles/
└── nginx/
    ├── tasks/
    │   └── main.yml
    ├── files/
    │   ├── site.conf
    │   └── index.html
    └── templates/
```

## 🚀 Como usar

No seu `playbook.yml`:

```yaml
- hosts: web
  become: yes
  roles:
    - nginx
```

## 🛠️ Requisitos

- Ubuntu Server 20.04 ou superior
- Acesso sudo
- Ansible 2.9+

## 📚 Observações

- O arquivo `site.conf` será copiado para `/etc/nginx/sites-available/`
- Certifique-se de que o link simbólico em `/etc/nginx/sites-enabled/` esteja presente (ou configure via role)
- O conteúdo de `index.html` pode ser personalizado em `roles/nginx/files/index.html`

---

## 👨‍💻 Rafael Mello

Este projeto foi criado como parte de estudos com Ansible e ambientes virtualizados utilizando VMware.

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
