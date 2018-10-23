aws-role
========

Assume an aws role and run shell commands with the role applied the environment.


Usage
-----

Create a config file named `role.conf`.

```
[role]
ROLE=arn:aws:iam::994193490583:role/my/role
MFA_SERIAL=arn:aws:iam::089043110190:mfa/dwoz
ACCESS_KEY=AKIFI2FAXD8YOPQ2DOIN
SECRET_KEY=+Om1ibPOjnaKUsV9nNak4Gisf+Jpodoejt2YVwYg
```

Make sure the config file has restricted permissions.

```
chmod 600 role.conf
```

Make sure role.sh is in your path.

```
export PATH="${PATH}:$(pwd)"
```

Run a command using the role

```
role.sh bundle exec kitchen converge py2-windows-2016
```


Using role.sh without having to enter an MFA code
-------------------------------------------------

Install oath-toolkit

```
brew install oath-toolkit
```

Add a new MFA token to your aws account. When presented with a QR code click on
the option to show the MFA secret. Put the MFA secret in your config file.
Note: You can scan still scan the QR code with an authenticator application on
a phone.

```
[role]
ACCESS_KEY=AKIFI2FAXD8YOPQ2DOIN
SECRET_KEY=+Om1ibPOjnaKUsV9nNak4Gisf+Jpodoejt2YVwYg
MFA_SECRET=CX3IC2CNOADPBQPMIIH9GA3IW7NPRNECRQC35WTMHDEGW6PEJJC5VF2OFI3JG7O9
```
