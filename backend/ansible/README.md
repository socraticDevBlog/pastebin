![Ansible](https://img.shields.io/badge/ansible-%231A1918.svg?style=for-the-badge&logo=ansible&logoColor=white)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)

# infra/vps

## requirements

- a linux server (debian) with ssh enabled and you have sudo privilege
- have Ansible installed on local machine
  - macOS: `brew install ansible`

## `inventory.ini` file

create a `inventory.ini` file at the root of this directory
and fill it out with your server's information:

- server url
- linux user's username

__don't commit this file with your private information__

``ìni
[linux_vps]
<my_server.com> ansible_user=<my_server_username>

```

## ansible update debian server

play only the check tasks to list what packages are getting upgraded

```bash
ansible-playbook --tags check --ask-become-pass update_debian.yml
```

perform the upgrade

```bash
ansible-playbook --ask-become-pass update_debian.yml
```

## ansible installs and configure postgresql database on Debian server

### test connection to vps first

```bash
ansible -i inventory.ini linux_vps -m ping

# expect success
```

### sensitive value in versionned file

we are using `ansible-vault` command-line tool to create, encrypt, decrypt, and
safely use versionned secrets in files

```bash
# create a new encrypted secrets file
ansible-vault create | edit <file_name>.yml

# will open a vi editor where you you can edit key-value (ini style) secrets
```

### run the playbook with the Vault password

Runs the playbook

- will prompt `BECOME` for your server 'sudo' password
- will prompt `Vault password` for your secret file (ansible-vault) password

```bash
ansible-playbook \
  --ask-vault-pass \
  --ask-become-pass \
  install_postgresql.yml
```

## from local machine

postgresql database is only available from server's localhost network

### ssh tunnel from local machine to server

in order to connect to it from an IDE like DBeaver, establish an ssh tunnel
(leave the terminal open to keep connection open)

```bash
ssh -L 5432:localhost:5432 m@dodeb.socratic.dev
```

### DBeaver IDE

| host      | Database | authentitification | username | password            |
| --------- | -------- | ------------------ | -------- | ------------------- |
| localhost | devdb    | Database native    | devuser  | `<db_password.yml>` |
